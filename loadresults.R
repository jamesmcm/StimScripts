files <- list.files(pattern="jamcvp01ses*")

dat1 <-  read.table(files[1], header = TRUE)
dat1 <- dat1[-c(1:20),]


for (i in 2:length(files)){
tempdat <-  read.table(files[i], header = TRUE)
tempdat <- tempdat[-c(1:20),]
dat1 <- rbind(dat1, tempdat)
}

dat1$leftinfield=dat1$leftmean-dat1$leftgrayplus
dat1$rightinfield=dat1$rightmean-dat1$rightgrayplus

xtabs(~ leftinfield + rightinfield, dat1)

dat1$leftstimuli=0

dat1[dat1$leftinfield==356 & dat1$leftmean==456,]$leftstimuli=1
dat1[dat1$leftinfield==376 & dat1$leftmean==476,]$leftstimuli=2
dat1[dat1$leftinfield==396 & dat1$leftmean==496,]$leftstimuli=3
dat1[dat1$leftinfield==416 & dat1$leftmean==516,]$leftstimuli=4
dat1[dat1$leftinfield==436 & dat1$leftmean==536,]$leftstimuli=5
dat1[dat1$leftinfield==416 & dat1$leftmean==476,]$leftstimuli=6
dat1[dat1$leftinfield==376 & dat1$leftmean==516,]$leftstimuli=7
View(dat1)

dat1$rightstimuli=0
dat1[dat1$rightinfield==356 & dat1$rightmean==456,]$rightstimuli=1
dat1[dat1$rightinfield==376 & dat1$rightmean==476,]$rightstimuli=2
dat1[dat1$rightinfield==396 & dat1$rightmean==496,]$rightstimuli=3
dat1[dat1$rightinfield==416 & dat1$rightmean==516,]$rightstimuli=4
dat1[dat1$rightinfield==436 & dat1$rightmean==536,]$rightstimuli=5
dat1[dat1$rightinfield==416 & dat1$rightmean==476,]$rightstimuli=6
dat1[dat1$rightinfield==376 & dat1$rightmean==516,]$rightstimuli=7
