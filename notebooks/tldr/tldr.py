
"""
first what i can do is break the transcript into certain sections and convert them into individial tldr and then combine them
(this method gives better results)
"""

from transformers import BartTokenizer, BartForConditionalGeneration
import argparse
import random

def generate_summary(model, tokenizer, article, min_length:int, max_length:int) -> str:
    inputs = tokenizer([article], max_length=1024, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], num_beams=20, min_length = min_length, max_length = max_length) 
    tldr = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return tldr

def parse(fn:str) -> tuple:
    article = open(fn,'r').read().strip().replace("\n"," ")
    ## ignore getting the names of speaker and the guest (if we have them)
    return (article)

def preprocess(article:tuple) -> list:
    sub_article = []
    sub = random.randint(5,10)
    section_len = len(article)//sub
    start,end = 0,section_len
    for i in range(sub):
        sub_article.append(article[start:end])
        start,end = end, end+section_len
        
    return sub_article

def main(fn) -> str:
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    article = parse(fn)
    sub_article = preprocess(article)
    summary  = ""
    for i in range(len(sub_article)):
        summary += generate_summary(model, tokenizer, sub_article[i], 0, 200)

    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter file name.')
    parser.add_argument('fn', metavar='file name', type=str, nargs='+',
                        help='File to convert into TLDR')
    args = parser.parse_args()
    summary = main(args.fn[0])
    print(summary)




