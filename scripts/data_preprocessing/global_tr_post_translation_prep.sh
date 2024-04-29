#!/usr/bin/bash

#tr

#xquad
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_tr_kaz_Cyrl xquad_tr_kaz_test 190 xquad_tr_kaz_val 200 xquad_tr_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        xquad_tr_uzn_Latn xquad_tr_uzn_test 190 xquad_tr_uzn_val 200 xquad_tr_uzn_train

#thquad dev
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        thquad_dev_tr_kaz_Cyrl thquad_tr_kaz_test

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        thquad_dev_tr_uzn_Latn thquad_tr_uzn_test

#thquad train
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        thquad_train_tr_kaz_Cyrl thquad_tr_kaz_val 1500 thquad_tr_kaz_train 

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        thquad_train_tr_uzn_Latn thquad_tr_uzn_val 1500 thquad_tr_uzn_train

#fatmaqad
bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        fatmaqad_tr_kaz_Cyrl fatmaqad_tr_kaz_test 1250 fatmaqad_tr_kaz_val 1000 fatmaqad_tr_kaz_train

bash /home/ml-srv-admin/Projects/turkic_qa/scripts/data_preprocessing/post_translation_preprocessing.sh \
        fatmaqad_tr_uzn_Latn fatmaqad_tr_uzn_test 1250 fatmaqad_tr_uzn_val 1000 fatmaqad_tr_uzn_train
