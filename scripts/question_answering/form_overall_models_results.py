import pandas as pd
import os
import json
from pathlib import Path


dir_path = '/home/ml-srv-admin/Projects/turkic_qa/scripts/question_answering'
model_names = []
datasets = []
EM = []
F1 = []
for dirname, _, filenames in os.walk(dir_path):
    if dirname.split('_')[-1] == 'model':
        model_name = Path(dirname).stem
        model_source_lang = model_name.split('_')[0]
        model_target_lang = model_name.split('_')[1]
        model_dir = dirname

        if model_name != 'baseline_model':
            for inside_dir_path, _, inside_filenames in os.walk(model_dir):
                inside_dir = Path(inside_dir_path).stem
                if (inside_dir.split('_')[0] == model_source_lang and \
                    inside_dir.split('_')[1] == model_target_lang and \
                    inside_dir_path != model_dir) \
                    or (inside_dir.split('_')[0] == 'orig' and \
                    inside_dir.split('_')[1] == model_target_lang and \
                    inside_dir_path != model_dir):
                    
                    res_file_path = Path(inside_dir_path) / 'eval_results.json'
                    dataset_name = inside_dir.split('_')[-1]
                    
                    if os.path.isfile(res_file_path):
                        with open(res_file_path, 'r') as f:
                            info = json.load(f)
                        
                            model_names += [model_name]
                            datasets += [dataset_name]
                            EM += [round(info['eval_exact_match'], 2)]
                            F1 += [round(info['eval_f1'], 2)]
                            
                    else:
                        model_names += [model_name]
                        datasets += [dataset_name]
                        EM += [None]
                        F1 += [None]
        elif model_name == 'baseline_model':
            res_file_path = Path(dirname) / 'overall_res.json'
            print(res_file_path)
            if os.path.isfile(res_file_path):
                info = pd.read_json(res_file_path, lines=True, orient='records')

                for i in range(len(info.index)):
                    source_lang = info.iloc[i]['dataset'].split('_')[0]
                    target_lang = info.iloc[i]['dataset'].split('_')[1]
                    datasets += [info.iloc[i]['dataset'].split('_')[-1]]
                    EM += [info.iloc[i]['EM']]
                    F1 += [info.iloc[i]['F1']]
                    model_names += [f'{model_name} ({source_lang} to {target_lang})']
            else:
                model_names += [model_name]
                datasets += [datasets[0]]
                EM += [None]
                F1 += [None]
                      
if len(model_names) == len(datasets) == len(F1) == len(EM):
    overall_data = pd.DataFrame(columns=list(set(datasets)), index=list(set(model_names)))
    for num, res in enumerate(F1):
        overall_data.loc[model_names[num], datasets[num]] = (F1[num], EM[num])
    
    overall_data = overall_data.sort_index()
    overall_data['model_name'] = overall_data.index
    overall_data = overall_data[['model_name', *list(set(datasets))]]

overall_data.to_json(dir_path + '/overall_res.json', 
                    lines=True, orient='records', force_ascii=False)
