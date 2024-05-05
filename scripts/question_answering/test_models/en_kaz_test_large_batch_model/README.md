---
license: mit
base_model: FacebookAI/xlm-roberta-large
tags:
- generated_from_trainer
model-index:
- name: pure_xlm-rob-large-ft-en-mt-kaz
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# pure_xlm-rob-large-ft-en-mt-kaz

This model is a fine-tuned version of [FacebookAI/xlm-roberta-large](https://huggingface.co/FacebookAI/xlm-roberta-large) on the None dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 32
- eval_batch_size: 32
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 5.0

### Training results



### Framework versions

- Transformers 4.40.1
- Pytorch 2.0.0+cu118
- Datasets 2.18.0
- Tokenizers 0.19.1
