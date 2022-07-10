"""Unit tests for the etl module."""

from pathlib import Path

from engine import etl

def test_parse_google_transcript():
    """Test the parse_google_transcript function."""
    transcript_data = etl.parse_google_transcript(
        path=Path("data/transcripts/Google/20220701 lex_ai_demis_hassabis.json"),
        episode_id=0,
    )
    assert not transcript_data.empty