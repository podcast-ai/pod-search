import torch
from transformers import AutoModel, AutoTokenizer


# This model is gonna to calculate the similarity score between the user input with the audio transcriptions.

tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/sup-simcse-bert-base-uncased")
model = AutoModel.from_pretrained("princeton-nlp/sup-simcse-bert-base-uncased")


def sentence_mapping(sentence):
    inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(
            **inputs, output_hidden_states=True, return_dict=True
        ).pooler_output
    return embeddings


def l2norm(x, dim=-1):
    return x / x.norm(2, dim=dim, keepdim=True).clamp(min=1e-6)


def similarity(inputs_repre, target_repre):
    return inputs_repre.mm(target_repre.t()).item()


def calc_score(query_text, target):
    """Calculate document similarity score between inputs and target."""
    if isinstance(target, str):
        target = [target]
        query_text = [query_text]

    assert len(target) == 1
    assert len(query_text) == 1
    inputs_repre = sentence_mapping(query_text)
    target_repre = sentence_mapping(target)

    score = similarity(l2norm(inputs_repre), l2norm(target_repre))

    return score
