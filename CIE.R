library(colorspace)
library(RColorBrewer)

i=0
mypalette <- NULL
#array <- as.matrix(1:786432,768,1024)
array <- t(matrix(1:10000,100,100))
j=0
while(i<=100){
  while(j<=100){
    #Switch to xyY
    Y=1
    x=i/100
    y=j/100
    X=(Y/y)*x
    Z=(Y/y)*(1-x-y)
    ## print(X)
    ## print(Y)
    ## print(Z)
    colort <- XYZ(X, Y,Z)
    mypalette <- c(mypalette, hex(colort, gamma = NULL, fixup = FALSE))
    j <- j+1
  }
  i <- i+1
  print(i)
  j <- 1
}

image((array),col=mypalette,xlab="Greens (sequential)", ylab="",xaxt="n",yaxt="n",bty="n")


#1024x768
colort=XYZ(0.4,0.4,1)
hex(colort, gamma = NULL, fixup = FALSE)

show(as(colort, "RGB"))

mypalette<-brewer.pal(7,"Greens")

image(t(vectorm),col=mypalette,xlab="Greens (sequential)", ylab="",xaxt="n",yaxt="n",bty="n")
