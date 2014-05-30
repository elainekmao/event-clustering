library(boot)

low_vs_high = read.csv("low_vs_high_stats.csv", header=F, sep=",")
expiration_vs_none = read.csv("expiration_vs_none_stats.csv", header=F, sep=",")

meanfunction <- function(x,i){mean(x[i])}
results <- boot(data=expiration_vs_none$V1, statistic=meanfunction, R=100)

