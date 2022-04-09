from project import create_app

app = create_app("config.DevConfig")

# Call the application factory function to construct a Flask application
# instance using the development configuration
if __name__ == "__main__":
    app.run()
