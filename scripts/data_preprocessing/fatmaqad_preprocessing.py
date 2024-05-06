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

data = pd.read_json(args.input_data_path)

contexts = []
questions = []
answers = []
answer_starts = []
for paragraph_and_data in data['data']:
    for question_and_answer in paragraph_and_data['qas']:

        contexts += [paragraph_and_data['text']]
        questions += [question_and_answer['question']]
        answers += [question_and_answer['answer']]
        answer_starts += [int(question_and_answer['answer_start'])]
        
full_data = pd.DataFrame({'context': contexts, 
                          'question': questions, 
                          'answer': answers, 
                          'answer_start': answer_starts})

full_data = prep.handle_quote_issue(full_data)
for column in full_data.columns:
    full_data[column] = full_data[column].apply(lambda text: \
                                                prep.change_square_brackets_on_reqular(text) \
                                                    if isinstance(text, str) else text)
full_data = prep.get_data_with_spans(full_data, '[', ']')

full_data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
