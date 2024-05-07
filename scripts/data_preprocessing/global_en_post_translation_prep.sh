#!/usr/bin/bash

#en

#xquad
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_en_kaz_Cyrl xquad_en_kaz_test 190 xquad_en_kaz_val 200 xquad_en_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_en_uzn_Latn xquad_en_uzn_test 190 xquad_en_uzn_val 200 xquad_en_uzn_train

#squad val
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        squad_val_en_3500_kaz_Cyrl squad_en_kaz_val 1500 squad_en_kaz_test 

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        squad_val_en_3500_uzn_Latn squad_en_uzn_val 1500 squad_en_uzn_test

#sqaud train
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        squad_train_en_7500_kaz_Cyrl squad_en_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        squad_train_en_7500_uzn_Latn squad_en_uzn_train

#mlqa val
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        mlqa_val_en_kaz_Cyrl mlqa_en_kaz_test

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        mlqa_val_en_uzn_Latn mlqa_en_uzn_test

#mlqa test
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        mlqa_test_en_9000_kaz_Cyrl mlqa_en_kaz_val 1500 mlqa_en_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        mlqa_test_en_9000_uzn_Latn mlqa_en_uzn_val 1500 mlqa_en_uzn_train
