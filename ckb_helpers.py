import re
from klpt.preprocess import Preprocess
from klpt.tokenize import Tokenize

import unicodedata

preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Arabic")
tokenizer_ckb = Tokenize("Sorani", "Arabic")


unify_numbers = {
    "٠|۰": "0",
    "١|۱": "1",
    "٢|۲": "2",
    "٣|۳": "3",
    "٤|۴": "4",
    "٥|۵": "5",
    "٦|۶": "6",
    "٧|۷": "7",
    "٨|۸": "8",
    "٩|۹": "9"
}

# Taken from AsoSoft library
def number_to_word(text):
    # convert numbers to latin
    for k, v in unify_numbers.items():
        text = re.sub(k, v, text)
    
    text = re.sub(r"([0-9]{1,3})[,،](?=[0-9]{3})", r"\1", text);  # remove thousend seperator  12,345,678 => 12345678
    text = re.sub(r"(?<![0-9])-([0-9]+)", r"ناقس \1", text);  # negative
    text = text.replace("٪", "%") # Replace arabic percent sign with latin
    text = re.sub(r"(?<![0-9])% ?([0-9]+)", r"لە سەددا \1", text);    # percent sign before
    text = re.sub(r"([0-9]+) ?%", r"\1 لە سەد", text);    # percent sign after
    text = re.sub(r"\$ ?([0-9]+(\.[0-9]+)?)", r"\1 دۆلار", text)    # $ querency 
    text = re.sub(r"£ ?([0-9]+(\.[0-9]+)?)", r"\1 پاوەن", text)  # £ querency 
    text = re.sub(r"€ ?([0-9]+(\.[0-9]+)?)", r"\1 یۆرۆ", text)   # € querency 

    # convert float numbers
    text = re.sub(r"([0-9]+)\.([0-9]+)", lambda x: float_name(x.group(1), x.group(2)), text)

    # convert remaining integr numbers
    text = re.sub(r"([0-9]+)", lambda match: integer_name(match.group(1)), text)

    return text

def float_name(integerPart, decimalPart):
    zeros = re.search("^0+", decimalPart)
    point = " پۆینت " 
    if(zeros):
        point = point + re.sub("0", " سفر ", zeros[0])
    return integer_name(integerPart) + point + integer_name(decimalPart)

ones = ["", "یەک", "دوو", "سێ", "چوار", "پێنج", "شەش", "حەوت", "هەشت", "نۆ"]
teens = [ "دە", "یازدە", "دوازدە", "سێزدە", "چواردە", "پازدە", "شازدە", "حەڤدە", "هەژدە", "نۆزدە" ]
tens = [ "", "", "بیست", "سی", "چل", "پەنجا", "شەست", "هەفتا", "هەشتا", "نەوەد"]
hundreds = ["", "سەد", "دووسەد", "سێسەد", "چوارسەد", "پێنسەد", "شەشسەد", "حەوتسەد", "هەشتسەد", "نۆسەد"]
thousands = ["", " هەزار", " ملیۆن", " ملیار", " ترلیۆن", " کوادرلیۆن", " کوینتلیۆن"]

