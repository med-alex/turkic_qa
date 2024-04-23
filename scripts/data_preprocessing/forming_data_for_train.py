import argparse
import os 
from pathlib import Path
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--input_dir_path', dest='input_dir_path', 
                    type=str, required=True)
parser.add_argument('--output_dir_path', dest='output_dir_path', 
                    type=str, required=True)
args = parser.parse_args()

data = pd.DataFrame(columns=['context', 'question', 'answer', 'answer_start'])

for source_lang in ['en', 'tr', 'ru']:
    for target_lang in ['kaz', 'uzn']:
        for split in ['test', 'val', 'train']:
            merging_files_paths = []
            for filename in os.listdir(args.input_dir_path):
                filename = Path(filename)
                if filename.suffix == '.pickle':
                    name_parts = filename.stem.split('_')
                    
                    file_source_lang = name_parts[1]
                    file_target_lang = name_parts[2]
                    file_split = name_parts[-1]

                    if file_source_lang == source_lang \
                        and file_target_lang == target_lang \
                        and file_split == split:

                        merging_files_paths += [str(Path(args.input_dir_path) / filename)]
         
            for file_path in merging_files_paths:
                data = pd.concat([data, pd.read_pickle(file_path)], ignore_index=True, axis=1)
            
            data = data.sample(frac=1)
            data.to_pickle(Path(args.output_dir_path) / f'{source_lang}_{target_lang}_{split}.pickle')
