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


def diarization(audio_data: str, podcast_dir: str) -> str:
    """
    Takes podcast audio file as input and spits out audio segments corresponding to different speakers in that particular
    podcast this process is called diarization.
    Which according to WIKI is :
    The process of partitioning an input audio stream into homogeneous segments according to the speaker identity

    It is basically used to answer the question "who spoke when?
    """
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(f"./{podcast_dir}/{audio_data}.wav")

    return str(diarization)


def crapy_diarization(audio) -> list:
    """
    Returns the same thing as what the diarization function does but not very accurate !
    """
    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")
    diarization = pipeline({"audio": "H:\wav2vec_pre\audio.wav"})

    return diarization


def get_chunks(trans_chunk, dizi) -> str:
    """
    Returns speaker ID corresponding to the segments listed by transcription data CSV **

    ** see main function for reference
    """
    for i in dizi:
        q = []
        q = i.split(" ")
        if trans_chunk >= get_sec(q[1]) and trans_chunk <= get_sec(q[4][:-1]):
            return str(q[-1])


def get_sec(stamp: str) -> float:
    """
    Converts the time stamp from diarization to H:M:S:MS format.
    """
    x = time.strptime(stamp.split(",")[0], "%H:%M:%S.%f")
    x = dt.timedelta(
        hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec
    ).total_seconds()

    return float(x)


def preprocess(trans_df, dizi) -> any:
    """
    Concatenate results from diarization and transcription data from the CSV **

    ** see main function for reference
    """
    for row in range(len(trans_df)):
        # print(trans_df.iloc[row]['chunk_start'])
        speaker = get_chunks(float(trans_df.iloc[row]["chunk_start"]), dizi)
        trans_df.at[row, "speaker"] = speaker
        # print(speaker)

    return trans_df


def main(episode: str, transcription: str, podcast_dir: str) -> any:
    """
    This function calls all the other functions.

    arguments:
        episode             data from the csv with format [episode_id,episode_name].
        transcription       data from the csv with format [episode_id, chunk_number, chunk_start, chunk_end, text, ...].
        podcast_dir         folder name where all the podcast audio files are stored.

        episode and transcription comes from the knowledge base
    """
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

    parser = argparse.ArgumentParser(
        description="Getting all the required files for segmentation."
    )
    parser.add_argument(
        "fn_01",
        metavar="[EPISODE DATA]",
        type=str,
        help="Episode data CSV with format [episode_id, episode_name] | example: episode.csv",
    )
    parser.add_argument(
        "fn_02",
        metavar="[TRANSCRIPTION DATA]",
        type=str,
        help="Transcription data CSV with format [episode_id, chunk_number, chunk_start, chunk_end, text, ...] | example: transcription.csv",
    )
    parser.add_argument(
        "fn_03",
        metavar="[PODCAST FOLDER]",
        type=str,
        help="folder address for all the podcast audio files",
    )
    args = parser.parse_args()

    segmented_transcription = main(args.fn_01[0], args.fn_02[0]), args.fn_03[0]
    # print(segmented_transcription)

    segmented_transcription.to_csv("segmented_transcription.csv")
