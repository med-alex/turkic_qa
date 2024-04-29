import argparse
import pandas as pd
import numpy as np
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

data = pd.read_json(args.input_data_path, orient='records', lines=True)

initial_data_len = len(data.index)

initial_data_without_any_brackets = data[~data.context.str.contains('\[|\]')]
initial_data_with_any_brackets = data[data.context.str.contains('\[|\]')]

initial_data_with_correct_brackets = data[[len(re.findall('\[', text)) == 1 and len(re.findall('\]', text)) == 1 for text in data.context]]
initial_data_without_correct_brackets = data[[len(re.findall('\[', text)) != 1 or len(re.findall('\]', text)) != 1 for text in data.context]]

data = data[[True if len(question.split()) <= 30 else False for question in data.question]]
data.answer = data.answer.apply(lambda answer: answer[:-1] if answer[:-1] == '.' else answer)
data['found_answer'] = data.context.apply(lambda context: re.findall('\[.+\]', context))
data['found_left_brackets'] = data.context.apply(lambda context: re.findall('\[', context))
data['found_right_brackets'] = data.context.apply(lambda context: re.findall('\]', context))
data.context = data.apply(lambda data: prep.answer_in_context_validation(data.context, data.answer, data.found_answer[0][1:-1]) \
                                if len(data.found_left_brackets) == 1 and len(data.found_right_brackets) == 1 \
                                    and len(data.found_answer) > 0 and len(data.found_answer[0]) > 2 \
                                        else prep.find_answer_in_context_from_translated_answer(data.context, data.answer) \
                                if len(data.found_left_brackets) == 1 and len(data.found_right_brackets) == 1 \
                                    and len(data.found_answer) > 0 and len(data.found_answer[0]) <= 2 \
                                        else prep.find_answer_in_context_from_context(data.context, data.answer) \
                                if len(data.found_left_brackets) == 0 and len(data.found_right_brackets) == 0 \
                                        else prep.find_answer_in_context_from_context(data.context, data.answer),
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
data['answers'] = data.apply(lambda data: {'text': np.array([data.answer], dtype=object), 'answer_start': np.array([data.answer_start], dtype=np.int32)}, 
                             axis=1)
data = data.drop(columns=['answer', 'answer_start', 'found_answer', 'found_left_brackets', 'found_right_brackets'])

three_files_condition = args.output_data_path is not None and args.first_file_sample_size is not None \
                        and args.second_output_data_path is not None and args.second_file_sample_size is not None \
                        and args.third_output_data_path is not None

two_files_condition = args.output_data_path is not None and args.first_file_sample_size is not None \
                        and args.second_output_data_path is not None and args.second_file_sample_size is None \
                        and args.third_output_data_path is None

one_file_condition = args.output_data_path is not None and args.first_file_sample_size is None \
                        and args.second_output_data_path is None and args.second_file_sample_size is None \
                        and args.third_output_data_path is None

if three_files_condition:
    first_file_data = data[data.index.isin(initial_data_with_correct_brackets.index)].sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[(~data.index.isin(first_file_data.index)) & (data.index.isin(initial_data_with_correct_brackets.index))]\
                            .sample(args.second_file_sample_size, random_state=42)
    third_file_data = data[~data.index.isin(second_file_data.index)]
    
    first_file_data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
    second_file_data.to_json(args.second_output_data_path, orient='records', lines=True, force_ascii=False)
    third_file_data.to_json(args.third_output_data_path, orient='records', lines=True, force_ascii=False)
     
elif two_files_condition:
    first_file_data = data[data.index.isin(initial_data_with_correct_brackets.index)].sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[~data.index.isin(first_file_data.index)]
    
    first_file_data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
    second_file_data.to_json(args.second_output_data_path, orient='records', lines=True, force_ascii=False)

elif one_file_condition:
    data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)
  
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
    writer.write(f'thrown_rows_without_brackets_to_initial_data: {round((len(prep_data_without_brackets.index) / initial_data_len) * 100, 2)}'+'\n\n')
    
    if three_files_condition:
        writer.write(f'first_file_size: {first_file_data.shape}, split: {Path(args.output_data_path).stem}'+'\n')
        writer.write(f'second_file_size: {second_file_data.shape}, split: {Path(args.second_output_data_path).stem}'+'\n')
        writer.write(f'second_file_size: {third_file_data.shape}, split: {Path(args.third_output_data_path).stem}'+'\n')
        
    elif two_files_condition:
        writer.write(f'first_file_size: {first_file_data.shape}, split: {Path(args.output_data_path).stem}'+'\n')
        writer.write(f'second_file_size: {second_file_data.shape}, split: {Path(args.second_output_data_path).stem}'+'\n')
        
    elif one_file_condition:
        writer.write(f'first_file_size: {data.shape}, split: {Path(args.output_data_path).stem}'+'\n')
