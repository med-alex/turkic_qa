def insert_spans(text, answer_start_num, suggested_answer, span_left, span_right):
    
    try: 
        isinstance(int(suggested_answer), int)
    except Exception:
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
