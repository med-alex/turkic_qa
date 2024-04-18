#!/usr/bin/bash

if [ ! -z $3 ] 
then
    input_file_name=sberquad_$1_ru.parquet
    output_file_name=sberquad_$2_ru_$3.json
    sample_size=$3

    python scripts/data_preprocessing/sberquad_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name \
        --sample_size=$sample_size
else
    input_file_name=sberquad_$1_ru.parquet
    output_file_name=sberquad_$2_ru.json

    python scripts/data_preprocessing/sberquad_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$output_file_name
fi
