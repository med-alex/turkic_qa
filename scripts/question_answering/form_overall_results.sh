#!/usr/bin/bash

dirname_with_data=$1

python /home/ml-srv-admin/Projects/turkic_qa/scripts/question_answering/form_overall_results.py \
        --dirname_with_data=$dirname_with_data
    