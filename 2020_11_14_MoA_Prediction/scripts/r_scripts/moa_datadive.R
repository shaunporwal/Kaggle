library(dplyr)
library(ggplot2)
library(reshape)

path_to_data_folder <- '~/kaggle_data/lish-moa/'
sample_submission <- read.csv('~/kaggle_data/lish-moa/sample_submission.csv')
test_features <- read.csv('~/kaggle_data/lish-moa/test_features.csv')
train_drug <- read.csv('~/kaggle_data/lish-moa/train_drug.csv')
train_features <- read.csv('~/kaggle_data/lish-moa/train_features.csv')
train_targets_nonscored <- read.csv('~/kaggle_data/lish-moa/train_targets_nonscored.csv')
train_targets_scored <- read.csv('C:/Users/seobo/Documents/kaggle_data/lish-moa/train_targets_scored.csv')
summary(train_features)

control <- train_features %>% filter(cp_type == 'ctl_vehicle')
rownames(control) <- control$sig_id
cols_drop <- c('sig_id','cp_type', 'cp_time', 'cp_dose')
control <- control[,!(names(control) %in% cols_drop)]

sample <- c('g.0','g.1','g.2','c.0','c.1','c.2')

boxplot(control[,sample])


