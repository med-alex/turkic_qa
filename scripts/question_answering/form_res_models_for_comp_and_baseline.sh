#!/usr/bin/bash

model_dirname=$1

python /home/ml-srv-admin/Projects/turkic_qa/scripts/question_answering/form_res_models_for_comp_and_baseline.py \
        --model_dirname=$model_dirname
    