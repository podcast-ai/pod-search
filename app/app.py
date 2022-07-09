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
from getSimilarity import calc_score
from getID import getID

flask_app = Flask(__name__)


@flask_app.route("/")
def Home():
    return render_template("index.html")


@flask_app.route("/predict", methods=["GET", "POST"])
def predict():
    # Param 1 $sentence$. Retrieve the search input from the user text-ins.
    sentence = request.form.get("inputText")
    target = request.args.get("question")
    target = escape(target)

    # Param 2 $fileName$. Get the selected file_name.
    save_path = "./notebooks/transcription/data_samples.csv"
    # fileName = './notebooks/transcription/data_mp3/' + getID(save_path, sentence)
    fileName = "./static/data/" + getID(save_path, sentence)
    # Parm 3 & 4 $startTime$ $endTime$ Here are the time we need to trim, which they will send back to the client side.
    startTime = 0
    endTime = 100

    return render_template(
        "test.html",
        sentence="{}".format(sentence),
        fileName="{}".format(fileName),
        startTime="{}".format(startTime),
        endTime="{}".format(endTime),
    )


if __name__ == "__main__":
    flask_app.run(debug=True)
