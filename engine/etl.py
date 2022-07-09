"""Extract / transform / load functions here."""

from pandera.typing import DataFrame

import pandas

def google_transcript_to_dataframe(
    path,
) -> DataFrame:
    """Parse Google Speech to Text API result .json -> pandas.DataFrame"""
    transcript_data = pandas.read_json(path)
    return transcript_data