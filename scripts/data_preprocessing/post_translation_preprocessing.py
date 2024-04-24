import argparse
import pandas as pd
from pathlib import Path
import re
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
parser.add_argument('--output_info_dir_path', dest='output_info_dir_path', 
                    type=str, required=True)
parser.add_argument('--first_file_sample_size', dest='first_file_sample_size', 
                    type=int, required=False)
parser.add_argument('--second_output_data_path', dest='second_output_data_path', 
                    type=str, required=False)
parser.add_argument('--second_file_sample_size', dest='second_file_sample_size', 
                    type=int, required=False)
parser.add_argument('--third_output_data_path', dest='third_output_data_path', 
                    type=str, required=False)
args = parser.parse_args()

data = pd.read_pickle(args.input_data_path)

initial_data_len = len(data.index)

initial_data_without_any_brackets = data[~data.context.str.contains('\[|\]')]
initial_data_with_any_brackets = data[data.context.str.contains('\[|\]')]

initial_data_with_correct_brackets = data[[len(re.findall('\[', text)) == 1 and len(re.findall('\]', text)) == 1 for text in data.context]]
initial_data_without_correct_brackets = data[[len(re.findall('\[', text)) != 1 or len(re.findall('\]', text)) != 1 for text in data.context]]

data.context = data.apply(lambda data: data.context \
                                            if len(re.findall('\[', data.context)) == 1 and len(re.findall('\]', data.context)) == 1 \
                                                else prep.find_answer_from_translated_answer(data.context, data.answer) \
                                            if len(re.findall('\[', data.context)) == 0 and len(re.findall('\]', data.context)) == 0 \
                                                else prep.find_answer_from_context(data.context, data.answer),
                            axis=1)
data['answer_start'] = data.context.apply(lambda text: text.find('[') \
                                                if len(re.findall('\[', text)) == 1 and len(re.findall('\]', text)) == 1 \
                                                    else -1)

prep_data_without_brackets = data[data.answer_start == -1]
data = prep_data_with_brackets = data[data.answer_start != -1]

data.answer = data.context.apply(lambda text: re.findall('\[.+\]', text)[0][1:-1])
data.context = data.context.apply(lambda text: text.replace('[', '').replace(']', ''))
data.question = data.question.apply(lambda text: text[:-1] if text[-2:] == '?.' else text)
data.question = data.question.apply(lambda text: f"{text.replace('?', '')}?" \
                                        if re.findall('\?', text) and text[-1] != '?' else text)

if args.first_file_sample_size is not None \
    and args.second_output_data_path is not None \
    and args.third_output_data_path is not None:
    
    first_file_data = data[data.index.isin(initial_data_with_correct_brackets.index)].sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[(~data.index.isin(first_file_data.index)) & (data.index.isin(initial_data_with_correct_brackets.index))]\
                            .sample(args.second_file_sample_size, random_state=42)
    third_file_data = data[~data.index.isin(second_file_data.index)]

    first_file_data.to_pickle(args.output_data_path)
    second_file_data.to_pickle(args.second_output_data_path)
    third_file_data.to_pickle(args.third_output_data_path)
     
elif args.first_file_sample_size is not None \
    and args.second_output_data_path is not None \
    and args.third_output_data_path is None:
    
    first_file_data = data[data.index.isin(initial_data_with_correct_brackets.index)].sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[~data.index.isin(first_file_data.index)]
    
    first_file_data.to_pickle(args.output_data_path)
    second_file_data.to_pickle(args.second_output_data_path)

elif args.first_file_sample_size is not None \
    and args.second_output_data_path is None \
    and args.third_output_data_path is None:
    
    data.to_pickle(args.output_data_path)
  
else:
    raise BaseException(f"Configuration of desired output files provided in a wrong way")

info_path = Path(args.output_info_dir_path) / f'{Path(args.input_data_path).stem}.txt'
with open(info_path, 'w', encoding="utf-8") as writer:
    writer.write(f'initial_num_rows: {initial_data_len}'+'\n\n')
    writer.write(f'initial_num_rows_with_any_brackets: {len(initial_data_with_any_brackets.index)}'+'\n')
    writer.write(f'initial_num_rows_without_any_brackets: {len(initial_data_without_any_brackets.index)}'+'\n')
    writer.write(f'initial_perc_of_rows_with_any_brackets: {round((len(initial_data_with_any_brackets.index) / initial_data_len) * 100, 2)}'+'\n')
    writer.write(f'initial_perc_of_rows_without_any_brackets: {round((len(initial_data_without_any_brackets.index) / initial_data_len) * 100, 2)}'+'\n\n')   
    writer.write(f'initial_num_rows_with_correct_brackets: {len(initial_data_with_correct_brackets.index)}'+'\n')
    writer.write(f'initial_num_rows_without_correct_brackets: {len(initial_data_without_correct_brackets.index)}'+'\n')
    writer.write(f'initial_perc_of_rows_with_correct_brackets: {round((len(initial_data_with_correct_brackets.index) / initial_data_len) * 100, 2)}'+'\n')
    writer.write(f'initial_perc_of_rows_without_correct_brackets: {round((len(initial_data_without_correct_brackets.index) / initial_data_len) * 100, 2)}'+'\n\n')
    writer.write(f'prep_num_rows: {len(data.index)}'+'\n')
    writer.write(f'prep_num_rows_with_brackets: {len(prep_data_with_brackets.index)}'+'\n')
    writer.write(f'prep_num_rows_without_brackets: {len(prep_data_without_brackets.index)}'+'\n')
    writer.write(f'prep_perc_of_rows_with_brackets: {round((len(prep_data_with_brackets.index) / len(data.index)) * 100, 2)}'+'\n\n')
    writer.write(f'thrown_rows_without_brackets_to_initial_data: {round((len(prep_data_without_brackets.index) / initial_data_len) * 100, 2)}'+'\n')
