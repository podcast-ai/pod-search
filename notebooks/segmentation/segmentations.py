import torch
import numpy as np
import pandas as pd
import argparse

from pyannote.audio import Pipeline
import datetime as dt
import time
#from pyannote.audio import Pipeline

### prerequisite
## pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
## git clone https://github.com/speechbrain/speechbrain.git
## pip install speechbrain


## gives very accurate results
def diarization(audio:str) -> str:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(f"/content/{audio}.wav")

    return str(diarization)

## total crap but faster runtime
def crapy_diarization(audio) -> list:
    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")
    diarization = pipeline({"audio":"H:\wav2vec_pre\audio.wav"})

    return diarization


def get_chunks(trans_chunk,dizi) -> str:
    for i in dizi:
      q = []
      q = i.split(" ")
      if trans_chunk >= get_sec(q[1]) and trans_chunk <= get_sec(q[4]):
        print(q[1],q[-1])
        return str(q[-1])

def get_sec(stamp:str) -> float:
   x = time.strptime(stamp.split(',')[0],'%H:%M:%S.%f')
   x = dt.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
   return float(x)

def preprocess(trans_df, dizi) -> any:
    for row in range(len(trans_df)):
        #print(trans_df.iloc[row]['chunk_start'])
        trans_df.iloc[row]['speaker'] = get_chunks(float(trans_df.iloc[row]['chunk_start']), dizi)
    return trans_df

def main(episode:str, transcription:str) -> any:
    ep = pd.read_csv(episode)
    trans = pd.read_csv(transcription)
    trans['speaker'] = np.nan
    ep_id = list(ep.episode_id)
    print(f"ep : {ep.head()}, trans : {trans.head()}, ep_id : {ep_id}")
    dizi_chunks = []
    for i in ep_id:
        dizi = diarization(ep[ep['episode_id'] == i]["file_name"])
        dizi_chunks = dizi.split("\n")
        trans_df = trans[trans['episode_id'] == i]
        trans_df = preprocess(trans_df, dizi_chunks)
    return trans_df

## Building an ETL
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Segmentations.')
    parser.add_argument('fn_01', metavar='episode data', type=str, nargs='+',
                        help='episode data')
    parser.add_argument('fn_02', metavar='transcription data', type=str, nargs='+',
                        help='transcription data')
    args = parser.parse_args()
    segmented_transcription = main(args.fn_01[0], args.fn_02[0])
    print(segmented_transcription)
