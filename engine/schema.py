"""Data Schema definitions."""

from pandera import Column, DataFrameSchema, Check, Index

transcript_data = DataFrameSchema(
    {
        "episode_id": Column(int),
        "chunk_number": Column(int, nullable=False),
        "chunk_start": Column(float, nullable=False),
        "chunk_end": Column(float, nullable=False),
        "paragraph_number": Column(int, nullable=False),
        "text": Column(str, nullable=False),
        "confidence": Column(float, nullable=True),
        "file_name": Column(str, nullable=False),
    },
)


episode_data = DataFrameSchema(
    {
        "episode_id": Column(int),
        "file_name": Column(str, nullable=False),
    },
)
