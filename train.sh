# Train BART
python run_summarization.py \
    --model_name_or_path "facebook/bart-base" \
    --config_name "facebook/bart-base" \
    --tokenizer_name ./tokenizer \
    --do_train \
    --do_eval \
    --evaluation_strategy="epoch" \
    --group_by_length \
    --num_train_epochs=10 \
    --train_file train.csv \
    --validation_file test.csv \
    --preprocessing_num_workers="20" \
    --output_dir ./bart-kurd-spell-base/ \
    --overwrite_output_dir \
    --per_device_train_batch_size=320 \
    --per_device_eval_batch_size=256 \
    --gradient_accumulation_steps=1 \
    --predict_with_generate \
    --logging_steps="100" \
    --save_total_limit="1" \
    --save_strategy="epoch" \
    --report_to="wandb" \
    --run_name="Bart Spell" \
    --max_target_length=1024 \
    --max_source_length=1024 \
    --fp16 \
    --save_safetensors \
    --push_to_hub 

# Train T5
# python3 run_summarization.py \
#     --source_prefix "correct: " \
#     --model_name_or_path "google/flan-t5-small" \
#     --config_name "google/flan-t5-small" \
#     --tokenizer_name ./tokenizer \
#     --do_train \
#     --do_eval \
#     --evaluation_strategy="epoch" \
#     --group_by_length \
#     --num_train_epochs=5 \
#     --train_file train.csv \
#     --validation_file test.csv \
#     --preprocessing_num_workers="12" \
#     --output_dir ./t5-kurd-spell-base/ \
#     --overwrite_output_dir \
#     --per_device_train_batch_size=64 \
#     --per_device_eval_batch_size=64 \
#     --gradient_accumulation_steps=1 \
#     --predict_with_generate \
#     --logging_steps="100" \
#     --save_total_limit="1" \
#     --save_strategy="epoch" \
#     --report_to="none" \
#     --run_name="T5 Spell" \
#     --max_target_length=1024 \
#     --max_source_length=1024 \
#     --push_to_hub 
#     # --fp16 \
