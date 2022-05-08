from project import db
from project.authentification.models import User
from project.cryptocurrency.models import (
    Cryptocurrency,
    Profit,
    Purchase,
    QuoteCurrency,
)
from datetime import date, datetime, timedelta
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from sqlalchemy.sql import func, select, desc
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


def get_user_current_total_valorization(user_id: int, only_total=False):
    """This function get an user and return is current total valorization
        and  if the only_total is false the valoziration for each purchase.
    Args:
        user_id (int): the user id that we want
        only_total (bool, optional):
            flag for check if we only want the total of the
            current valorization. Defaults to False.

    Returns:
        only_total == False : a tuple that containt a list of dic and an int
        only_total == True : return an int
    """
    # Get the last quote of a cryptocurrency
    get_lastest_quote = (
        select(QuoteCurrency.price)
        .filter(QuoteCurrency.cryptocurrency_id == Cryptocurrency.id)
        .order_by(desc(QuoteCurrency.date))
        .limit(1)
        .scalar_subquery()
    )
    # Get the current total of each cryptocurrency valorization for an user
    cryptocurrencys_total = (
        Purchase.query.join(Cryptocurrency)
        .with_entities(
            (
                get_lastest_quote * func.sum(Purchase.quantity)
                - func.sum(Purchase.price)
            ).label("valorization")
        )
        .filter(Purchase.user_id == user_id)
        .group_by(Cryptocurrency.id)
        .subquery()
    )
    # Get the current sum of the valorizations
    total_valorization = (
        db.session.query(func.sum(cryptocurrencys_total.c.valorization))
        .select_entity_from(cryptocurrencys_total)
        .scalar()
    )
    # if the total is none the total is set to 0
    if total_valorization is None:
        total_valorization = 0
    if only_total:
        return total_valorization
    # Get for each purchase data of cryptocurrency(name,symbol,icon) and
    # the valorization of each purchase
    cryptocurrencys = (
        Purchase.query.join(Cryptocurrency)
        .with_entities(
            Cryptocurrency.name.label("name"),
            Cryptocurrency.symbol.label("symbol"),
            Cryptocurrency.coinmarketcap_icon.label("icon"),
            (get_lastest_quote * Purchase.quantity - Purchase.price).label(
                "valorization"
            ),
        )
        .filter(Purchase.user_id == user_id)
        .order_by("name")
    )
    return (
        cryptocurrencys,
        total_valorization,
    )


def get_user_total_valorization_of_the_day(user_id: int) -> tuple:
    """This function get an user id and return the valorization
        the last valorization of yesterday.
    Args:
        user_id (int): the user id that we want

    Returns:
        tuple: last valorization of yesterday and yesterday is date
    """
    yesterday = date.today() - timedelta(days=1)
    yesterday_start = datetime.combine(yesterday, datetime.min.time())
    yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59)
    # Get the last quote of the day
    get_lastest_quote_of_the_day = (
        select(QuoteCurrency.price)
        .filter(
            QuoteCurrency.cryptocurrency_id == Cryptocurrency.id,
            QuoteCurrency.date <= yesterday_end,
        )
        .order_by(desc(QuoteCurrency.date))
        .limit(1)
        .scalar_subquery()
    )
    cryptocurrencys_total_day = (
        Purchase.query.join(Cryptocurrency)
        .with_entities(
            (
                get_lastest_quote_of_the_day * func.sum(Purchase.quantity)
                - func.sum(Purchase.price)
            ).label("valorization"),
        )
        .filter(Purchase.user_id == user_id, Purchase.date <= yesterday_end)
        .group_by(Cryptocurrency.id)
        .subquery()
    )
    # Get the last sum of the valorizations
    total_valorization = (
        db.session.query(func.sum(cryptocurrencys_total_day.c.valorization))
        .select_entity_from(cryptocurrencys_total_day)
        .scalar()
    )
    # if the total is none the total is set to 0
    if total_valorization is None:
        total_valorization = 0
    return (total_valorization, yesterday_end)


def add_cryptocurrency():
    """This function fetch coinmarketcap api data and add a list of
    cryptocurrency in the database
    """
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"
    parameters = {
        "id": "1,1027,52,3408,74",
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": environ.get("COIN_MARKET_CAP_API_KEY"),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        for i in data["data"]:
            item = data["data"][i]
            new_crypto = Cryptocurrency(
                name=item["name"],
                symbol=item["symbol"],
                coinmarketcap_id=item["id"],
                coinmarketcap_icon=item["logo"],
            )
            db.session.add(new_crypto)
            db.session.commit()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    finally:
        session.close()


def update_quote():
    """This function fetch coinmarketcap api data and add the last
    quote currency of each cryptocurrency in the database
    """
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    cryptocurrencys = Cryptocurrency.query.all()
    dico_id = {item.coinmarketcap_id: item.id for item in cryptocurrencys}
    string_of_id = ",".join([str(id) for id in dico_id.keys()])
    parameters = {"id": string_of_id, "convert": "EUR"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": environ.get("COIN_MARKET_CAP_API_KEY"),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        for i in data["data"]:
            item = data["data"][i]
            date_time_tz = datetime.strptime(
                item["quote"]["EUR"]["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            date_sql = date_time_tz.strftime("%Y-%m-%d %H:%M:%S")
            new_quote = QuoteCurrency(
                cryptocurrency_id=dico_id.get(item["id"]),
                price=item["quote"]["EUR"]["price"],
                date=date_sql,
            )
            db.session.add(new_quote)
            db.session.commit()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    finally:
        session.close()


def daily_update_user_last_valorization():
    """This function get the list of all user and call
    the function get_user_total_valorization_of_the_day for
    each of them to store the last valorization of yesterday
    for each of them.
    """
    user_id_list = [id for id, in db.session.query(User.id).all()]
    for user_id in user_id_list:
        (
            total_valorization,
            yesterday_end,
        ) = get_user_total_valorization_of_the_day(user_id)
        new_profit = Profit(
            user_id=user_id,
            profit_and_loss=total_valorization,
            date=yesterday_end,
        )
        db.session.add(new_profit)
        db.session.commit()
