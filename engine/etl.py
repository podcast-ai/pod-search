"""Extract / transform / load functions here."""

from pathlib import Path
from pandera.typing import DataFrame

import pandas
import tqdm
from loguru import logger


def parse_google_transcript(
    path,
    episode_id: int = None,
) -> DataFrame:
    """Parse Google Speech to Text API result .json -> pandas.DataFrame"""
    transcript_data = pandas.read_json(path)
    # transcript_data["file_name"] = path.stem
    transcript_data["episode_id"] = episode_id
    return transcript_data


def clean_google_transcript(
    transcript_data,
) -> DataFrame:
    """Clean Google Speech to Text API result."""
    transcript_data = transcript_data.rename(
        columns={"start": "chunk_start", "end": "chunk_end", "newpara": "new_paragraph"}
    )
    transcript_data["new_paragraph"] = (
        transcript_data["new_paragraph"].fillna(0.0).astype(bool)
    )
    transcript_data["chunk_number"] = transcript_data.index
    # enumerate paragraphs
    transcript_data["paragraph_number"] = transcript_data["new_paragraph"].cumsum()
    transcript_data = transcript_data.drop(columns=["new_paragraph"])
    return transcript_data


def process_transcripts(
    transcript_dir,
):
    """Process all transcripts in a directory and create the files of the knowledge base."""
    transcript_paths = [p for p in transcript_dir.glob("*.json")]
    transcript_data = []
    for episode_id, path in enumerate(tqdm.tqdm(transcript_paths)):
        logger.debug(f"processing {path}")
        transcript_data.append(
            clean_google_transcript(
                parse_google_transcript(
                    path,
                    episode_id,
                )
            )
        )
    episode_data = pandas.DataFrame(
        [
            {"episode_id": episode_id, "file_name": path.stem}
            for episode_id, path in enumerate(transcript_paths)
        ]
    )
    transcript_data = pandas.concat(transcript_data)
    transcript_data = transcript_data.set_index(["episode_id", "chunk_number"])
    episode_data = episode_data.set_index("episode_id")
    return transcript_data, episode_data


def store_knowledge_base(
    transcript_data,
    episode_data,
    knowledge_base_dir,
):
    """Store knowledge base."""
    transcript_data.to_parquet(knowledge_base_dir / "transcript_data.parquet")
    episode_data.to_parquet(knowledge_base_dir / "episode_data.parquet")
    # transcript_data.to_json(knowledge_base_dir / "transcript_data.json")
    # episode_data.to_json(knowledge_base_dir / "episode_data.json")


def load_knowledge_base(
    knowledge_base_dir,
):
    """Load knowledge base."""
    knowledge_base_dir = Path(knowledge_base_dir)
    transcript_data = pandas.read_parquet(
        knowledge_base_dir / "transcript_data.parquet"
    )
    episode_data = pandas.read_parquet(knowledge_base_dir / "episode_data.parquet")

    return {
        "transcript_data": transcript_data,
        "episode_data": episode_data,
    }
