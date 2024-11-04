export PYTHONPATH=./
export CUDA_VISIBLE_DEVICES=0,1
export TRANSFORMERS_NO_ADVISORY_WARNINGS='true'
PROC_PER_NODE=$(python -c "import torch; print(torch.cuda.device_count())")
MASTER_PORT=11451

LANGUAGE=en
TASK_NAME=layoutlmv3-base_rfund_${LANGUAGE}
PRETRAINED_PATH=private_pretrained/layoutlmv3-base
DATA_DIR=private_data/rfund
OUTPUT_DIR=private_output/weights/$TASK_NAME
RUNS_DIR=private_output/runs/$TASK_NAME
LOG_DIR=private_output/logs/$TASK_NAME.log
torchrun --nproc_per_node $PROC_PER_NODE --master_port $MASTER_PORT start/run_rfund.py \
    --model_name_or_path $PRETRAINED_PATH \
    --data_dir $DATA_DIR \
    --language $LANGUAGE \
    --output_dir $OUTPUT_DIR \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --dataloader_num_workers 1 \
    --warmup_ratio 0.1 \
    --learning_rate 5e-5 \
    --max_steps 25000 \
    --evaluation_strategy steps \
    --eval_steps 1000 \
    --save_strategy steps \
    --save_steps 1000 \
    --save_total_limit 1 \
    --logging_strategy epoch \
    --logging_dir $RUNS_DIR \
    --detail_eval True \
    --save_eval_detail True \
    2>&1 | tee -a $LOG_DIR