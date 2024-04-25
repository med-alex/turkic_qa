import argparse
import pandas as pd
from pathlib import Path
from importlib import machinery, util
loader = machinery.SourceFileLoader('forming_data_for_translation_script.py', 
                                    str(Path.cwd()/'scripts'/'functions'/'forming_data_for_translation_script.py'))
spec = util.spec_from_loader('forming_data_for_translation_script.py', loader)
form_data = util.module_from_spec(spec)
loader.exec_module(form_data)


parser = argparse.ArgumentParser()
parser.add_argument('--input_data_path', dest='input_data_path', 
                    type=str, required=True)
parser.add_argument('--output_dir_path', dest='output_dir_path', 
                    type=str, required=True)
parser.add_argument('--source_lang_tag', dest='source_lang_tag', 
                    type=str, required=True)
parser.add_argument('--target_langs_tags', dest='target_langs_tags', 
                    type=str, required=True)
args = parser.parse_args()

data = pd.read_json(args.input_data_path, lines=True)

name_split = Path(args.input_data_path).stem.split('_')
if (name_split[-1] != 'en' and name_split[-2] != 'en' and args.source_lang_tag == 'eng_Latn') \
    or (name_split[-1] != 'ru' and name_split[-2] != 'ru' and args.source_lang_tag == 'rus_Cyrl') \
    or (name_split[-1] != 'tr' and name_split[-2] != 'tr' and args.source_lang_tag == 'tur_Latn'):
    raise ValueError(f"Specified source language: {args.source_lang_tag} and sorce language dataset: {args.input_data_path} don't match")

for target_language_tag in args.target_langs_tags.split(','):
    for column in ['context', 'question', 'answer']:
        data_column = form_data.forming_column_for_translation(data[column], args.source_lang_tag, target_language_tag)
        
        path = Path(args.output_dir_path) / Path(args.input_data_path).stem / target_language_tag / f'{column}s'
        path.mkdir(parents=True, exist_ok=True)
        
        pd.DataFrame(data_column).to_json(f'{str(path)}/data.json', orient='records', lines=True, force_ascii=False)
