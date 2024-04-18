#!/usr/bin/bash

input_file_name=thquad_$1_tr.json
output_file_name=thquad_$2_tr.json

python scripts/data_preprocessing/thquad_preprocessing.py \
    --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
    --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name
