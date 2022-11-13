from flask_base import app
from flask_base.controllers import start, readers, journalists, news

if __name__ == "__main__":
    app.run(debug=True)
    