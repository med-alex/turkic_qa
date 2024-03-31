#!/usr/bin/bash

input_file_name=xquad_$1.parquet
output_file_name=xquad_$1.json

python scripts/data_preprocessing/xquad_preprocessing.py \
    --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
    --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name
