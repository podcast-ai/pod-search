"""Run the ETL worker to prepare the knowledge base."""

import etl, config, schema
from loguru import logger

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
    raise NotImplementedError("TODO")

def prepare_search_index():
    logger.info("Preparing search index")

if __name__ == "__main__":
    logger.info("Starting worker")

    prepare_knowledge_base()
    
    prepare_search_index()


