
library(ggplot2)
library(reshape)

install.packages('dplyr')

library(dplyr)

path_to_data_folder <- '~/kaggle_data/lish-moa/'
sample_submission <- read.csv('~/kaggle_data/lish-moa/sample_submission.csv')
test_features <- read.csv('~/kaggle_data/lish-moa/test_features.csv')
train_drug <- read.csv('~/kaggle_data/lish-moa/train_drug.csv')
train_features <- read.csv('~/kaggle_data/lish-moa/train_features.csv')
train_targets_nonscored <- read.csv('~/kaggle_data/lish-moa/train_targets_nonscored.csv')
train_targets_scored <- read.csv('~/kaggle_data/lish-moa/train_targets_scored.csv')
summary(train_features)

control <- train_features %>% filter(cp_type == 'ctl_vehicle')
rownames(control) <- control$sig_id
cols_drop <- c('sig_id','cp_type', 'cp_time', 'cp_dose')
control <- control[,!(names(control) %in% cols_drop)]

sample <- c('g.0','g.1','g.2','g.3','g.4','c.0','c.1','c.2','c.3','c.4')

boxplot(control[,sample])

experimental <- train_features %>% filter(cp_type == 'trt_cp')

experimental <- experimental[,!(names(control) %in% cols_drop)]
boxplot(experimental[,sample])
sd(experimental[,'g.0'])
mad(experimental[,'g.0'])*2
hist(experimental[,'g.0'])
mean(experimental[,'g.0'])
median(experimental[,'g.0'])

joined <- left_join(experimental, train_targets_scored, by = NULL, copy = FALSE)
cols_drop <- c('sig_id', 'cp_type', 'cp_time', 'cp_dose')

tmp <- experimental %>% filter(sig_id == 'id_000644bb2')
tmp <- tmp[,!(names(tmp) %in% cols_drop)]
#tmp <- data.frame(t(tmp))
rownames(tmp) <- 'val'
tmp5 <- tmp[,tmp > 0.5]
tmp1 <- tmp[,tmp > 1]
tmp2 <- tmp[,tmp > 2.0]
tmp196 <- tmp[,tmp > 1.96]

tmp <- joined['5-alpha_reductase_inhibitor'== 1]

