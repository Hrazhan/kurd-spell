# Central Kurdish Neural Spell Corrector 
<img src="https://www.razhan.ai/_next/image?url=/static/images/projects/spell-checker.webp&w=1200&q=75" alt="Banner Image" height="200">

> **Note:** The documentation for this project is currently being written. I am working hard to make this project easily hackable so people can add new heuristics and train more models.

This repository contains a collection of neural spell correctors for the Central Kurdish language, trained on a large corpus of synthetically generated data. The models are able to correct a wide range of spelling errors, including typos and grammatical errors.



## Observations
| Model Name                                                       | Dataset Distortion| CER   | WER   |
|------------------------------------------------------------------|-------------------|-------|-------|
| [bart-base](razhan/bart-kurd-spell-base-05)  | 5%                | 5.39% | 34.73% |
| [bart-base](razhan/bart-kurd-spell-base-05)  | 10%               | 2.15% | 11.19% |
| [bart-base](https://huggingface.co/razhan/bart-kurd-spell-base-05_10)  | Mixed (5% + 10%)  | **1.54%** | **8.31%** |


### Evaluation on ASOSOFT Benchmark
The benchmark for this [Project](https://github.com/AsoSoft/Central-Kurdish-Spelling-dataset) is exclusively designed for single-word spelling corrections. The script `create_asosoft_benchmark.py` processes each word from the Amani dataset by searching for sentences with the correct spelling, checking if the sentence has not been included in `train.csv` and replaces it with the provided misspelling. This is hacky way to get a gold-standard benchmark. The current best-performing model achieves the following results:

| Metric   | Value  |
|----------|--------|
| CER      | 9.6545 |
| WER      | 21.7558|
| Bleu     | 68.1724|


## References
- [AraSpell](https://github.com/msalhab96/AraSpell/)
- https://www.researchsquare.com/article/rs-2974359/v1
- https://arxiv.org/abs/1910.13461
