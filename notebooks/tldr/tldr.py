
"""
break the transcript into certain sections and convert them into individial tldr and then combine them
(this method gives better results)
"""

from transformers import BartTokenizer, BartForConditionalGeneration
import argparse
import random
import numpy as np
import pandas as pd
from tqdm import trange

def generate_summary(model, tokenizer, article, min_length:int, max_length:int) -> str:
    inputs = tokenizer([article], max_length=1024, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], num_beams=20, min_length = min_length, max_length = max_length) 
    tldr = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return tldr

def parse(fn:str) -> np.array:
    #article = open(fn,'r').read().strip().replace("\n"," ")
    _,form = fn.split(".")
    if form == "csv":
        df = pd.read_csv(fn)
        article = np.array(df.transcription)
    if form == "json":
        df = pd.read_json(fn)
        article = np.array(df.text)

    ## ignore getting the names of speaker and the guest (if we have them)
    return article

def preprocess(article:np.array) -> list:
    sub_article = []
    sub = len(article)//8
    section_len = sub
    start,end = 0,section_len
    while end < len(article):
        sub_article.append(" ".join(article[start:end]))
        start,end = end, end+section_len
        
    return sub_article

def main(fn) -> str:
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    article = parse(fn)
    sub_article = preprocess(article)
    summary  = ""
    for i in (w := trange(len(sub_article))):
        summary += generate_summary(model, tokenizer, sub_article[i], 16, 256)
        w.set_description(f"generating summary for subgroup : {i}")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter file name.')
    parser.add_argument('fn', metavar='file name', type=str, nargs='+',
                        help='File to convert into TLDR')
    args = parser.parse_args()
    summary = main(args.fn[0])
    print(summary)




