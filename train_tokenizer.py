from datasets import load_dataset
from transformers import AutoTokenizer
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--tokenizer_name", default="facebook/bart-base", help="The name of the tokenizer to train a new one from")
parser.add_argument("--output_dir", default="tokenizer", type=str, help="Repo id the tokenizer to be pushed to")
parser.add_argument("--push_to_hub", default=False, action="store_true", help="Push to hub",)

args = parser.parse_args()


dataset = load_dataset("oscar-corpus/OSCAR-2301", "ckb", split="train", token=True)

def get_training_corpus(batch_size=1000):
    for start_idx in range(0, len(dataset), batch_size):
        samples = dataset[start_idx : start_idx + batch_size]
        yield samples["text"]

training_corpus = get_training_corpus()

tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)

tokenizer = tokenizer.train_new_from_iterator(
    training_corpus, vocab_size=len(tokenizer),
    special_tokens_map={
        "eos_token": "</s>",
        "bos_token": "<s>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
    },
)


tokenizer.save_pretrained(args.output_dir, push_to_hub=args.push_to_hub)

