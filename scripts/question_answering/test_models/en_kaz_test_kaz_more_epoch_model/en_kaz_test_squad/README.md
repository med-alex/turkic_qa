---
base_model: med-alex/kaz-rob-ft-en-mt-kaz-more-epoch
tags:
- generated_from_trainer
model-index:
- name: en_kaz_test_squad
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# en_kaz_test_squad

This model is a fine-tuned version of [med-alex/kaz-rob-ft-en-mt-kaz-more-epoch](https://huggingface.co/med-alex/kaz-rob-ft-en-mt-kaz-more-epoch) on the None dataset.

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
- train_batch_size: 16
- eval_batch_size: 16
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 3.0

### Framework versions

- Transformers 4.40.1
- Pytorch 2.1.2
- Datasets 2.18.0
- Tokenizers 0.19.1
