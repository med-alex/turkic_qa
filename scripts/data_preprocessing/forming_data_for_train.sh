#!/usr/bin/bash

python /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/forming_data_for_train.py \
    --input_dir_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed \
    --output_dir_path=/home/ml-srv-admin/Projects/turkic_qa/data/for_finetuning
