import argparse
from pathlib import Path
from importlib import machinery, util

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
args = parser.parse_args()

data = pd.read_parquet(args.input_data_path, columns=['context',
                                                      'question', 
                                                      'answers'])

data['answer'] = data.answers.apply(lambda answers: \
                                    answers['text'][0])
data['answer_start'] = data.answers.apply(lambda answers: \
                                          answers['answer_start'][0])

data = data.drop(columns=['answers'])

data = prep.handle_quote_issue(data)
for column in data.columns:
    data[column] = data[column].apply(lambda text: \
                                        prep.change_square_brackets_on_reqular(text) \
                                            if isinstance(text, str) else text)
for i in data.index:
    if data.loc[i].context[data.loc[i].answer_start : \
                            data.loc[i].answer_start + len(data.loc[i].answer)] \
                            != data.loc[i].answer:
        data.loc[i, 'answer_start'] = prep.find_new_answer_start(data.loc[i], data.loc[i].context)
data = prep.get_data_with_spans(data, '[', ']')

data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
