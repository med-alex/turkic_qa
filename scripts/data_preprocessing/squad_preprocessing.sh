#!/usr/bin/bash

if [ ! -z $3 ] 
then
    input_file_name=squad_$1_en.parquet
    output_file_name=squad_$2_en_$3.json
    sample_size=$3

    python scripts/data_preprocessing/squad_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name \
        --sample_size=$sample_size
else
    input_file_name=squad_$1_en.parquet
    output_file_name=squad_$2_en.json

    python scripts/data_preprocessing/squad_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name
fi
