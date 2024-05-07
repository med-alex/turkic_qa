#!/usr/bin/bash

#ru

#xquad
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_ru_kaz_Cyrl xquad_ru_kaz_test 190 xquad_ru_kaz_val 200 xquad_ru_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_ru_uzn_Latn xquad_ru_uzn_test 190 xquad_ru_uzn_val 200 xquad_ru_uzn_train

#sberquad val
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        sberquad_val_ru_3000_kaz_Cyrl sberquad_ru_kaz_test

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        sberquad_val_ru_3000_uzn_Latn sberquad_ru_uzn_test

#sqaud train
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        sberquad_train_ru_18000_kaz_Cyrl sberquad_ru_kaz_val 3000 sberquad_ru_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        sberquad_train_ru_18000_uzn_Latn sberquad_ru_uzn_val 3000 sberquad_ru_uzn_train