def integer_name(inputInteger):
    output = ""
    if (inputInteger != "0"):
        temp = inputInteger
        for i in range(0, len(inputInteger), 3):
            matched_numbers = re.findall(r"[0-9]{1,3}$", temp)
            currentThree = matched_numbers[0] if matched_numbers else ""

            temp = temp[:len(temp) - len(currentThree)]
            currentThree = currentThree.rjust(3, '0')
            C = int(currentThree[0])
            X = int(currentThree[1])
            I = int(currentThree[2])
            conjunction1 = " و " if (C != 0) and (X != 0 or I != 0) else ""
            conjunction2 = " و " if X != 0 and I != 0 else ""

            if (X == 1):
                currentThree = hundreds[C] + conjunction1 + teens[I]
            else:
                currentThree = hundreds[C] + conjunction1 + tens[X] + conjunction2 + ones[I]
            
            currentThree += "" if currentThree == "" else thousands[i // 3]

            conjunction3 = "" if output == "" else " و "
            if (currentThree != ""):
                output = currentThree + conjunction3 + output
        output = output.replace("یەک هەزار", "هەزار")
    else: # if input number = 0
        output = "سفر"
    return output




def replace_words_in_corpus(sentence):
    modified_corpus = []

    words = sentence.split()
    modified_words = []

    for word in words:
        if word in word_replacements:
            modified_words.append(word_replacements[word])
        else:
            modified_words.append(word)

    modified_sentence = " ".join(modified_words)

    return modified_sentence

# put this in a json file
word_replacements = {
    "ههڵاڵەەي": "هەڵاڵەی",
    "وهەمهەمه": "وهەمهەمه",
    "ئهباتههوه": "ئەباتەوە",
    "بەخءرایی": "بەخێرایی",
    "ئیثانۆڵ": "ئیسانۆڵ",
    "عەبدوڵڵاهـ": "عەبدوڵڵا",
    "کولاهـ": "کولاه",
    "ئاھ": "ئاه",
}


char_replacements = {
    '\u200e': '',
    '\u200f': '',
    '\u200c': '',
    'õ': '',
    'ھ': 'ه'
}
def apply_char_replacements(text: str):
    
    for old, new in char_replacements.items():
        text = text.replace(old, new)
    return text


def remove_arabic_alphabets(text: str):
    """
    Removes ``Arabic`` words and digits from a ``text``

    Args:
         text (str): Sorani text
    Returns:
        str: ``str`` object with arabic alphabets removed
    """
    characters = "ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱ"
    table = str.maketrans({key: None for key in characters})
    return text.translate(table)



def filtered_arabic_characters():
    kurdish_characters = set("ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ")
    arabic_characters = set("ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱ")

    # Create a new set of Arabic characters without the Kurdish characters
    filtered_arabic_characters = arabic_characters - kurdish_characters

    return ''.join(filtered_arabic_characters)



def is_arabic_string(text):
    """Returns True if the text contains any Arabic characters, False otherwise."""
    # arabic_characters = set("ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْٰٱ")
    arabic_characters = filtered_arabic_characters()
    for ch in text:
        if ch in arabic_characters:
            return True
    return False

def contains_arabic(text):
    arabic_characters = filtered_arabic_characters()
    return any(char in arabic_characters for char in text)


def is_english_string(text):
    """Returns True if the text contains only English characters, False otherwise."""
    english_pattern = re.compile(r'[a-zA-Z]')
    return bool(english_pattern.search(text))


def remove_english_alphabets(text: str):
    """
    Removes ``English`` words and digits from a ``text``
    """
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    table = str.maketrans({key: None for key in characters})
    return text.translate(table)




def resolve_ae(text):
    """
    This function takes a text input in Central Kurdish (Sorani) script and performs a series of character replacements
    to standardize variations in the script. Specifically, it addresses cases where the character 'ە' (Arabic letter
    AE) may be used in different contexts.
    """
    # First replace all occurrences of 'ه' with 'ە'
    text = re.sub("ه", "ە", text)
    # Replace specific combinations with 'ها', 'هێ', and 'ه'
    text = re.sub("ەا", "ها", text)  # Replace ەا with ها
    text = re.sub("ەێ", "هێ", text)  # Replace ەێ with هێ
    text = re.sub("ەۆ", "هۆ", text)  # Replace ەۆ with هۆ

    # Replace ە (AE) at the beginning of a word with ه (HEH)
    text = re.sub(r"\b(ە\w*)", lambda match: "ه" + match.group(1)[1:], text)

    #  Replace ALEF+AE with ALEF+HEH
    text = re.sub("اە", "اه", text)

    # Special words should go here before the replcement of 'ە' at the end of the word
    # Special case: گەهـ or گاهـ but without the tatweel since tatweel is not a phoneme in Kurdish and it will be a class for the model
    text = re.sub(r'\bگەە[-ـ]?\b', "گەه", text)
 
    # Replace 'ەە' at the beginning and end with 'هە'
    text = re.sub(r"\bەە|ەە\b", "هە", text)

    # Special case if two AEs come before ۆ it should be replaced with AE+HEH
    text = re.sub(r"ەە(?=ۆ)", "ەه", text)

    # Special case if two AEs come after either و or ب or ئ or ڕ or ق or ز they should be replaced with AE+HEH
    text = re.sub(r"(?<=\b[بوئڕقزژ])ەە", "ەه", text)
    # The following special case should happen after the previous special case and before the following speciall case
    # Special case when two words are together with waw and the the AEs after the waw becomes HEH+AE
    text = re.sub(r'(?<=و)ەە(?=\w)', "هە", text)

    # Replace Three AEs with AE+HEH+AE (This has to be run before the following special case so words like لەهەوادا will not be ruined)
    text = re.sub(r"(?<=\w)ەەە(?=\w)", "ەهە", text)

    # Special case if two AEs are in the middle of a word and come before YEH ی or TCHEH چ or و they will be replaced with AE+HEH if  the YEH or TCHEH are not at the END of the word
    text = re.sub(r"(?<=\w)ەە(?=[چیو]\B)", "ەه", text)    

    # Replace 'ەە'AE+AE in the middle of a word with HEH+AE
    text = re.sub(r"(?<=\w)ەە(?=\w)", "هە", text)

    # Replace two AE with spaces in between with AE HEH
    text = re.sub("ە ە", "ە ه", text)

    # Replace all HEH DOACHASHMEE with HEH
    # text = text.replace('ھ', 'ە')
    return text

clean_punctuation = re.compile(r"(?<!\d)[.,;:'?!\/](?!\d)")
def remove_punctuation(text):
    """Remove all punctuation from string, except if it's between digits"""
    return clean_punctuation.sub("", text)


def extract_punctuation(text):
    # Initialize an empty string to store the extracted punctuation
    extracted_punctuation = ""
    
    # Iterate through each character in the input text
    for char in text:
        # Check if the character is categorized as punctuation
        if unicodedata.category(char).startswith('P'):
            extracted_punctuation += char  # Add it to the result
    
    return set(extracted_punctuation)



ARABIC_PUCTUATIONS = "،؛۔٫٪؟"
CKB_PUNCTUATIONS = "!.:;?،؛؟«»"  + ARABIC_PUCTUATIONS
KURDISH_CHARS = set(f"{CKB_PUNCTUATIONS}ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ٠١٢٣٤٥٦٧٨٩ ")

def contains_non_kurdish_characters(text):
    # kurdish_characters = set("ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ٠١٢٣٤٥٦٧٨٩ ")
    kurdish_characters = set(f"{CKB_PUNCTUATIONS}ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ٠١٢٣٤٥٦٧٨٩ ")
    non_kurdish_chars = set(text) - kurdish_characters
    
    return len(non_kurdish_chars) > 0


def keep_kurdish_characters(text):
    kurdish_characters = set(f"{CKB_PUNCTUATIONS}ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ٠١٢٣٤٥٦٧٨٩ ")

    cleaned_text = ''.join(char for char in text if char in kurdish_characters)
    return cleaned_text



def remove_emojis(text):
    emoji_pattern = re.compile("["
                               "\U0001F600-\U0001F64F"  # Emoticons
                               "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                               "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                               "\U0001F700-\U0001F77F"  # Alchemical Symbols
                               "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               "\U0001FA00-\U0001FA6F"  # Chess Symbols
                               "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               "\U00002702-\U000027B0"  # Dingbats
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_language_families(text):
    patterns = [
        "[\u1100-\u11FF\u2E80-\u4DBF\u4E00-\u9FFF\uAC00-\uD7AF]+",  # Asian scripts
        "[\u0000-\u024F]+",  # Basic Latin and Latin-1 Supplement
        "[\u0400-\u04FF]+",  # Cyrillic
        "[\u0370-\u03FF]+",  # Greek
        "[\u0900-\u097F]+",  # Devanagari
        r"\u0B80-\u0BFF",  # Tamil
        r"\u4E00-\u9FFF",  # Han
        r"\u10A0-\u10FF",  # Georgian
        r"\u0C80-\u0CFF"   # Kannada
    ]

    combined_pattern = re.compile("|".join(patterns))

    cleaned_text = combined_pattern.sub(r'', text)
    return cleaned_text


clean_punctuation = re.compile(r"(?<!\d)[.,;:'?!،.؟؛:](?!\d)")
def remove_punctuation(text):
    """Remove all punctuation from string, except if it's between digits"""
    return clean_punctuation.sub("", text)

def contains_repeated_ngram(window, n):
    ngrams = generate_ngrams(window, n)
    ngram_set = set(ngrams)
    return len(ngrams) != len(ngram_set)


def generate_ngrams(text, n):
     words = text.split()
     output = []  
     for i in range(len(words)- n+1):
         output.append(tuple(words[i:i+n]))
     return output

def remove_repeated_ngram(text, n):
    words = text.split()
    output = []  
    for i in range(len(words)- n+1):
        if not contains_repeated_ngram(" ".join(words[i:i+n]), n):
            output.append(words[i])
    return " ".join(output)

def normalize_punctuations(text: str) -> str:
    # Replace , with ،    
    text = text.replace(',', '،')
    # Replace ? with ؟
    text = text.replace('?', '؟')
    # Replace two or three of the same punctuation marks with a single one
    text = re.sub(r'([.,;:?!،؛؟])\1{1,2}', r'\1', text)

    
    # Replace double opening and closing parentheses with guillemets
    text = re.sub(r'\(\(', '«', text)
    text = re.sub(r'\)\)', '»', text)
    
    # Normalize space around the guillemets and other punctuation marks
    text = re.sub(r'\s*«\s*', ' «', text)
    text = re.sub(r'\s*»\s*', '» ', text)
    
    # Additional punctuation normalization
    text = re.sub(r'\s*([,،؟])\s*', r'\1 ', text)
    
    # Ensure there is no space before a guillemet at the beginning of the text or after a
    # guillemet at the end of the text
    text = re.sub(r'^\s*«', '«', text)
    text = re.sub(r'»\s*$', '»', text)
    
    # If multiple punctuation marks come after each other only keep the first one
    # text = re.sub(r'([.!?؟،؛])\1+', r'\1', text)

    # if conective punctuation marks come after each other only keep the first one
    text = re.sub(r'([.!?؟،؛])\1+', r'\1', text)

    # if punctuation marks come after each other with space between them like: ? ? ? keep the first one remove the rest
    text = re.sub(r'([.!?؟،؛])\s\1+', r'\1', text)
    # Trim leading and trailing spaces and return the normalized text
    text = text.strip()
    return text


def fix_sentence(sentence):
  
    if sentence.startswith('"') and sentence.endswith('"'):
        # we can remove trailing quotation marks as they do not affect the sentence
        sentence = sentence[1:-1]
  
    if sentence[-1] not in [".", "?", "!"]:
        # append a full-stop to sentences that do not end in punctuation
        sentence = sentence + "."
    # sentence = sentence[:-1].translate(str.maketrans('', '', string.punctuation)) + sentence[-1]
    return sentence


def add_period_abbreviations(text):

    abbreviations = set(["پ", "د"])  # Add more abbreviations as needed

    # Define a regular expression pattern to match a letter followed by a space and then a word character
    pattern = re.compile(r'([{}]) (?=\w)'.format(''.join(abbreviations)))

    # Use regex to add periods after the specified abbreviations with a space after the period
    text = pattern.sub(r'\1. ', text)

    # Add periods after each letter if "د" and "خ" appear together
    text = re.sub(r'د\sخ|خ ?د|د\.?خ|خ\.?د', 'د. خ.', text)
    
    # Abbreviated dates
    # text = re.sub(r'\b(پ\. ز)\b', r'\1.', text)
    
    return text


def process_text(text):
    # text = replace_words_in_corpus(text)
    text = resolve_ae(text)
    # text = number_to_word(text)
    text = preprocessor_ckb.preprocess(text)
    # text = normalizer(text).strip()
    text = remove_emojis(text)
    text = normalize_punctuations(text)
    text = fix_sentence(text)
    text = apply_char_replacements(text)
    return text

if __name__ == "__main__":
    # text = "لە ساڵی 1999دا بڕی 40% لە پارەکەیان واتە $102.1 یان وەرگرت. 'õ'\u200c\u200f\u200e'ھ'"

    # print(process_text(text))
    # print(contains_non_kurdish_characters(text))
    # text = "دەقی«کوردی » و ڕێنووس ،((خاڵبەندی )) چۆنە ؟"
    # correct = "دەقی «کوردی» و ڕێنووس، «خاڵبەندی» چۆنە؟"
    # print("Before punctuation normalization:", text)
    # print("After punctuation normalization:", normalize_punctuations(text))
    # print("Correct:\t\t\t", correct)
    # print(normalize_punctuations(text) == correct)
    # print(normalize_punctuations("ڕەوا بورهان 4 تەمموز ، کوردستانی سلێمانی?!!"))
    # print(normalize_punctuations("یانەی کوردژین   تکایە  چۆن بە شی سە ڕە کی و لاوە کی بۆ مالپە ڕە کە م زیاد بکە م؟؟ ؟ ؟ لە  سکرێپە یتی ژومیلە"))
    # with open('data/data.ckb.txt', 'r', encoding='utf-8') as src_file:
    #     source_data = src_file.read()

    # unified_data = normalize_punctuations(source_data)

    # # Save the unified data to a new file
    # with open('data/unified_data.txt', 'w', encoding='utf-8') as file:
    #     file.writelines(unified_data)

    # print("Unified data saved to unified_data.txt")

    text = "Hello ((Friend)) Hello ,  Friend World"
    # print(remove_repeated_ngram(text, 2))
    # print(remove_repeated_ngrams(text, ))
    print(process_text(text))