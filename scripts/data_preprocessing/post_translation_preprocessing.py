import argparse
import re
from pathlib import Path
from importlib import machinery, util

import pandas as pd
import numpy as np


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

# посчитаем некоторые показатели
initial_data_len = len(data.index)

initial_data_without_any_brackets = data[~data.context.str.contains('\[|\]')]
initial_data_with_any_brackets = data[data.context.str.contains('\[|\]')]

initial_data_with_correct_brackets = data[[len(re.findall('\[', text)) == 1
                                                and len(re.findall('\]', text)) == 1
                                            for text in data.context]]
initial_data_without_correct_brackets = data[[len(re.findall('\[', text)) != 1
                                                    or len(re.findall('\]', text)) != 1
                                                for text in data.context]]

# удалим строчки, где при переводе ошибочно сгенерировались слишком большие последовательности токенов
data = data[[True if len(question.split()) <= 30 else False for question in data.question]]

# удалим точку с конца ответов
data.answer = data.answer.apply(lambda answer: answer[:-1] if answer[-1] == '.' else answer)

# найдем некоторые характеристики строк, которые используем в дальнейшем:
# последовательность в квадратных скобках из контекста
data['str_in_brackets'] = data.context.apply(lambda context: re.findall('\[.+\]', context))
# количество найденных левыx и правыx скобок отдельно
data['found_left_brackets'] = data.context.apply(lambda context: len(re.findall('\[', context)))
data['found_right_brackets'] = data.context.apply(lambda context: len(re.findall('\]', context)))

data.context = data.apply(lambda data: prep.answer_in_context_validation(data.context, \
                                                                         data.answer, \
                                                                         data.str_in_brackets[0][1:-1]) \
                                # 1. когда в контексте есть одна левая и одна правая скобка, и пара скобок одна
                                if data.found_left_brackets == 1 \
                                        and data.found_right_brackets == 1 \
                                        and len(data.str_in_brackets) == 1 \
                                    # если выполняется первое условие, то валидируем ответ в скобках и
                                        # возвращаем контекст либо с ответом в скобках, либо без скобок
                                    else prep.find_answer_in_context_from_translated_answer(data.context, \
                                                                                            data.answer) \
                                        # 2. когда в контексте нет ни одной левой и правой скобки
                                    if data.found_left_brackets == 0 \
                                            and data.found_right_brackets == 0 \
                                        # в этом случае пробуем найти ответ в контексте с помощью
                                            # переведенного ответа. Если находится, то возвращаем
                                            # контекст с ответом скобках, если нет, то контекст
                                            # без скобок
                                        else prep.find_answer_in_context_from_context(data.context, \
                                                                                        data.answer), \
                                            # 3. естественным образом остаются прочие ситуации,
                                                # когда пар скобок больше одной. В этих случаях
                                                # пробуем выбрать ответ из существующих вариантов
                                                # если удается, то возвращаем контекст с ответом
                                                # в скобках, если нет, контекст без скобок
                            axis=1)

# найдем начало ответа в контексте. А если скобок нет, то присваеваем -1
data['answer_start'] = data.context.apply(lambda text: text.find('[') \
                                                if len(re.findall('\[', text)) == 1 and len(re.findall('\]', text)) == 1 \
                                                    else -1)

# найдем количество строк, с -1 (т.е. без ответа)
prep_data_without_brackets = data[data.answer_start == -1]
# для дальнеших преобразований выберем только строки с ответом
data = prep_data_with_brackets = data[data.answer_start != -1]

# на место ответа поставим значения, которые находятся в скобках в контексте, чтобы они совпадали
data.answer = data.context.apply(lambda text: re.findall('\[.+\]', text)[0][1:-1])
# удалим скобки из контекста
data.context = data.context.apply(lambda text: text.replace('[', '').replace(']', ''))

# в вопросах удалим точку на конце, если сгенерированная последовательность заканчивается на ?.
data.question = data.question.apply(lambda text: text[:-1] if text[-2:] == '?.' else text)
# есть также случаи, когда вопросительный знак оказывается не в конце последовательности. 
# В таком случае удалим его из середины, и поставим в конец
data.question = data.question.apply(lambda text: f"{text.replace('?', '')}?" \
                                        if re.findall('\?', text) and text[-1] != '?' else text)

# приведем данные об ответе и начале ответа к формату SQUAD 
data['answers'] = data.apply(lambda data: {'text': np.array([data.answer], dtype=object), \
                                            'answer_start': np.array([data.answer_start], dtype=np.int32)}, \
                             axis=1)
data = data.drop(columns=['answer', 'answer_start', 'str_in_brackets',
                          'found_left_brackets', 'found_right_brackets'])

# определим условия разделения и сохранения данных, в зависимости от
# необходимости разделить данные на три/два файла, или оставить один
three_files_condition = args.output_data_path is not None \
                        and args.first_file_sample_size is not None \
                        and args.second_output_data_path is not None \
                        and args.second_file_sample_size is not None \
                        and args.third_output_data_path is not None

two_files_condition = args.output_data_path is not None \
                        and args.first_file_sample_size is not None \
                        and args.second_output_data_path is not None \
                        and args.second_file_sample_size is None \
                        and args.third_output_data_path is None

