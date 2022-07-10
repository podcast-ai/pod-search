import torch
import numpy as np
import pandas as pd
import argparse
#from pyannote.audio import Pipeline

## pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
## git clone https://github.com/speechbrain/speechbrain.git
## pip install speechbrain

## gives very accurate results
def diarization() -> list:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline("audio.wav")

    return diarization

def crapy_diarization(audio) -> list:
    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")
    diarization = pipeline({"audio":"H:\wav2vec_pre\audio.wav"})

    return diarization

def get_chunks(trans_chunk,dizi) -> list:
   # for _, (i,j) in enumerate(dia_list):
   #     if start > i and start < j:
   #         return dia_list[something]
   return 1

def preprocess(trans_df, dizi) -> any:
    for row in range(len(trans_df)):
        trans_df.iloc[row]['speaker'] = get_chunks(trans_df.iloc[row]['chunk_start'], dizi)
    return trans_df

def main(episode:str, transcription:str) -> any:
    ep = pd.read_csv(episode)
    trans = pd.read_csv(transcription)
    trans['speaker'] = np.nan
    ep_id = list(ep.episode_id)
    print(f"ep : {ep.head()}, trans : {trans.head()}, ep_id : {ep_id}")
    for i in ep_id:
        dizi = crapy_diarization(ep[ep['episode_id'] == i]["file_name"])
        print(dizi)
        trans_df = trans[trans['episode_id'] == i]
        trans_df = preprocess(trans_df, dizi)
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
