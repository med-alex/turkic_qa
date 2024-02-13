#!/usr/bin/bash

python scripts/data_preprocessing/xquad_preprocessing.py \
    --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/xquad_en.parquet \
    --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/xquad_en.jsonl
