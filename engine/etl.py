"""Extract / transform / load functions here."""

from pandera.typing import DataFrame

import pandas

def read_google_transcript(
    path,
) -> DataFrame:
    """Parse Google Speech to Text API result .json -> pandas.DataFrame"""
    transcript_data = pandas.read_json(path)
    return transcript_data
