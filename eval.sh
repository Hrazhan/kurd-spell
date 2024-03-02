# Evaluation
python3 run_summarization.py \
    --model_name_or_path "razhan/bart-kurd-spell-base" \
    --do_eval \
    --validation_file data/asosoft_benchmark.csv \
    --output_dir /tmp \
    --overwrite_output_dir \
    --per_device_eval_batch_size=32 \
    --predict_with_generate \
    --logging_steps="1" \
    --max_target_length=1024 \
    --max_source_length=1024 \
    --report_to="none" 