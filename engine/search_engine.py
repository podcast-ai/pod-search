from typing import List
from pandera.typing import DataFrame

# Used to import data from local.
import pandas as pd

# Used to create the dense document vectors.
import torch
from sentence_transformers import SentenceTransformer

# Used to create and store the Faiss index.
import faiss
import numpy as np
import pickle
from pathlib import Path
import numpy as np
from loguru import logger


import librosa

model = None
index = None
transcript_data = None
episode_data = None

# column names
transcription_col = "text"
episode_id_col = "episode_id"
paragraph_col = "paragraph_number"
id_col = "id"
chunk_start_col = "chunk_start"
chunk_end_col = "chunk_end"


def load_knowledge_base(knowlege_base_path):
    """loads knowledge base to a dataframe. ** Make sure the above mentioned columns are present in the dataframe"""
    # TODO - use the load knowledge base function from etl.py
    global transcript_data
    global episode_data

    knowledge_base_dir = knowlege_base_path
    transcript_data = pd.read_parquet(knowledge_base_dir + "/" + "transcript_data.parquet")
    episode_data = pd.read_parquet(knowledge_base_dir + "/" + "episode_data.parquet")
    assert not transcript_data.empty
    assert not episode_data.empty

    episode_data = episode_data.reset_index(level=0)

    transcript_data = transcript_data.reset_index(level=0)
    transcript_data = transcript_data.reset_index(level=0)
    transcript_data["id"] = transcript_data.index


def indexer(knowlege_base_path):
    """indexes transcripts and loads models"""
    logger.info(f"building the search index""")
    global model
    global index

    load_knowledge_base(knowlege_base_path)
    # Instantiate the sentence-level DistilBERT
    model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
    # Check if GPU is available and use it
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
    print(model.device)

    # Convert abstracts to vectors
    embeddings = model.encode(transcript_data[transcription_col].to_list(), show_progress_bar=True)
    print(f"Shape of the vectorised abstract: {embeddings.shape}")

    # Step 1: Change data type
    embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
    # Step 2: Instantiate the index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    # Step 3: Pass the index to IndexIDMap
    index = faiss.IndexIDMap(index)
    # Step 4: Add vectors and their IDs
    index.add_with_ids(embeddings, transcript_data[id_col].values)
    print(f"Number of vectors in the Faiss index: {index.ntotal}")
    return model, index, transcript_data, episode_data


def vector_search(query, model, index, num_results=10):
    """Tranforms query to vector using a pretrained, sentence-level
    DistilBERT model and finds similar vectors using FAISS.
    Args:
        query (str): User query that should be more than a sentence long.
        model (sentence_transformers.SentenceTransformer.SentenceTransformer)
        index (`numpy.ndarray`): FAISS index that needs to be deserialized.
        num_results (int): Number of results to return.
    Returns:
        D (:obj:`numpy.array` of `float`): Distance between results and query.
        I (:obj:`numpy.array` of `int`): Paper ID of the results.

    """
    vector = model.encode(list(query))
    D, I = index.search(np.array(vector).astype("float32"), k=num_results)
    return D, I


def id2details(df, I, column):
    """Returns the paper titles based on the paper index."""
    return [list(df[df.id == idx][column]) for idx in I[0]]


def flatten(l):
    return [x[0] for x in l]


def group_segments(episode_id, chunk_number, df):
    """return the start and end time of segement"""
    segmented_df = df[(df[episode_id_col] == episode_id) & (df['chunk_number'] == chunk_number)]
    start_time = segmented_df[chunk_start_col].values[0]
    end_time = segmented_df[chunk_end_col].values[0]
    return (start_time, end_time)

def get_segments(user_query,df,model,index):
    """returns the ranked matched segments from knowledge base"""
    segments = []
    D, I = vector_search([user_query], model, index, num_results=10)
    episode_id_matches = id2details(df, I, episode_id_col)
    #para_matches = id2details(df, I, paragraph_col)
    chunk_matches = id2details(df, I, 'chunk_number')
    
    matches = set(zip(flatten(episode_id_matches), flatten(chunk_matches)))
    for rank, match in enumerate(matches):
        filename = match[0]
        chunk = match[1]
        start_time, end_time = group_segments(filename, chunk,df)
        segments.append((rank, filename, start_time, end_time,chunk))
    return segments


#def save_segment

def get_proportion(start_time, file_name):

    duration = librosa.get_duration(filename=file_name)

    return start_time / duration


def get_json_segments(user_query, df, episode_df, model, index, limit: int = None):
    logger.info(f"querying: {user_query}")
    json_segments = []
    segments = get_segments(user_query, df, model, index)
    for rank, id, chunk_start, chunk_end, chunk_id in segments:
        json_seg = {}
        json_seg["id"] = id
        json_seg["fileName"] = '/static/data/podcasts/' + episode_df[episode_df[episode_id_col] == id][
            "file_name"
        ].values[0].replace(' ', '_') + '.mp3'
        json_seg["start_proportion"] = get_proportion(chunk_start, '/home/adrian.zuur/Desktop/podcast-ai-lab/app/' + json_seg['fileName'])
        json_seg["podcast_title"] = episode_df[episode_df[episode_id_col] == id][
            "title"
        ].values[0] #f"Podcast title, episode {id}"
        json_seg["podcast_url"] = episode_df[episode_df[episode_id_col] == id][
            "url"
        ].values[0] + f'&t={int(chunk_start)}' #f"https://www.podcast{id}.com"
        json_seg[
            "podcast_info"
        ] = f"This is info to print about the chunk or podcast. Chunk {chunk_id} is really interesting..."

        json_segments.append(json_seg)

    if limit:
        return json_segments[:limit]
    else:
        return json_segments

