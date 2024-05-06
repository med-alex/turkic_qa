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
answers_starts = []
for i in data.index:
    for paragraph in data.loc[i, 'data']['paragraphs']:
        questions += [qas['question'] for qas in paragraph['qas']]
        answers += [qas['answers'][0]['text'] for qas in paragraph['qas']]
        answers_starts += [int(qas['answers'][0]['answer_start']) for qas in paragraph['qas']]
        for num_qa in range(len([qas['question'] for qas in paragraph['qas']])):
            contexts += [paragraph['context']]

full_data = pd.DataFrame({'context':contexts,
                          'question':questions,
                          'answer':answers,
                          'answer_start':answers_starts})

full_data.question = full_data.question.apply(lambda question: f'{question.strip()[:-2]}?' \
                                                if question.strip()[-1] == '?' \
                                                    and question.strip()[-2] == ' ' \
                                                else question.strip())
for column in ['context', 'answer']:
    full_data[column] = full_data[column].apply(lambda text: text.strip())

full_data = prep.handle_quote_issue(full_data)
full_data = prep.deal_with_sevral_text_issues(full_data)
full_data = prep.get_data_with_spans(full_data, '[', ']')

full_data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
