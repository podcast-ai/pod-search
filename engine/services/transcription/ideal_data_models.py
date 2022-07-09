# TODO: all code is commented out - is this module still needed?
# from dataclasses import dataclass
# from typing import List, Optional, Tuple
# import librosa
# import numpy as np

# from abc import ABC, abstractmethod
# from __future__ import annotations


# Basic stuff, for sure needed


# @dataclass
# class Podcast:
#     id: str


# @dataclass
# class ChunkTimestamp:
#     beginning_secs: float
#     end_secs: float


# @dataclass
# class TranscriptionChunk:
#     podcast: Podcast
#     transcription: str
#     timestamp: ChunkTimestamp


# # super general repr of audiosource


# class AudioSource:
#     pass


# # subclasses of audiosource for local transcription


# @dataclass
# class AudioChunkForLocalTranscription:
#     podcast: Podcast
#     wave: np.array
#     sr: int
#     timestamp: ChunkTimestamp


# class AudioSourceForLocalTranscription:
#     # also abstract, yields AudioChunksForLocalTranscription
#     pass


# class AudioSourceForLocalTranscriptionImpl1(AudioSourceForLocalTranscription):
#     pass


# # General repr of transcriber


# class Transcriber(ABC):
#     @abstractmethod
#     def transcribe(self, audio_source: AudioSource) -> List[TranscriptionChunk]:
#         pass


# class LocalTranscriber(
#     Transcriber, ABC
# ):  # this inheritanec is kind of weird, but the idea is that there could bea family of local transcribers
#     pass







# @dataclass(slots=True)
# class AudioChunk:
#     wave: np.array
#     sr: int
#     timestamp_secs: Tuple[float, float]


# @dataclass
# class TranscriptionChunk:
#     transcription: str
#     timestamp_secs: Tuple[float, float]

#     def __add__(self, other_chunk: TranscriptionChunk) -> TranscriptionChunk:
#         beg_1, end_1 = self.timestamp_secs
#         beg_2, end_2 = other_chunk.timestamp_secs
#         one_before_two = round(end_1, 2) == round(beg_2, 2)
#         two_before_one = round(end_2, 2) == round(beg_1, 2)
#         consecutive = one_before_two or two_before_one
#         assert consecutive, "Audio chunks must be consecutive to add them"

#         if one_before_two:
#             text = self.transcription + " " + other_chunk.transcription
#             timestamp_secs = (beg_1, end_2)
#             return TranscriptionChunk(text, timestamp_secs)
#         else:
#             text = other_chunk.transcription + " " + self.transcription
#             timestamp_secs = (beg_2, end_1)
#             return TranscriptionChunk(text, timestamp_secs)


# class AudioSource(ABC):
#     pass


# class AudioChunksFromFilename(AudioSource):

#     def __init__(self, filename, sr, chunk_duration_secs):
#         self.sr = sr
#         self.chunk_duration_secs = chunk_duration_secs
#         self.chunk_duration_timesteps = self.sr * self.chunk_duration_secs
#         self.full_wave = librosa.load(filename, sr)
#         self.i = 0

#     def __iter__(self):
#         return self

#     def __next__(self):

#         initial_timestep = self.i * self.chunk_duration_timesteps
#         end_timestep = initial_timestep + self.chunk_duration_timesteps

#         if initial_timestep > len(self.full_wave):
#             raise StopIteration

#         chunk_wave = self.full_wave[
#             initial_timestep : (initial_timestep + self.chunk_duration_timesteps)
#         ]
#         chunk_ts_secs = (initial_timestep / self.sr, end_timestep / self.sr)

#         self.i += 1
#         return AudioChunk(chunk_wave, chunk_ts_secs)


# class Transcriber(ABC):

#     @abstractmethod
#     def transcribe_chunk(self, audio_chunk: AudioChunk) -> TranscriptionChunk:
#         pass

#     def transcribe(self, audio_source: AudioSource):


# class HuggingFaceTranscriber()
