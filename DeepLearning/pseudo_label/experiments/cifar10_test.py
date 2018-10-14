import sys
import torch

import main
import test_dataset
from util.Config import parse_dict_args

def parameters():
    defaults = {
        # Technical details
        'is_parallel': False,
        'workers': 2,
        'checkpoint_epochs': 20,

        # Data
        'dataset': 'cifar10',
        'base_batch_size': 64,
        'base_labeled_batch_size': 32,
        'print_freq': 30,
        'train_subdir': 'train+val',
        'eval_subdir': 'test',

        # Architecture
        #'arch': 'lenet',
        #'arch': 'vgg19',
        'arch': 'resnet18',
        #'arch': 'preact_resnet18',
        #'arch': 'densenet121',
        #'arch': 'resnext29_32x4d',
        #'arch': 'senet',
        #'arch': 'dpn92',
        #'arch': 'shuffleG3',
        #'arch': 'mobileV2',

        # Optimization
        'loss': 'soft',
        'optim': 'adam',
        'epochs': 500,
        'base_lr': 0.001,
        'momentum': 0.9,
        'weight_decay': 5e-4,
        'nesterov': True,

        # lr_schedular
        #'lr_scheduler': 'none',
        #'lr_scheduler': 'multistep',
        'steps': '100,150,200,250,300,350,400,450,480',
        'gamma': 0.5,
        'lr_scheduler': 'cos',
        'min_lr': 1e-4,
    }

    for n_labels in [4000]:
        for data_seed in range(10, 11):
            yield{
                **defaults,
                'n_labels': n_labels,
                'data_seed': data_seed
            }

def run(base_batch_size, base_labeled_batch_size, base_lr, n_labels, data_seed, is_parallel, **kwargs):
    if is_parallel and torch.cuda.is_available():
        ngpu = torch.cuda.device_count()
    else:
        ngpu = 1
    adapted_args = {
        'batch_size': base_batch_size * ngpu,
        'labeled_batch_size': base_labeled_batch_size * ngpu,
        'lr': base_lr,
        'labels': 'data-local/labels/cifar10/{}_balanced_labels/{:02d}.txt'.format(n_labels, data_seed),
        'is_parallel': is_parallel,
    }
    args = parse_dict_args(**adapted_args, **kwargs)
    main.main(args)
    #test_dataset.main(args)


if __name__ == "__main__":
    for run_params in parameters():
        run(**run_params)
