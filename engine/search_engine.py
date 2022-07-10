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

model = None
index = None
df = None

# column names
transcription_col = "text"
episode_id_col = "episode_id"
paragraph_col = "paragraph_number"
id_col = "id"
chunk_start_col = "chunk_start"
chunk_end_col = "chunk_end"


def load_knowledge_base(knowlege_base_path):
    """loads knowledge base to a dataframe. ** Make sure the above mentioned columns are present in the dataframe"""
    global df
    df = pd.read_parquet(knowlege_base_path, engine="pyarrow")
    df = df.reset_index(level=0)
    df = df.reset_index(level=0)
    df["id"] = df.index
    print("knowledge base loaded")


def indexer(knowlege_base_path):
    """indexes transcripts and loads models"""
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
    embeddings = model.encode(df[transcription_col].to_list(), show_progress_bar=True)
    print(f"Shape of the vectorised abstract: {embeddings.shape}")

    # Step 1: Change data type
    embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
    # Step 2: Instantiate the index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    # Step 3: Pass the index to IndexIDMap
    index = faiss.IndexIDMap(index)
    # Step 4: Add vectors and their IDs
    index.add_with_ids(embeddings, df[id_col].values)
    print(f"Number of vectors in the Faiss index: {index.ntotal}")


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


def group_segments(episode_id, para):
    """return the start and end time of segement"""
    segmented_df = df[(df[episode_id_col] == episode_id) & (df[paragraph_col] == para)]
    start_time = segmented_df[chunk_start_col].min()
    end_time = segmented_df[chunk_end_col].max()
    return (start_time, end_time)


def get_segments(user_query):
    """returns the ranked matched segments from knowledge base"""
    segments = []
    D, I = vector_search([user_query], model, index, num_results=10)

    episode_id_matches = id2details(df, I, episode_id_col)
    para_matches = id2details(df, I, paragraph_col)
    matches = set(zip(flatten(episode_id_matches), flatten(para_matches)))
    for rank, match in enumerate(matches):
        filename = match[0]
        para = match[1]
        start_time, end_time = group_segments(filename, para)
        segments.append((rank, filename, start_time, end_time))
    return segments
