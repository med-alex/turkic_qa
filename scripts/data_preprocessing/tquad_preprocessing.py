import argparse
import pandas as pd
from pathlib import Path
from importlib import machinery, util
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
    for paragraph in data.loc[i].values[0]['paragraphs']:
        questions += [qas['question'] for qas in paragraph['qas']]
        answers += [qas['answers'][0]['text'] for qas in paragraph['qas']]
        answers_starts += [int(qas['answers'][0]['answer_start']) for qas in paragraph['qas']]
        for num_qa in range(len([qas['question'] for qas in paragraph['qas']])):
            contexts += [paragraph['context']]

full_data = pd.DataFrame({'context':contexts,
                          'question':questions,
                          'answer':answers,
                          'answer_start':answers_starts})

full_data.question = full_data.question.apply(lambda question: f'{question.strip()[:-2]}?' 
                                              if question.strip()[-1]=='?' and question.strip()[-2]==' ' 
                                              else question.strip())
full_data.context = full_data.context.apply(lambda context: context.strip())
for i in full_data.index:
    if full_data.loc[i, 'answer'][-1] == ' ':
        full_data.loc[i, 'answer'] = full_data.loc[i, 'answer'].rstrip()
    if full_data.loc[i, 'answer'][0] == ' ':
        full_data.loc[i, 'answer'] = full_data.loc[i, 'answer'].lstrip()
        full_data.loc[i, 'answer_start'] -= 1

full_data = prep.get_data_with_spans(full_data, '[', ']')

full_data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
