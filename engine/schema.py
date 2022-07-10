"""Data Schema definitions."""

from pyparsing import null_debug_action
from pandera import Column, DataFrameSchema, Check, Index

knowledge_base = DataFrameSchema(
    {
        "chunk_start": Column(float, nullable=False),
        "chunk_end": Column(float, nullable=False),
        "chunk_number": Column(int, nullable=False),
        "paragraph_number": Column(int, nullable=False),
        "text": Column(str, nullable=False),
        "confidence": Column(float, nullable=True),
        "file_name": Column(str, nullable=False),
    },
)
