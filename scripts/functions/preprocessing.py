# import string
# import re
# import contractions


def insert_spans(text, answer_start_num, suggested_answer):
    
    try: 
        isinstance(int(suggested_answer), int)
    except Exception:
        answer_end_num = answer_start_num + len(suggested_answer)
        if text[answer_start_num:answer_end_num] == \
            suggested_answer:
            text = text[:answer_start_num] + \
                    '<a>' + suggested_answer + '</a>' + \
                    text[answer_end_num:]
                    
    return text


def get_data_with_spans(data):
    
    data.context = data.apply(lambda data: insert_spans(data.context, 
                                                        data.answer_start, 
                                                        data.answer),
                                            axis=1)
    data.answer_start += 3
     
    return data


# def preprocess_text(text):
    
#     text = re.sub(r"[{}]".format(string.punctuation), '', text)
#     text = text.lower()
    
#     return text


# def preprocess_data(data):
    
#     for column in data.columns:
#         if column not in ['answer', 'answer_start']:
#             data[column] = data[column].apply(lambda text: preprocess_text(text))
#         elif column == 'answer':
#             data[column] = data[column].apply(lambda text: text.lower())
            
#     return data