one_file_condition = args.output_data_path is not None \
                        and args.first_file_sample_size is None \
                        and args.second_output_data_path is None \
                        and args.second_file_sample_size is None \
                        and args.third_output_data_path is None

# разделим и сохраним данные
if three_files_condition:
    first_file_data = data.sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[~data.index.isin(first_file_data.index)] \
                            .sample(args.second_file_sample_size, random_state=42)
    third_file_data = data[~data.index.isin(first_file_data.index) & ~data.index.isin(second_file_data.index)]

    first_file_data.to_json(args.output_data_path,
                            orient='records', lines=True, force_ascii=False)
    second_file_data.to_json(args.second_output_data_path,
                             orient='records', lines=True, force_ascii=False)
    third_file_data.to_json(args.third_output_data_path,
                            orient='records', lines=True, force_ascii=False)

elif two_files_condition:
    first_file_data = data.sample(args.first_file_sample_size, random_state=42)
    second_file_data = data[~data.index.isin(first_file_data.index)]

    first_file_data.to_json(args.output_data_path,
                            orient='records', lines=True, force_ascii=False)
    second_file_data.to_json(args.second_output_data_path,
                             orient='records', lines=True, force_ascii=False)

elif one_file_condition:
    data.to_json(args.output_data_path, orient='records', lines=True, force_ascii=False)

else:
    raise BaseException("Configuration of desired output files provided in a wrong way")

# также посчитаем и сохраним некоторые показатели о данных и препроцессинге
info_path = Path(args.output_info_dir_path) / f'{Path(args.input_data_path).stem}.txt'
with open(info_path, 'w', encoding="utf-8") as writer:
    writer.write(f'initial num rows: {initial_data_len}' + '\n\n')

    initial_num_rows_with_any_brackets = len(initial_data_with_any_brackets.index)
    writer.write(f'initial num rows with any brackets: {initial_num_rows_with_any_brackets}' + '\n')

    initial_num_rows_without_any_brackets = len(initial_data_without_any_brackets.index)
    writer.write(f'initial num rows without any brackets: {initial_num_rows_without_any_brackets}' + '\n')

    initial_perc_of_rows_with_any_brackets = round((len(initial_data_with_any_brackets.index) \
                                                    / initial_data_len) * 100, 2)
    writer.write(f'initial perc of rows with any brackets: {initial_perc_of_rows_with_any_brackets}' + '\n')

    initial_perc_of_rows_without_any_brackets = round((len(initial_data_without_any_brackets.index) \
                                                        / initial_data_len) * 100, 2)
    writer.write(f'initial perc of rows without any brackets: {initial_perc_of_rows_without_any_brackets}' + '\n\n')

    initial_num_rows_with_correct_brackets = len(initial_data_with_correct_brackets.index)
    writer.write(f'initial num rows with correct brackets: {initial_num_rows_with_correct_brackets}' + '\n')

    initial_num_rows_without_correct_brackets = len(initial_data_without_correct_brackets.index)
    writer.write(f'initial num rows without correct brackets: {initial_num_rows_without_correct_brackets}' + '\n')

    initial_perc_of_rows_with_correct_brackets = round((len(initial_data_with_correct_brackets.index) \
                                                        / initial_data_len) * 100, 2)
    writer.write(f'initial perc of rows with correct brackets: {initial_perc_of_rows_with_correct_brackets}' + '\n')

    initial_perc_of_rows_without_correct_brackets = round((len(initial_data_without_correct_brackets.index) \
                                                            / initial_data_len) * 100, 2)
    writer.write(f'initial perc of rows without correct brackets: {initial_perc_of_rows_without_correct_brackets}' + '\n\n')

    writer.write(f'prep num rows: {len(data.index)}' + '\n')

    writer.write(f'prep num rows with brackets: {len(prep_data_with_brackets.index)}' + '\n')

    writer.write(f'prep num rows without brackets: {len(prep_data_without_brackets.index)}' + '\n')

    prep_perc_of_rows_with_brackets = round((len(prep_data_with_brackets.index) \
                                            / len(data.index)) * 100, 2)
    writer.write(f'prep perc of rows with brackets: {prep_perc_of_rows_with_brackets}' + '\n\n')

    thrown_rows_without_brackets_to_initial_data = round((len(prep_data_without_brackets.index) \
                                                            / initial_data_len) * 100, 2)
    writer.write(f'thrown rows without brackets to initial data: {thrown_rows_without_brackets_to_initial_data}' + '\n\n')

    if three_files_condition:
        writer.write(f'first file size: {first_file_data.shape}, split: {Path(args.output_data_path).stem}' + '\n')
        writer.write(f'second file size: {second_file_data.shape}, split: {Path(args.second_output_data_path).stem}' + '\n')
        writer.write(f'second file size: {third_file_data.shape}, split: {Path(args.third_output_data_path).stem}' + '\n')

    elif two_files_condition:
        writer.write(f'first file size: {first_file_data.shape}, split: {Path(args.output_data_path).stem}' + '\n')
        writer.write(f'second file size: {second_file_data.shape}, split: {Path(args.second_output_data_path).stem}' + '\n')

    elif one_file_condition:
        writer.write(f'first file size: {data.shape}, split: {Path(args.output_data_path).stem}' + '\n')
