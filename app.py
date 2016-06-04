from app import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
