import pandas as pd
import os
import json
from pathlib import Path

dir_path = '/home/ml-srv-admin/Projects/turkic_qa/scripts/question_answering/baseline_model'
datasets = []
EM = []
F1 = []
for dirname, _, filenames in os.walk(dir_path):
    for filename in filenames:
        if filename == 'eval_results.json':
            path_to_info = os.path.join(dirname, filename)
            with open(path_to_info, 'r') as f:
                info = json.load(f)
                
                datasets += [Path(path_to_info).parent.stem]
                EM += [round(info['eval_exact_match'], 2)]
                F1 += [round(info['eval_f1'], 2)]

if len(datasets) == len(F1) == len(EM):
    overall_res = pd.DataFrame({'dataset': datasets, 'EM': EM, 'F1': F1}).sort_values('dataset')
    overall_res.to_json(dir_path + '/overall_res.json', 
                        lines=True, orient='records', force_ascii=False)
