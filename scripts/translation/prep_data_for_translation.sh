#!/usr/bin/bash

source_dataset=$1
source_lang_tag=$2
target_langs_tags=$3

python scripts/translation/data_prep_for_translation.py \
    --input_data_path /home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/$source_dataset.json \
    --output_dir_path /home/ml-srv-admin/Projects/turkic_qa/scripts/translation/translation_prep_data \
    --source_lang_tag $source_lang_tag \
    --target_langs_tags $target_langs_tags
    
#kaz_Cyrl,uzn_Latn
