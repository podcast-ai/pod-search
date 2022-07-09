from dataclasses import dataclass
import os
import time
from typing import List, Tuple, Union
import librosa
import numpy as np
import pandas as pd
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

SAMPLE_RATE = 16_000
CHUNK_DURATION_SECS = 10
HF_MODEL_PATH = "facebook/wav2vec2-base-960h"
DATASET_PATH = "podcasts/"
N_CHUNKS_PER_BATCH = 20


class HuggingFaceWav2Vec2Transcriber:
    def __init__(self, model_path: str):
        self.processor = Wav2Vec2Processor.from_pretrained(model_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_path)
        self.sr: int = 16_000

    def transcribe_waves(
        self, waves: Union[np.array, List[np.array]], sr: float
    ) -> str:
        assert sr == self.sr, f"Sample rate must be {self.sr}"
        inputs = self.processor(
            waves, sampling_rate=self.sr, return_tensors="pt", padding=True
        )

        with torch.no_grad():
            logits = self.model(
                inputs.input_values  # , attention_mask=inputs.attention_mask
            ).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = self.processor.batch_decode(predicted_ids)
        return predicted_sentences


@dataclass
class ChunkTimestamp:
    begin_secs: float
    end_secs: float


def make_chunks_from_wave(
    wave: np.array, sr: float, chunk_duration_secs: float
) -> Tuple[List[np.array], List[ChunkTimestamp]]:

    chunk_duration_timesteps = sr * chunk_duration_secs
    n_chunks = np.ceil(len(wave) / chunk_duration_timesteps)

    chunk_waves = np.array_split(wave, n_chunks)

    chunk_end_times = np.cumsum([sr * len(wave) for wave in chunk_waves]).tolist()
    chunk_begin_times = [0] + chunk_end_times[:-1]
    chunk_timestamps = [
        ChunkTimestamp(b, e) for b, e in zip(chunk_begin_times, chunk_end_times)
    ]

    return chunk_waves, chunk_timestamps


def main(list_of_audio_files):

    print(f"Using model {HF_MODEL_PATH} for transcriptions.\n")
    transcriber = HuggingFaceWav2Vec2Transcriber(HF_MODEL_PATH)

    results = []

    begin_time_overall = time.time()

    for audio_file in list_of_audio_files:

        begin_time_audio_file = time.time()

        print(f"\nLoading {audio_file}")
        wave, _ = librosa.load(audio_file, sr=SAMPLE_RATE)

        print(
            f"Getting audio chunks of duration {CHUNK_DURATION_SECS} secs, plus timestamps"
        )
        chunk_waves, chunk_timestamps = make_chunks_from_wave(
            wave, SAMPLE_RATE, CHUNK_DURATION_SECS
        )
        print(f"Obtained {len(chunk_timestamps)} chunks")

        print("Transcribing chunks")
        n_batches = int(np.ceil(len(chunk_waves) / N_CHUNKS_PER_BATCH))
        batches = [
            chunk_waves[(i * N_CHUNKS_PER_BATCH) : ((i + 1) * N_CHUNKS_PER_BATCH)]
            for i in range(n_batches)
        ]
        chunk_transcriptions = [
            transcription
            for batch in batches
            for transcription in transcriber.transcribe_waves(batch, SAMPLE_RATE)
        ]
        print(f"Transcribed chunks. Sample transcription: {np.random.choice(chunk_transcriptions)}")

        results.extend(
            [
                {
                    "audio_file": audio_file,
                    "chunk_num": i,
                    "transcription": text,
                    "begin_secs": ts.begin_secs,
                    "end_secs": ts.end_secs,
                }
                for i, (text, ts) in enumerate(
                    zip(chunk_transcriptions, chunk_timestamps)
                )
            ]
        )

        timedelta_audio_file = time.time() - begin_time_audio_file
        print(
            f"Seconds elapsed while processing {audio_file}: {timedelta_audio_file:.2f}"
        )

    pd.DataFrame(results).to_csv("transcribed_audios.csv", index=False)

    total_timedelta = time.time() - begin_time_overall
    print(f"\n\nTotal seconds elapsed: {total_timedelta:.2f}")


if __name__ == "__main__":
    podcast_filenames = [DATASET_PATH + x for x in os.listdir(DATASET_PATH)]
    main(podcast_filenames)
