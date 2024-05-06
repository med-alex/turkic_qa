import argparse
import os
import json
from pathlib import Path

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--dirname_with_data', dest='dirname_with_data',
                    type=str, required=True)
args = parser.parse_args()

baic_path = Path('/home/ml-srv-admin/Projects/turkic_qa/scripts/question_answering')
dir_path = baic_path / args.dirname_with_data
model_names = []
datasets = []
EM = []
F1 = []

content = os.scandir(dir_path)
for model_obj in content:
    if model_obj.is_dir() and model_obj.name.split('_')[-1] == 'model':
        model_dir_content = os.scandir(model_obj.path)
        for dataset_dir_obj in model_dir_content:
            if dataset_dir_obj.is_dir() and dataset_dir_obj.name != 'runs':

                model_source_lang_tag = model_obj.name.split('_')[0]
                model_target_lang_tag = model_obj.name.split('_')[1]

                dataset_source_lang_tag = dataset_dir_obj.name.split('_')[0]
                dataset_target_lang_tag = dataset_dir_obj.name.split('_')[1]
                dataset_name = dataset_dir_obj.name.split('_')[-1]

                mt_data_condition = model_source_lang_tag == dataset_source_lang_tag and \
                    model_target_lang_tag == dataset_target_lang_tag

                orig_data_condition = dataset_source_lang_tag == 'orig' and \
                    model_target_lang_tag == dataset_target_lang_tag

                if mt_data_condition or orig_data_condition:
                    with open(Path(dataset_dir_obj.path) / 'eval_results.json', 'r') as f:
                        info = json.load(f)

                        model_names += [model_obj.name]
                        datasets += [dataset_name]
                        EM += [round(info['eval_exact_match'], 2)]
                        F1 += [round(info['eval_f1'], 2)]
          
                else:
                    raise ValueError(f"model {model_obj} tags doesn't match \
                                        dataset {dataset_dir_obj} tags")

if len(model_names) == len(datasets) == len(F1) == len(EM):
    overall_data = pd.DataFrame(columns=list(set(datasets)), index=list(set(model_names)))
    for num, res in enumerate(F1):
        overall_data.loc[model_names[num], datasets[num]] = f'{EM[num]}, {F1[num]}'

    overall_data = overall_data.sort_index()
    overall_data['model_name'] = overall_data.index
    overall_data = overall_data[['model_name', *list(set(datasets))]]

overall_data.to_json(baic_path / f'{args.dirname_with_data}_overall_res.json',
                    lines=True, orient='records', force_ascii=False)
