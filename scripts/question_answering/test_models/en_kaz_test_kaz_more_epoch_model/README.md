---
license: apache-2.0
base_model: kz-transformers/kaz-roberta-conversational
tags:
- generated_from_trainer
model-index:
- name: kaz-rob-ft-en-mt-kaz-more-epoch
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# kaz-rob-ft-en-mt-kaz-more-epoch

This model is a fine-tuned version of [kz-transformers/kaz-roberta-conversational](https://huggingface.co/kz-transformers/kaz-roberta-conversational) on the None dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 1e-05
- train_batch_size: 28
- eval_batch_size: 28
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- lr_scheduler_warmup_ratio: 0.2
- num_epochs: 15.0

### Training results



### Framework versions

- Transformers 4.40.1
- Pytorch 2.0.0+cu118
- Datasets 2.18.0
- Tokenizers 0.19.1