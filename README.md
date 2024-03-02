# Central Kurdish Neural Spell Corrector 
<p align="center">
    <img src="https://www.razhan.ai/_next/image?url=/static/images/projects/spell-checker.webp&w=1200&q=75" alt="Banner Image" height="240" width="1200">
    <br>
    <a href="https://huggingface.co/razhan/bart-kurd-spell-base">
        [🔥 Best model] 
    </a>
    <a href="https://huggingface.co/models?search=bart-kurd-spell">
        [📀 Models] 
    </a>
    <a href="https://huggingface.co/spaces/razhan/Kurd-Spell">
      [🤗 Demo]
    </a>
</p>
    



> **Note:** The documentation for this project is currently being written. I am working hard to make this project easily hackable so people can add new heuristics and train more models.

This repository contains a collection of neural spell correctors for the Central Kurdish language.These models have been trained on an extensive corpus of synthetically generated data. They are able to correct a wide range of spelling errors, including typos and grammatical errors.


Using various heuristics, we generate a rich dataset by mapping sequences containing misspellings to the correct sequence. We do this by randomly inserting valid characters, deleting characters or patterns, substituting characters with random ones or their keyboard neighbors, swapping two adjacent characters, shuffling sentences, and replacing specific predefined patterns with targeted alternatives. 



## Experiments
The error injection framework in `prepare_data` offers a method to inject errors according to a distortion ratio. I conducted the following experiments to determine the optimal ratio that allows the model to achieve the lowest Word Error Rate (WER) and Character Error Rate (CER) on the synthetic test set.
| Model Name                                                       | Dataset Distortion| CER   | WER    |
|------------------------------------------------------------------|-------------------|-------|--------|
| [bart-base](razhan/bart-kurd-spell-base-05)                      | 5%                | 5.39% | 34.73% |
| [bart-base](razhan/bart-kurd-spell-base-05)                      | 10%               | 2.15% | 11.19% |
| [bart-base](https://huggingface.co/razhan/bart-kurd-spell-base-05_10)| Mixed (5% + 10%)| **1.54%** | **8.31%** |
| [bart-base](https://huggingface.co/razhan/bart-kurd-spell-base)  |  15%               | 2.17% | 12.3% |


## Evaluation on ASOSOFT Spelling Benchmark
The benchmark for this [project](https://github.com/AsoSoft/Central-Kurdish-Spelling-dataset) is exclusively designed for single-word spelling corrections. The script `create_asosoft_benchmark.py` processes each word from the Amani dataset by searching for sentences with the correct spelling, checking if the sentence has not been included in `train.csv` and replaces it with the provided misspelling. This is hacky way to get a gold-standard benchmark. The current best-performing model achieves the following results:

| Metric   | Value  |
|----------|--------|
| CER      | 9.6545 |
| WER      | 21.7558|
| Bleu     | 68.1724|

## Evluation on Sorani Script Normalization Benchmark
The final generated dataset is also concatenated with the training dataset from [Script Normalization for Unvonventional Writing](https://github.com/sinaahmadi/ScriptNormalization/tree/main) project. Therefore, the model not only correct spelling but also normalize unconventional writings. "Unconventional Writing" means using the writing system of one language to write in another language.

They also employ a similiar approach to generate their data. But it's not wise to evaluate your model on the synthetic test set since the model can memorize the underlying patterns from the training set. Hence they provide a gold-standard benchmark for Central Kurdish and they use `Bleu` & `chrF` to measure the performance of their model.

| Model                 | Bleu  | chrF  |
|-----------------------|-------|-------|
| Script Normalization  | 12.7  | 69.6  |
| Bart-kurd-spell-base  | 13.8  | 73.9  |

> Keep in mind of both these models have seen the same data for script normalization but our model is performing slighly better due to the additional data for spell correction.


## Train a New Model
Since the problem is framed as mapping a sequence containing misspellings to a correct sequence, we can train different econder-decoder models such as T5.
1. Run [`train_tokenizer.py`](train_tokenizer.py) to build tokenizer for your chosen model with `--tokenizer_name` argument.
2. Create `data.txt` and put it in [`data`](data) dir. Check [`inspect_data.ipynb`](inspect_data.ipynb).
3. Check the arguments of [`pepare_data/process_data.py`](pepare_data/process_data.py) and run it to get `train.csv` and `test.csv`
4. Change the arguments in [`train.sh`](train.sh) if your want to train a different model other than Bart. In case you want to train T5, you need to add `--source_prefix "correct: "`.
5. Evaluate the model on both [`data/asosoft_benchmark.csv`](data/asosoft_benchmark.csv) and [`data/Sorani-Arabic.csv`](data/Sorani-Arabic.csv) using  [`eval.sh`](eval.sh) 

## Observations
TBW

## References
- https://arxiv.org/abs/1910.13461
- https://www.researchsquare.com/article/rs-2974359/v1
- https://arxiv.org/abs/2305.16407
