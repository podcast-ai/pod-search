import torch
import numpy as np
import pandas as pd
import argparse

from pyannote.audio import Pipeline
import datetime as dt
import time


### prerequisite
## pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
## git clone https://github.com/speechbrain/speechbrain.git
## pip install speechbrain


"""
Takes podcast audio file as input and spits out audio segments corresponding to different speakers in that perticular
podcast this process is called diarization.
Which according to WIKI : 
The process of partitioning an input audio stream into homogeneous segments according to the speaker identity

It is basically used to answer the question "who spoke when?
"""
## gives very accurate results
def diarization(audio_data: str, podcast_dir: str) -> str:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(f"./{podcast_dir}/{audio_data}.wav")

    return str(diarization)


"""
Returns the same thing as what the diarization function does but not very accurate !
"""
## total crap but faster runtime
def crapy_diarization(audio) -> list:
    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")
    diarization = pipeline({"audio": "H:\wav2vec_pre\audio.wav"})

    return diarization


"""
Returns speaker ID corresponding to the segments listed by transcription data CSV **

** see main function for reference 
"""
def get_chunks(trans_chunk, dizi) -> str:
    for i in dizi:
        q = []
        q = i.split(" ")
        if trans_chunk >= get_sec(q[1]) and trans_chunk <= get_sec(q[4][:-1]):
            return str(q[-1])


"""
Gets the time stamp from diarization to H:M:S:MS format.
"""
def get_sec(stamp: str) -> float:
    x = time.strptime(stamp.split(",")[0], "%H:%M:%S.%f")
    x = dt.timedelta(
        hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec
    ).total_seconds()

    return float(x)


"""
concatenate results from diarization and transcription data from the CSV **

** see main function for reference 
"""
def preprocess(trans_df, dizi) -> any:
    for row in range(len(trans_df)):
        # print(trans_df.iloc[row]['chunk_start'])
        speaker = get_chunks(float(trans_df.iloc[row]["chunk_start"]), dizi)
        trans_df.at[row, "speaker"] = speaker
        # print(speaker)

    return trans_df


"""
This function calls all the other functions.

arguments:
    episode             data from the csv with format [episode_id,episode_name].
    transcription       data from the csv with format [episode_id, chunk_number, chunk_start, chunk_end, text, ...].
    podcast_dir         folder name where all the podcast audio files are stored.

    episode and transcription comes from the knowledge base
"""
def main(episode: str, transcription: str, podcast_dir: str) -> any:
    ep = pd.read_csv(episode, index_col=0)
    trans = pd.read_csv(transcription, index_col=0)
    trans["speaker"] = None
    trans["episode_id"] = 0
    ep_id = list(ep.index)
    # print(f"ep : {ep.head()}\n, trans : {trans.head()}, ep_id : {ep_id}")
    dizi_chunks = []

    for i in ep_id:
        # print(ep[ep.index == i].file_name)
        dizi = diarization(ep[ep.index == i]["file_name"][0], podcast_dir)
        dizi_chunks = dizi.split("\n")
        trans_df = trans[trans["episode_id"] == i]
        trans_df = preprocess(trans_df, dizi_chunks)
    return trans_df


## Building an ETL
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Segmentations.")
    parser.add_argument(
        "fn_01", metavar="episode data", type=str, nargs="+", help="episode data"
    )
    parser.add_argument(
        "fn_02",
        metavar="transcription data",
        type=str,
        nargs="+",
        help="transcription data",
    )
    parser.add_argument(
        "document",
        metavar="audio data pre address",
        type=str,
        nargs="+",
        help="pre address",
    )
    print("Usage: python3 segmentation.py [TRANSCRIPT DATA]... [EPISODE DATA]... [PODCAST FOLDER]...")
    args = parser.parse_args()

    #segmented_transcription = main(args.document, args.fn_01[0], args.fn_02[0])
    # print(segmented_transcription)

    #segmented_transcription.to_csv("segmented_transcription.csv")
