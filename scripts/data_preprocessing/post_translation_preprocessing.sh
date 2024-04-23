#!/usr/bin/bash

input_file_name=$1.pickle
first_output_file_name=$2.pickle

if [ ! -z $6 ]
then
    first_file_sample_size=$3
    second_output_file_name=$4.pickle
    second_file_sample_size=$5    
    third_output_file_name=$6.pickle

    python /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$first_output_file_name \
        --output_info_dir_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/preprocessing_info \
        --first_file_sample_size=$first_file_sample_size \
        --second_output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$second_output_file_name \
        --second_file_sample_size=$second_file_sample_size \
        --third_output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$third_output_file_name
    
elif [ ! -z $4 ]
then
    first_file_sample_size=$3.pickle
    second_output_file_name=$4.pickle

    python /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$first_output_file_name \
        --output_info_dir_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/preprocessing_info \
        --first_file_sample_size=$first_file_sample_size \
        --second_output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$second_output_file_name
        
elif [ ! -z $2 ]
then
    python /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.py \
        --input_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/raw/$input_file_name \
        --output_data_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/$first_output_file_name \
        --output_info_dir_path=/home/ml-srv-admin/Projects/turkic_qa/data/target_lagns/preprocessed/preprocessing_info

fi