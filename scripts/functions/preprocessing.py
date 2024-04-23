import re
from difflib import SequenceMatcher
from nltk import ngrams


def insert_spans(text, answer_start_num, suggested_answer, span_left, span_right):
    
    answer_end_num = answer_start_num + len(suggested_answer)
    if text[answer_start_num:answer_end_num] == \
        suggested_answer:
        text = text[:answer_start_num] + \
                span_left + suggested_answer + span_right + \
                text[answer_end_num:]
                    
    return text


def get_data_with_spans(data, span_left, span_right):
    
    data.context = data.apply(lambda data: insert_spans(data.context, 
                                                        data.answer_start, 
                                                        data.answer,
                                                        span_left, 
                                                        span_right),
                                            axis=1)
    data.answer_start += len(span_left)
    
    for i in data.index:
        if not re.findall('\[.+\]', data.loc[i].context) \
            or re.sub('\[|\]', '', re.findall('\[.+\]', data.loc[i].context)[0]) != data.loc[i].answer:
            raise BaseException(f"In row {i} answer spans don't inserted or inserted in a wrong way")

    return data



def handle_json_quote_issue(data):

    for column in data.columns:
        data[column] = data[column].apply(lambda text: text.replace('"', "'") if isinstance(text, str) else text)

    return data


def delete_unmatched_brackets(text):
    
    for brakets_pair in ['()', '[]', '{}']:
        correct_sent = []
        for sub_sent_num, sub_sent in enumerate(re.split(f'\{brakets_pair[0]}', text)):
            if sub_sent_num == 0:
                correct_sent += re.sub(f'\{brakets_pair[1]}', '', sub_sent)
            elif re.findall(f'\{brakets_pair[1]}', sub_sent):
                correct_sent += f'{brakets_pair[0]}{sub_sent}'
            else:
                correct_sent += sub_sent
        text = ''.join(correct_sent)
    
    return text


def change_square_brackets_on_reqular(text):
    
    text = text.replace('[', '(')
    text = text.replace(']', ')')
    
    return text


def get_rid_of_special_characters(text):
    
    text = re.sub('\\r\\n', ' ', text)        
    
    return text


def get_rid_of_unnessesary_extra_spaces(text):
    
    sep_simbols = ['\.', ',', ';', ':']
    for sep_simbol in sep_simbols:
        pattern = '\s+' + sep_simbol + '\s+'
        findings = re.findall(pattern, text)
        for f in findings:
            simbol = sep_simbol if sep_simbol != '\.' else '.'
            text = re.sub(pattern, f'{simbol} ', text)
    
    return text


def insert_nessesary_extra_spaces(text):

    for f in re.findall('\S+\s+-[\S][^\d]|\S+-\s+\S+', text):
        found_start = text.find(f)
        input_changing_fild = text[found_start:found_start + len(f)]
        output_changing_fild = ' - '.join([split_part.strip() for split_part in re.split('-', input_changing_fild)])
        text = text.replace(input_changing_fild, output_changing_fild, 1)

    return text


def split_sentence(text):

    sep_simbols = ['\.', ',', ';', ':']
    for sep_simbol in sep_simbols:
        pattern = '[^\s\.,]{3,}' + sep_simbol + '[^\d\s\.,]{1,}'
        findings = re.findall(pattern, text)
        for f in findings:
            found_start = text.find(f)
            input_changing_fild = text[found_start:found_start + len(f)]
            split_simbol = sep_simbol if sep_simbol != '\.' else f'\d*{sep_simbol}'
            join_simbol = sep_simbol if sep_simbol != '\.' else '.'
            output_changing_fild = f'{join_simbol} '.join(re.split(split_simbol, input_changing_fild))
            text = text.replace(input_changing_fild, output_changing_fild, 1)
            
    return text


def get_rid_of_unnesesary_numbers_at_the_end(text):
    
    pattern = '[^\d\s:;,.-]{3,}\d+\.'
    findings = re.findall(pattern, text)
    for f in findings:
        found_start = text.find(f)
        input_changing_fild = text[found_start:found_start + len(f)]
        output_changing_fild = ''.join(re.split('\d+', input_changing_fild))
        text = text.replace(input_changing_fild, output_changing_fild)
        
    return text


def find_new_answer_start(data, new_context):
    
    split_sent = new_context.split(data.answer)
    best_ratio = 0.
    new_answer_start = 0
    for sub_sent_num, sub_sent in enumerate(split_sent):
        testing_str = f'{data.answer}'.join(split_sent[:sub_sent_num+1])
        if len(testing_str) == 0:
            testing_str = data.answer
        match_ratio = SequenceMatcher(None, 
                            data.context[:data.answer_start],
                            testing_str).ratio()
        if match_ratio > best_ratio:
            best_ratio = match_ratio
            new_answer_start = len(f'{data.answer}'.join(split_sent[:sub_sent_num+1]))

    return new_answer_start


def deal_with_sevral_text_issues(data):

    new_data = data.copy()
    for column in ['answer', 'context', 'question']:
        for i in new_data.index:
            text = new_data.loc[i, column]
            if isinstance(text, str):
                text = delete_unmatched_brackets(text)
                text = change_square_brackets_on_reqular(text)
                text = get_rid_of_special_characters(text)
                text = get_rid_of_unnessesary_extra_spaces(text)
                text = insert_nessesary_extra_spaces(text)
                text = split_sentence(text)
                text = get_rid_of_unnesesary_numbers_at_the_end(text)                       
                if column == 'context':
                    new_data.loc[i, 'answer_start'] = find_new_answer_start(new_data.loc[i], text)
                    
                new_data.loc[i, column] = text
                
    return new_data


def find_answer_in_contex(context, answer):

    len_translated_answer_nqram = len(answer.split())

    possible_answers_ngrams_length = [len_translated_answer_nqram + i for i in range(-2,3) \
                                        if len_translated_answer_nqram + i > 0]

    answers_by_ngrams = [[n_gram for n_gram in ngrams(context.split(), ngram_length)] \
                            for ngram_length in possible_answers_ngrams_length]
    possible_answers = [possible_answer for sub_list in answers_by_ngrams for possible_answer in sub_list]

    best_ratio = 0
    best_choice_ngram_length = 0
    found_answer = ''
    for possible_answer in possible_answers:
        possible_answer = ' '.join(possible_answer)
        match_ratio = SequenceMatcher(None,
                                    possible_answer,
                                    answer).ratio()
        if match_ratio > best_ratio:
            best_ratio = match_ratio
            best_choice_ngram_length = len(possible_answer)
            found_answer = possible_answer
        elif match_ratio == best_ratio and len(possible_answer) < best_choice_ngram_length:
            best_ratio = match_ratio
            best_choice_ngram_length = len(possible_answer)
            found_answer = possible_answer

    if best_ratio >= 0.8:
        context = insert_spans(context, context.find(found_answer), found_answer, '[', ']')
    
    return context
