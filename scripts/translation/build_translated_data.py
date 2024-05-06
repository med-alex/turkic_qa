import argparse
import re
from pathlib import Path

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--input_dir_path', dest='input_dir_path',
                    type=str, required=True)
parser.add_argument('--output_dir_path', dest='output_dir_path',
                    type=str, required=True)
args = parser.parse_args()

full_data = pd.DataFrame()
for folder_name in ['contexts', 'questions', 'answers']:

    with open(f'{args.input_dir_path}/{folder_name}/generated_predictions.txt', 'r') as file:
        data = file.readlines()
        data = pd.Series([re.sub('\n', '', line) for line in data], name=folder_name[:-1])
        full_data = pd.concat([full_data, data], axis=1)

output_path = Path(args.output_dir_path)
output_path.mkdir(parents=True, exist_ok=True)

full_data.to_json(output_path / \
                    f'{Path(args.input_dir_path).parents[0].stem}_{Path(args.input_dir_path).stem}.json',
                  orient='records', lines=True, force_ascii=False)
