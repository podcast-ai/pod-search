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

# from flask_ngrok import run_with_ngrok
import time
import requests
import argparse
from loguru import logger

# from getSimilarity import calc_score
# import backend
import sys, os

sys.path.append(os.path.abspath(os.path.join("engine")))

import search_engine

# config
#os.environ["TOKENIZERS_PARALLELISM"] = "false"

# load the knowledge base
model, index, transcript_data, episode_data = search_engine.indexer("data/knowledge_base")

flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return render_template("index.html")


@flask_app.route("/search", methods=["GET", "POST"])
def search():
    # Param 1 $sentence$. Retrieve the search input from the user text-ins.
    query_text = request.form.get("inputText")

    results = search_engine.get_json_segments(
        query_text, 
        transcript_data, 
        episode_data, 
        model, 
        index,
        limit=1,
    )
    # results = backend.query(query_text)

    logger.info("rendering result")
    return render_template(
        "test.html", 
        query_text=query_text, 
        results=results
    )


if __name__ == "__main__":
    flask_app.run(debug=False)
