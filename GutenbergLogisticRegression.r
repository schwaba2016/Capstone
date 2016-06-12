#Written for R
#Program is intended to predict the genre (fiction or nonfiction)
#of cleaned text documents in English sourced from Project Gutenberg.


setwd("D:/Capstone/RCode")
#list of 559 text files
textfiledir <- "D:/Gutenberg8C/"

#modules
library(NLP)
library(tm)
library(readr)
library(RWeka)
library(RColorBrewer)
library(wordcloud)
library(plyr)
require(plyr)

#loading in file containing filename and genre
filegenre <- read.csv("D:/Capstone/Code/filegenre.csv", header = TRUE)
bookstext <- filegenre

#Obtaining a list of files in the directory
#All files are .txt file type.
file_list = list.files("D:/Gutenberg8C")

#creating a variable containing the text of the 559 books (text files)
booktext <- list()

for (filename in file_list) {
  #print(filename)
  filetoread <- paste0(textfiledir, filename)
  singlestring <- read_file(filetoread)
  singlestring2 <- gsub("\n"," ",singlestring)
  booktext <- rbind(booktext, singlestring2)
}

bookstext <- cbind(bookstext, booktext)

#converting the 'fiction' or 'nonfiction' designation into 1 (nonfiction) or 0 (fiction)
bookstext2 <- bookstext
bookstext2$genre <- as.character(bookstext2$genre)
bookstext2$genre[bookstext2$genre == "nonfiction"] <- 1
bookstext2$genre[bookstext2$genre == "fiction"] <- 0
bookstext2$genre <- as.numeric(bookstext2$genre)

#creating a variable containing equal number of files for each genre
text_data <- bookstext2[, c(2,3)]
c0 <- text_data[text_data["genre"]==0,]
length(c0)
c1 <- text_data[text_data["genre"]==1,]
length(c1)
c1_559 <- c1[sample(nrow(c1), 232),]
data_559 <- rbind(c0, c1_559)
table(data_559$genre)

#Processing the booktext
myCorpus <- Corpus(VectorSource(data_559$booktext))
myCorpus <- tm_map(myCorpus, removePunctuation)
myCorpus <- tm_map(myCorpus, removeNumbers)
myCorpus <- tm_map(myCorpus, stripWhitespace)
myCorpus <- tm_map(myCorpus, removeWords, stopwords("english"))

dtm <- DocumentTermMatrix(myCorpus)
str(dtm)
dput(head(dtm, 30))


findFreqTerms(dtm, 30)
dtm_tfidf <- DocumentTermMatrix(myCorpus, control = list(weighting = weightTfIdf, minWordLength=2, minDocFreq=5))
sort(as.matrix(dtm_tfidf)[1,], decreasing=T)[1:20]
df1 <- as.data.frame(as.matrix(dtm))
df2 <- as.data.frame(as.matrix(dtm_tfidf))
df1_c<-cbind(df1,out_put_class=as.factor(data_559$genre))
df2_c<-cbind(df2,out_put_class=as.factor(data_559$genre))

df1colsums <- colSums(df1)
df2colsums <- colSums(df2)
sum(df1colsums[df1colsums > 500])

#http://stackoverflow.com/questions/10608060/excluding-columns-from-a-dataframe-based-on-column-sums
#Limiting the regression model to use words that occur more than 4,000 times in the corpus
df1B <- df1[,colSums(df1)>4000]
length(df1B)
df2B <- df2[,colSums(df1)>4000]
length(df2B)
df1B_c<-cbind(df1B,out_put_class=as.factor(data_559$genre))
df2B_c<-cbind(df2B,out_put_class=as.factor(data_559$genre))

#cross validation logistic regression model based on the frequency of words
formula = as.formula("out_put_class ~ .")
weka_fit1 <- Logistic(formula, data = df1B_c)
evaluate_Weka_classifier(weka_fit1, numfolds = 10)
weka_fit2 <- Logistic(formula, data = df2B_c)
evaluate_Weka_classifier(weka_fit2, numfolds = 10)

#Get most frequent words for fiction books
myCorpus0 <- Corpus(VectorSource(c0$booktext))
myCorpus0 <- tm_map(myCorpus0, removePunctuation)
myCorpus0 <- tm_map(myCorpus0, removeNumbers)
myCorpus0 <- tm_map(myCorpus0, stripWhitespace)
myCorpus0 <- tm_map(myCorpus0, removeWords, stopwords("english"))

#cross-validation logistic regression model based on the importance of the words (td-idf)
dtm0 <- DocumentTermMatrix(myCorpus0)
dtm0_tfidf <- DocumentTermMatrix(myCorpus0, control = list(weighting = weightTfIdf, minWordLength=2, minDocFreq=5))
sort(as.matrix(dtm0_tfidf)[1,], decreasing=T)[1:50]

#Get most frequent words for nonfiction books
myCorpus1 <- Corpus(VectorSource(c1_559$booktext))
myCorpus1 <- tm_map(myCorpus1, removePunctuation)
myCorpus1 <- tm_map(myCorpus1, removeNumbers)
myCorpus1 <- tm_map(myCorpus1, stripWhitespace)
myCorpus1 <- tm_map(myCorpus1, removeWords, stopwords("english"))

dtm1 <- DocumentTermMatrix(myCorpus1)
dtm1_tfidf <- DocumentTermMatrix(myCorpus1, control = list(weighting = weightTfIdf, minWordLength=2, minDocFreq=5))
sort(as.matrix(dtm1_tfidf)[1,], decreasing=T)[1:50]


#----------
#wordcloud
#----------

#http://www.rdatamining.com/examples/text-mining
http://www.r-bloggers.com/word-cloud-in-r/

m <- as.matrix(dtm)
myNames <- colnames(m)
myrowsums <- rowSums(m)
mycolsums <- colSums(m)

mydata <- cbind(myNames, mycolsums)
mydataframe <- data.frame(word=myNames, freq=mycolsums)
mydataframe2 <- mydataframe
mydataframe2$word <- as.character(mydataframe2$word)
order.freq <- order(mydataframe2$freq, decreasing=TRUE)
mydataframe2[order(mydataframe2$freq, decreasing=TRUE),]

wordcloud(mydataframe2$word, mydataframe2$freq, min.freq=922, c(4, 0.5))
