import pandas as pd
from tqdm import tqdm
from ckb_helpers import *
df = pd.read_csv('data/asotest.csv')

data_df = pd.read_csv('data/data.txt', names=['text']) 
train_df = pd.read_csv('train.csv')


data = []
pbar = tqdm(df.itertuples(), total=len(df))

for row in pbar:
    incorrect_word = row.text
    correct_word = row.summary
    
    # look up sentences from data_df that contain correct_word and make only keep those rows that are not  in train_df
    sentences = data_df[data_df['text'].str.contains(correct_word, case=False, na=False)]
    sentences = sentences[~sentences.text.isin(train_df.summary)]
    
    pbar.set_description(f"Rows found after cross checking train data: {len(sentences)} for {correct_word}")
    for r in sentences.head(1).itertuples():
        new_sentence = r.text.replace(correct_word, incorrect_word)
        data.append({"text": new_sentence, "summary": process_text(r.text)})
        # drop that row so the final dataset doesn't include same sentence for two incorrect words
        data_df.drop(index=r.Index, axis=0, inplace=True)



df = pd.DataFrame(data)
df.to_csv('asosoft_spell.csv', index=False)
