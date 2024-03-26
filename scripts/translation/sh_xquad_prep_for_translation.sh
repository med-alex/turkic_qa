#!/usr/bin/bash

python scripts/translation/data_prep_for_translation.py \
    --input_data_path /home/ml-srv-admin/Projects/turkic_qa/data/source_langs/preprocessed/xquad_en.json \
    --output_dir_path /home/ml-srv-admin/Projects/turkic_qa/scripts/translation/prepared_data \
    --source_lang_tag eng_Latn \
    --target_langs_tags kaz_Cyrl,uzn_Latn