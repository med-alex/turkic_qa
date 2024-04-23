#!/usr/bin/bash

output_file_name=fatmaqad_tr.json

python scripts/data_preprocessing/fatmaqad_preprocessing.py \
    --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/fatmaqad_tr.json \
    --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name
