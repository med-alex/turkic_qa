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

for source_lang in ['en', 'tr', 'ru']:
    for target_lang in ['kaz', 'uzn']:
        for split in ['test', 'val', 'train']:
            data = pd.DataFrame(columns=['context', 'question', 'answers'])
            if split in ['val', 'train']:
                merging_files_paths = []
                for filename in os.listdir(args.input_dir_path):
                    filename = Path(filename)
                    if filename.suffix == '.json':
                        name_parts = filename.stem.split('_')

                        file_source_lang = name_parts[1]
                        file_target_lang = name_parts[2]
                        file_split = name_parts[-1]

                        if file_source_lang == source_lang \
                            and file_target_lang == target_lang \
                            and file_split == split:

                            merging_files_paths += [str(Path(args.input_dir_path) / filename)]

                for file_path in merging_files_paths:
                    data = pd.concat([data, pd.read_json(file_path,
                                                         orient='records', lines=True)],
                                     ignore_index=True, axis=0)

                data.index = list(range(len(data.index)))
                data = data.sample(frac=1)
                data['id'] = data.index
                data.to_json(Path(args.output_dir_path) / \
                                f'{source_lang}_{target_lang}_{split}.json',
                                    orient='records', lines=True, force_ascii=False)

            elif split == 'test':
                for filename in os.listdir(args.input_dir_path):
                    filename = Path(filename)
                    if filename.suffix == '.json':
                        name_parts = filename.stem.split('_')

                        dataset_name = name_parts[0]
                        file_source_lang = name_parts[1]
                        file_target_lang = name_parts[2]
                        file_split = name_parts[-1]

                        if file_source_lang == source_lang \
                            and file_target_lang == target_lang \
                            and file_split == split:

                            data_as_it_is = pd.read_json(str(Path(args.input_dir_path) / filename),
                                                         orient='records', lines=True)
                            data_as_it_is = data_as_it_is.sample(frac=1)
                            data_as_it_is['id'] = data_as_it_is.index

                            data_as_it_is.to_json(Path(args.output_dir_path) / \
                                                    f'{source_lang}_{target_lang}_{split}_{dataset_name}.json',
                                                    orient='records', lines=True, force_ascii=False)
