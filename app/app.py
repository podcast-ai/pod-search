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
#from flask_ngrok import run_with_ngrok
import time
import requests
import argparse
#from getSimilarity import calc_score
#import backend
import sys, os
sys.path.append(os.path.abspath(os.path.join('engine')))

from search_engine import indexer,get_json_segments

# load the knowledge base
model,index,df,episode_df = indexer('data/knowledge base')

flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return render_template("index.html")


@flask_app.route("/search", methods=["GET", "POST"])
def search():
    # Param 1 $sentence$. Retrieve the search input from the user text-ins.
    query_text = request.form.get("inputText")

    results = get_json_segments(query_text,df,episode_df,model,index)
    #results = backend.query(query_text)

    return render_template(
        "test.html",
        query_text=query_text,
        results=results
    )


if __name__ == "__main__":
    flask_app.run(debug=True)
