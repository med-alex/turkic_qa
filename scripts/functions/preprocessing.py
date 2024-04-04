import re

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
     
    return data


def replace_double_quote(text):
    
    for quote_num, quote in enumerate(re.findall('"', text)):
        if quote_num % 2 == 0:
            text = re.sub('"', '«', text, count=1)
        elif quote_num % 2 != 0:
            text = re.sub('"', '»', text, count=1)
    
    text = re.sub('« ', '«', text)
    text = re.sub(' »', '»', text)
    
    return text


def handle_json_quote_issue(data):

    for column in data.columns:
        data[column] = data[column].apply(lambda text: replace_double_quote(text) if isinstance(text, str) else text)  

    return data
