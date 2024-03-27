#!/usr/bin/bash

lang_tag=$1

python scripts/data_preprocessing/xquad_preprocessing.py \
    --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/xquad_$lang_tag.parquet \
    --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/xquad_$lang_tag.json
