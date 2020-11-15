import dplyr
path_to_data_folder <- '~/kaggle_data/lish-moa/'
sample_submission <- read.csv('~/kaggle_data/lish-moa/sample_submission.csv')
test_features <- read.csv('~/kaggle_data/lish-moa/test_features.csv')
train_drug <- read.csv('~/kaggle_data/lish-moa/train_drug.csv')
train_features <- read.csv('~/kaggle_data/lish-moa/train_features.csv')
train_targets_nonscored <- read.csv('~/kaggle_data/lish-moa/train_targets_nonscored.csv')
train_targets_scored <- read.csv('~/kaggle_data/lish-moa/train_targets_scored.csv')