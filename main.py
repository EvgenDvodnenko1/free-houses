from app import app
from models import Config

if __name__ == '__main__':
    Config.up()
    app.run(debug=True)