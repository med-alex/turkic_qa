#!/usr/bin/bash

source_dataset=$1
target_lang=$2

python scripts/translation/build_translated_data.py \
    --input_dir_path /home/ml-srv-admin/Projects/turkic_qa/scripts/translation/translated_data/$source_dataset/$target_lang \
    --output_dir_path /home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/raw
