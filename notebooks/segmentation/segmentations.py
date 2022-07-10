import torch
from pyannote.audio import Pipeline

## pip install https://github.com/pyannote/pyannote-audio/archive/develop.zip
## git clone https://github.com/speechbrain/speechbrain.git
## pip install speechbrain

## gives very accurate results
def diarization() -> list:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline("audio.wav")

    return diarization

def crapy_diarization() -> list:
    pipeline = torch.hub.load("pyannote/pyannote-audio", "dia")
    diarization = pipeline({"audio": "audio.wav"})

    return diarization

def get_chunks() -> list:
    pass

def main(episode:str, transcription:str) -> pd.dataframe:
    ep = pd.read_csv(episode)
    trans = pd.read_csv(transcription)
    ep_id = list(ep.episode_id)
    print(ep_id)
    pass

## Building an ETL
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Segmentations.')
    parser.add_argument('fn_01', metavar='episode data', type=str, nargs='+',
                        help='episode data')
    parser.add_argument('fn_02', metavar='transcription data', type=str, nargs='-',
                        help='transcription data')
    args = parser.parse_args()
    segmented_transcription = main(args.fn_01[0], args.fn_02[0])
