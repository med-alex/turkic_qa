import os
import json
import argparse
from pathlib import Path

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--model_dirname', dest='model_dirname',
                    type=str, required=True)
args = parser.parse_args()

dir_path = Path.cwd() / 'scripts' / 'question_answering' / {args.model_dirname}
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
    overall_res.to_json(dir_path + f'/{Path(dir_path).name}_overall_res.json',
                        lines=True, orient='records', force_ascii=False)
