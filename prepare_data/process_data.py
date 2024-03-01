from argparse import ArgumentParser
import os
import re
import time
from processors import FilesProcessor, get_text_distorter
from processes import (
    CharsRemover,
    LengthFilter,
    LinesSplitter,
    LoadFile,
    NumbersFilter,
    OOVFilter,
    RepeatedCharsCollapsor,
    # SoloCharFilter,
    SpacesRemover,
    ValidCharsKeeper,
    WordsFilter,
    WordsNumberFilter,
    CharsNormalizer,
    TokenizerLengthFilter,
    )
from helpers import load_json, save_text_file
from typing import Union, List
from pathlib import Path
import constants
import pandas as pd


def get_paths(
        main_dir: Union[Path, str]
        ) -> List[Union[Path, str]]:
    paths = [
        os.path.join(main_dir, file)
        for file in os.listdir(main_dir)
        ]
    return paths

def get_path(
        file_path: Union[Path, str]
        ) -> List[Union[Path, str]]:
    if os.path.isfile(file_path):
        return [file_path]
    else:
        raise FileNotFoundError


def get_file_processor(args):
    words = load_json(args.execlude_words_files)
    processes = [
        LoadFile(),
        *[LinesSplitter(sep=sep) for sep in args.sep],
        RepeatedCharsCollapsor(args.max_rep_chars),
        NumbersFilter(),
        # SoloCharFilter(),
        WordsFilter(words),
        ValidCharsKeeper(constants.VALID_CHARS),
        SpacesRemover(),
        WordsNumberFilter(args.min_words, args.max_words),
        # TokenizerLengthFilter(),
        LengthFilter(args.min_len, args.max_len)
    ]
    return FilesProcessor(processes)


def post_process(data: List[str]) -> List[str]:
    lines = []
    for item in data:
        lines.extend(item)
    lines = list(set(lines))
    # lines = OOVFilter(args.max_oov).execute(lines)
    return lines


clean_punctuation = re.compile(r"(?<!\d)[!.:;?،؛؟«» ،؛۔٫٪؟](?!\d)")

def remove_punctuation(text):
    """Remove all punctuation from string, except if it's between digits"""
    return clean_punctuation.sub("", text)



def get_argparser():
    parser = ArgumentParser()
    parser.add_argument(
        '--sep', default=[
            '\n',
            #   '\t', '.', '،', ',', '=', ':', '-', '\\', '/'
            ], nargs='+', type=str,
        help='The seperator to be used to split the lines on'
        )
    parser.add_argument(
        '--min_len', default=5, type=int,
        help='The minimum line length to keep'
        )
    parser.add_argument(
        '--max_len', default=1020, type=int,
        help='The maximum line length to keep'
        )
    parser.add_argument(
        '--dist_run', default=False, action='store_true'
    )
    parser.add_argument(
        '--data_path', default='data/data.txt'
    )
    parser.add_argument(
        '--save_path', default='data/clean_data.txt'
    )
    parser.add_argument(
        '--max_rep_chars', default=2
    )
    parser.add_argument(
        '--execlude_words_files', default='data/words.json'
    )
    parser.add_argument(
        '--max_oov', default=100, type=int
    )
    parser.add_argument(
        '--min_words', default=3, type=int
    )
    parser.add_argument(
        '--max_words', default=100, type=int
    )
    parser.add_argument(
        '--dist_ratios', default=[0.05, 0.1, 0.15]
    )
    parser.add_argument(
        '--remove_punc', default=False, action='store_true', help='Remove punctuation of the distorted lines'
    )
    return parser


def main(args) -> None:
    fp = get_file_processor(args)
    files = get_path(args.data_path)
    print('Started!')
    start = time.time()
    if args.dist_run is True:
        print('dist run')
        data = fp.dist_run(files)
    else:
        data = fp.run(files)
    end = time.time()
    print(f'Files Processing completed in {end - start}')
    data = post_process(data)
    sentences = data[: len(data) // 2]
    print("Length of data after post processing", len(data))
    df = None
    for i, ratio in enumerate(args.dist_ratios):
        distorter = get_text_distorter(ratio, sentences)
        # TODO: Don't touch 2 percent of sentences to keep the model from having a high bias towards the noise

        dist = list(map(distorter.run, data))
        if df is None:
            df = pd.DataFrame({
                'clean': data,
                f'distorted_{ratio}': dist
            })
        else:
            df[f'distorted_{ratio}'] = dist
    if args.remove_punc is True:
        print("Removing punctuations for the distorted lines")
        for ratio in args.dist_ratios:
            df[f'distorted_{ratio}'] = df[f'distorted_{ratio}'].apply(
                remove_punctuation
            )
    df.to_csv(f'data/data.csv', encoding='utf-8')
    # save_text_file(args.save_path, '\n'.join(data))


if __name__ == '__main__':
    parser = get_argparser()
    args = parser.parse_args()
    main(args)
    num_lines = sum(1 for line in open(f"data/data.csv",'r'))
    os.system(f"echo \"text,summary\" > train.csv")
    # # Only change the first $ variable for different distortion ratios
    # os.system(f"awk -F',' 'NR>1 && NR<={num_lines-50000} {{print $4 \",\" $2}}' data/data.csv >> train.csv")
    # os.system(f"awk -F',' 'NR>1 && NR<={num_lines-50000} {{print $3 \",\" $2}}' data/data.csv >> train.csv")
    os.system(f"awk -F',' 'NR>1 && NR<={num_lines-50000} {{print $5 \",\" $2}}' data/data.csv | sed 's/\"//g' >> train.csv")
    os.system(f"awk -F',' 'NR>1 && NR<={num_lines-50000} {{print $4 \",\" $2}}' data/data.csv | sed 's/\"//g' >> train.csv")
    os.system(f"awk -F',' 'NR>1 && NR<={num_lines-50000} {{print $3 \",\" $2}}' data/data.csv | sed 's/\"//g' >> train.csv")

    os.system(f"echo \"text,summary\" > test.csv")
    # os.system(f"tail -n 50000 data/data.csv | awk -F',' '{{print $4 \",\" $2}}' >> test.csv")
    # os.system(f"tail -n 50000 data/data.csv | awk -F',' '{{print $3 \",\" $2}}' >> test.csv")
    os.system(f"awk -F',' 'NR>{num_lines-50000} {{print $5 \",\" $2}}' data/data.csv | sed 's/\"//g' >> test.csv")
    os.system(f"awk -F',' 'NR>{num_lines-50000} {{print $4 \",\" $2}}' data/data.csv | sed 's/\"//g' >> test.csv")
    os.system(f"awk -F',' 'NR>{num_lines-50000} {{print $3 \",\" $2}}' data/data.csv | sed 's/\"//g' >> test.csv")





