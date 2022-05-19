response_data <- read.table("response_times.csv", header=T, sep=",")

png(filename="figure.png", height=900, width=1440, 
 bg="white")
   
barplot(as.matrix(response_data), main="Resp times", ylab= "Total",
   beside=TRUE, col=rainbow(3))

legend("topleft", c("httpclient sync","httpclient async","webclient"), cex=0.6, 
   bty="n", fill=rainbow(3));

dev.off()
