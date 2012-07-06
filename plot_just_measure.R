#!/usr/bin/env Rscript (python)
# -*- encoding: utf-8 -*-
# ./plot_just_measure.R
#
# (c) 2010 Konstantin Sering, Nora Umbach, Dominik Wabersich
# <colorlab[at]psycho.uni-tuebingen.de>
#
# GPL 3.0+ or (cc) by-sa (http://creativecommons.org/licenses/by-sa/3.0/)
#
# plots for behavior of luminance of tubes over time
#
# content: (1) Plot most recent measurement
#
# input: justmeasure_color_20120519_1121.txt
# output: /figures/tubes_over_time.pdf
#
# last mod 2012-05-21, NU

#setwd("Z:/AG_Heller/calibdata/measurements/calibdata")

###### (1) Plot most recent measurement ######
## i=1
## times=10
## files <- dir(pattern="calibrange[0-9][0-9].*\\.txt")

# plot(x=1, y=1, xlim=c(700,800), ylim=c(200,300), type="n")
# for (file in files){
# dat <- read.table(file,header=TRUE)

# #par(new=T, fig=c(0,1,0,1))
# #x <- seq(1,length(dat[,1]),by=100)
# points(y=dat$Y, x=dat$gray_1, xlab="gray color", ylab="Luminance", pch=4, col=colors()[(i+50)*5])
# i=i+1
# }

# dev.print(device=postscript, "highend.eps")
#pdf(paste("testpdf.pdf", sep=""), height=2.75, width=10)
#dev.off()

i=1
times=10
files <- dir(pattern="calibrange[0-9][0-9].*\\.txt")

## Nora's solution
dat1 <- NULL
for (file in files){
   dat1 <- rbind(dat1, read.table(file, T))
   }

dat2 <- dat1[,c(1,6,7,8)]
dat2$time <- factor(rep(1:times, e=180))
dat3 <- dat2[dat2$gray_1<800,] #remove dodgy points

i=1
nlslist <-  NULL
for (i in 1:10){
  subdata <- dat3[dat3$time==i,]
  nlslist <- c(nlslist, list(nls(Y~((a*gray_1)-s)^g, subdata, start=c(a=0.005, g=3.5, s=-1), trace=T)))
}

nlsfulldata <- nls(Y~((a*gray_1)-s)^g, dat3, start=c(a=0.005, g=3.5, s=-1), trace=T)

means <- NULL
for(gray in seq(795, 5, by=-5)){
  means <- c(means, mean(dat3[dat3$gray_1==gray,]$Y))

}

## > nlsmeans
## Nonlinear regression model
##   model:  means ~ ((a * grayval) - s)^g 
##    data:  datmeans 
##         a         g         s 
##  0.001964  5.632002 -1.163851 
##  residual sum-of-squares: 51.52

## Number of iterations to convergence: 29 
## Achieved convergence tolerance: 3.936e-07 
## > nlsfulldata
## Nonlinear regression model
##   model:  Y ~ ((a * gray_1) - s)^g 
##    data:  dat3 
##         a         g         s 
##  0.001964  5.632002 -1.163851 
##  residual sum-of-squares: 2132

datmeans <- data.frame(dat3[dat3$time==1,]$gray_1, means)
colnames(datmeans)[1] <- "grayval"

nlsmeans <- nls(means~((a*grayval)-s)^g, datmeans, start=c(a=0.005, g=3.5, s=-1), trace=T)

summary(nlsall)

plot(dat3$gray_1, dat3$Y, xlim=c(760,795), ylim=c(240,290), type=c("p"))
points(predict(nlsfulldata)~gray_1, dat3, col="red")
points(predict(nlsmeans)~grayval, datmeans, col="blue")


# points(gamma(subdata$gray_1, 0.005, -1, 3.5)~subdata$gray_1, col="yellow", type="l")
# summary(nls1)
#predict(nls1)
#Completely wrong attempt at ANOVA
# In theory may work for one specific colour, but need more than one point
## subdata <- dat3[dat3$gray_1==895,]
## tsst <- sum((subdata$Y-mean(subdata$Y))^2)

## i=1

## ssw <- 0
## ssb <- 0
## len <- length(subdata[subdata$time==1,]$Y)
## #dat3[dat3$time==1,]
## for (i in times){
##   ssw <- ssw+ sum((subdata[subdata$time==i,]$Y-mean(subdata[subdata$time==i,]$Y))^2)
##   ssb <- ssb+(5*((mean(subdata[subdata$time==i,]$Y)-mean(subdata$Y))^2))
## }

## fstat <- (ssb/(times-1))/(ssw/(times*(len-1)))





## library(lattice)

## xyplot(Y ~ gray_1 | time, dat2, type=c("l","g"))

## s <- seq(50, 25, -5)
## dat_tmp <- dat2[dat2$gray_1 %in% s,]

## xyplot(Y ~ gray_1, dat_tmp, type=c("b","g"), groups=time)



