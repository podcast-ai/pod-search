"""Run the ETL worker to prepare the knowledge base."""

import etl, config, schema
from loguru import logger
import sys
import os


sys.path.append(os.path.abspath(os.path.join("engine")))

import search_engine
import config


def prepare_knowledge_base():
    logger.info("Preparing knowledge base")
    logger.info("processing transcripts")
    transcript_data, episode_data = etl.process_transcripts(
        config.transcript_dir,
    )
    logger.info("storing knowledge base")
    etl.store_knowledge_base(
        transcript_data,
        episode_data,
        config.knowledge_base_dir,
    )

def prepare_search_index():
    logger.info("Preparing search index")
    model, index, transcript_data, episode_data = search_engine.indexer(config.knowledge_base_dir)

def prepare_search_index():
    logger.info("Preparing search index")

if __name__ == "__main__":
    logger.info("Starting worker")

    prepare_knowledge_base()
    
    prepare_search_index()


