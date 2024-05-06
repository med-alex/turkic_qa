from pathlib import Path
from importlib import machinery, util
import argparse

import pandas as pd


loader = machinery.SourceFileLoader('preprocessing.py',
                                    str(Path.cwd()/'scripts'/'functions'/'preprocessing.py'))
spec = util.spec_from_loader('preprocessing.py', loader)
prep = util.module_from_spec(spec)
loader.exec_module(prep)

parser = argparse.ArgumentParser()
parser.add_argument('--input_data_path', dest='input_data_path',
                    type=str, required=True)
parser.add_argument('--output_data_path', dest='output_data_path',
                    type=str, required=True)
parser.add_argument('--sample_size', dest='sample_size',
                    type=int, required=False)
args = parser.parse_args()

data = pd.read_parquet(args.input_data_path)

data = data.drop(columns=['id'])

data['answer'] = data.answers.apply(lambda answer_info: \
                                    answer_info['text'][0])
data['answer_start'] = data.answers.apply(lambda answer_info: \
                                            int(answer_info['answer_start'][0]))
data = data.drop(columns=['answers'])

data = prep.handle_quote_issue(data)
for column in data.columns:
    data[column] = data[column].apply(lambda text: \
                                        prep.change_square_brackets_on_reqular(text) \
                                            if isinstance(text, str) else text)

answer_found_from_spans = data.apply(lambda data: \
                                        data.context[data.answer_start : \
                                                    data.answer_start+len(data.answer)], \
                                        axis=1)
data = data[data.answer == answer_found_from_spans]

if args.sample_size is not None and len(data.index) >= args.sample_size:
    data = data.sample(args.sample_size, random_state=42)
elif args.sample_size is not None and len(data.index) < args.sample_size:
    raise BaseException(f"Existing {len(data.index)} clean data rows \
        is not enough to sample desired {args.sample_size} rows")

data = prep.get_data_with_spans(data, '[', ']')

data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
