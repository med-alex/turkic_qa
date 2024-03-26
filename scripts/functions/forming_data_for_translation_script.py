def forming_column_for_translation(column, src_lang, trg_lang):
    
    column = column.apply(lambda text: {'src_txt': text,
                                        'tgt_txt': '',
                                        'src_lang': src_lang,
                                        'tgt_lang': trg_lang
                                        })
    column.name = 'translation'
    
    return column
