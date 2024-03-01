import random 
from string import punctuation
import re
import os
from transformers import AutoTokenizer
from tqdm import tqdm
from typing import List
from constants import KURDISH_CHARS, KEYBOARD_BLANK, KEYBOARD_KEYS, NUMBERS


def tokenizer_check_if_text_too_long(text, tokenizer, max_length):
    data = tokenizer.batch_encode_plus([text],max_length=max_length,truncation=True,return_overflowing_tokens=True )    
    if len(data["input_ids"]) > 1:
        return True
    else:
        return False#, len(data["input_ids"][0])

def delete_characters(text, char_delete_percentage=0.01):
    modifyed_line = []   
    for char in text:
        if random.random() > char_delete_percentage or char in NUMBERS:
            modifyed_line.append(char)
    return "".join(modifyed_line)

def insert_characters(text, augmentation_probability=0.01):
    modifyed_line = []   
    for char in text:
        if random.random() <= augmentation_probability and char not in NUMBERS:            
            modifyed_line.append(random.choice(KURDISH_CHARS))
        modifyed_line.append(char)
    return "".join(modifyed_line)

def replace_characters(text, augmentation_probability=0.01):
    modifyed_line = []   
    for char in text:
        if random.random() <= augmentation_probability and char not in NUMBERS:            
            modifyed_line.append(random.choice(KURDISH_CHARS))
        else:
            modifyed_line.append(char)
    return "".join(modifyed_line)

def random_neighbor_replace(line: str, keyboard_rows: List[str], blank: str) -> str:
    lines = keyboard_rows
    n_rows = len(keyboard_rows)
    _mapper = {}

    def __get_left(row_idx: int, col_idx: int) -> List[str]:
        if col_idx == 0:
            return []
        return [lines[row_idx][col_idx - 1]]

    def __get_right(row_idx: int, col_idx: int) -> List[str]:
        if col_idx == (len(lines[row_idx]) - 1):
            return []
        return lines[row_idx][col_idx + 1]

    def __get_upper(row_idx: int, col_idx: int) -> List[str]:
        if row_idx == 0:
            return []
        line = lines[row_idx - 1]
        start = max(0, col_idx - 1)
        end = min(len(line), col_idx + 2)
        return list(line[start: end])

    def __get_lower(row_idx: int, col_idx: int) -> List[str]:
        if row_idx == (n_rows - 1):
            return []
        line = lines[row_idx + 1]
        start = max(0, col_idx - 1)
        end = min(len(line), col_idx + 2)
        return list(line[start: end])

    funcs = [__get_left, __get_right, __get_upper, __get_lower]
    for row_idx in range(n_rows):
        for col_idx in range(len(lines[row_idx])):
            items = []
            for func in funcs:
                items.extend(func(row_idx, col_idx))
            items = list(filter(lambda x: x != blank, items))
            char = lines[row_idx][col_idx]
            _mapper[char] = items.copy()

    def get_char(char: str) -> str:
        if char not in _mapper:
            return char
        return random.choice(_mapper[char])

    length = len(line)
    if length == 0:
        length = 1
    idx = random.randint(0, length - 1)
    return line[:idx] + get_char(line[idx]) + line[idx + 1:]
def lower_case_words(text, augmentation_probability=0.5):
    modifyed_line = []   
    for word in text.split():
        if word[0].islower() == False and random.random() <= augmentation_probability:            
            word = word.lower()
        modifyed_line.append(word)
    return " ".join(modifyed_line)


clean_chars = re.compile(r'[^A-Za-zöäüÖÄÜß,.!?’\'$%€0-9\(\)\- ]', re.MULTILINE)
def cleanup(text):    
    text = clean_chars.sub('', text)
    #print("bug: somehow all numbers are removed - this is might be due to this regex")
    #exit()
    #text = text.replace("\n", "")
    #text = text.replace('"','\\"')
    return text

clean_punctuation = re.compile(r"(?<!\d)[.,;:'?؟.!()؟،»«](?!\d)")
def remove_punctuation(text):
    """Remove all punctuation from string, except if it's between NUMBERS"""
    return clean_punctuation.sub("", text)

def combine_sentences(text, sentences, augmentation_probability = 1):
    if random.random() < augmentation_probability:
        sentences_to_sample = random.randint(0,10)
        augmentation_sentences = random.sample(sentences,sentences_to_sample)    
        return text + " " + " ".join(augmentation_sentences)
    else:
        return text

def delete_word(text, augmentation_probability = 0.001):        
    if random.random() < augmentation_probability:
        words = text.split()
        if len(words) < 3:
            # do not delete word in short text, as there will be no context to guess the word
            return text
        word_to_remove = random.randint(0,len(words)-1)
        words.pop(word_to_remove)
        return " ".join(words)
    else:
        return text


if __name__ == "__main__":
    data_file = "data/data.txt" #"data/en.wikidump.processed.24m.txt" #
    language = "ckb" # "wikidump.24m.en"
    num_lines = sum(1 for line in open(data_file,'r'))
    print("Number of lines:",num_lines)
    with open(data_file,'r') as file:
        sentences = file.readlines(int(num_lines*0.5))
        # sentences = [cleanup(sentence) for sentence in sentences]
        
    # tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
    tokenizer = AutoTokenizer.from_pretrained("./tokenizer")
    with open(language+".csv","w",encoding='utf-8') as output:        
        with open(data_file,'r') as file:
            for line in tqdm(file, total=num_lines):
                # line = cleanup(line)
                if len(line) < 1:
                    continue 
                line = combine_sentences(line,sentences)                
                if tokenizer_check_if_text_too_long(line,tokenizer,max_length=1024):
                    print(f"skipping line as its too long ({len(line)}):\n"+line)
                    continue
                
                if random.random() >0.02:
                    # we will leave 2% of the data untouched, to teach the 
                    # model, not to "overact" on the texts
                    new_line = delete_word(line)
                    new_line = delete_characters(new_line)
                    new_line = insert_characters(new_line)
                    new_line = replace_characters(new_line)  
                    new_line = random_neighbor_replace(new_line, KEYBOARD_KEYS, KEYBOARD_BLANK)                                     
                    new_line = remove_punctuation(new_line)
                else:
                    new_line = line
                output.write(f'"{new_line.strip()}","{line.strip()}"\n')        
    os.system(f"echo \"text,summary\" > {language}.train.csv")
    num_lines = sum(1 for line in open(f"{language}.csv",'r'))
    os.system(f"head -n {num_lines-2000} {language}.csv >> {language}.train.csv")
    os.system(f"echo \"text,summary\" > {language}.test.csv")
    os.system(f"tail -n 2000 {language}.csv >> {language}.test.csv")



