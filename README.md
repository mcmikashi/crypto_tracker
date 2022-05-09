# crypto_tracker
A small application that shows the valuation of your investments in cryptocurrency
## Requirement 
* [Python 3](https://www.python.org/downloads/)
* An UNIX OS (optionaly for run test properly windows doesn't allow multiprocessing) or run test on the github action)
## Demo
link : [crypto-tracker](https://crypto-tracker40.herokuapp.com/)

Demo user :

e-mail = test@test.com

password = azerty973

## Installation Instructions
Clone the repository :

`git clone https://github.com/mcmikashi/crypto_tracker.git`

Create a new virtual environment:
```
cd crypto_tracker
python3 -m venv env
```
Activate the virtual environment:

`source env/bin/activate`

Install the python packages specified in requirements.txt:

`pip install -r requirements.txt`

Set env file :
For this step you will need to get an api key on [link](https://coinmarketcap.com/api/)
and choose the type of database that you want to use [link](https://docs.sqlalchemy.org/en/14/core/engines.html)
for smtp server the default value is server: smtp.office365.com and port  : 587 change this value on config.py file
```
cp .env_exemple .env
sed -i 's/secret_key/${{ your_seret_key }}/g' .env 
sed -i 's/password_salt/${{ your_password_slat }}/g' .env 
sed -i 's/db_prod_uri/{{your_db}}/g' .env
sed -i 's/api_key/{{your_api_key}}/g' .env
sed -i 's/email/{{your_email}}/g' .env
sed -i 's/email_password/{{your_email_password}}/g' .env 
```
Database Initialization:
```
flask shell
from project import db
db.create_all()
```
Running the Flask Application:
```
flask run
```
Now you can navigate to 'http://localhost:5000' in your favorite web browser to view the website!

## Test and Coverage
Once you finish to install the app
you can test by adding the database test again this [link](https://docs.sqlalchemy.org/en/14/core/engines.html) will help you to use specific database.
```
sed -i 's/db_test_uri/{{your_db}}/g' .env
```
Then run the test 
```
coverage run -m unittest discover tests
```
And for the coverage run 
```
coverage report
```
