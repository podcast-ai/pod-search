from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    send_from_directory,
    render_template,
    escape,
    session,
)

from functools import lru_cache
from flask_ngrok import run_with_ngrok
import time
import requests
import argparse






flask_app = Flask(__name__)

@flask_app.route("/")
def Home():
    return render_template("index.html")


@flask_app.route("/predict", methods=['GET', 'POST'])
def predict():
    # retrieve the answer input from the user text-ins
    sentence = request.form.get('inputText')
    target = request.args.get('question')
    target = escape(target)
    startTime = 1
    endTime = 1.5

    return render_template("test.html", sentence = "{}".format(sentence), startTime = "{}".format(startTime), endTime = "{}".format(endTime))







if __name__ == "__main__":
    flask_app.run(debug=True)























