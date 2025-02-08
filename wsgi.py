from api import create_app

app = create_app()

# for development
if __name__ == "__main__":
    app.run()