from flask import Flask
from producer import producer
application = Flask(__name__)

@application.route("/")
def routine():
    producer()
    return "Hello World!"

if __name__ == "__main__":
    application.run()
