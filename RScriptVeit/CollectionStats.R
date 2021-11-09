library(jsonlite)
library(eulerr)
library(dplyr)
library(wordcloud2)
library(webshot2)


A <- read_json("https://bio.tools/api/t?format=json&page=1")
num_tools <- A$count

# #Full dump, takes time
# AllTools <- NULL
# for (i in 1:(num_tools/10)) {
#   AllTools <- c(AllTools, read_json(paste0("https://bio.tools/api/t?format=json&page=",i))$list)  
#      
#   }
# length(AllTools)
# write_json(AllTools, path="fullDump.json")
fullToolContent <- read_json("fullDump.json")


### Getting all tool names
fullToolNames <- read_json("fullDump.json")
fullToolNames <- unlist(sapply(fullToolNames, function(x) x$name[[1]]))


################## Here we define the use cases ############
usecase <- "https://bio.tools/api/t?topic='Proteomics'&format=json"

## Use case using call above
A <- read_json(paste0(usecase, "&page=1"))
num_tools <- A$count
num_tools

AllTools <- NULL
for (i in 1:(num_tools/10)) {
  AllTools <- c(AllTools, read_json(paste0(usecase, "&page=",i))$list)
  
}
length(AllTools)


## Extracting EDAM terms and more
extractStats <- function(toolSet, termname=NULL, termname2=NULL, termname3=NULL, tags=c("term","uri")) {
  collectTopics <- list()
  for (i in 1:length(toolSet)) {
    currTool <- toolSet[[i]]
    subTool <- NULL
    if (is.null(termname)) {
      subTool <- currTool
    } else if (is.null(termname2)) {
      subTool <- currTool[[termname]]
    } else if (is.null(termname3)) {
      if (length(currTool[[termname]]) > 0) {
        subTool <- lapply(currTool[[termname]], function(x) x[[termname2]])
      } else {
        subTool <- NULL
      }
    } else {
      if (length(currTool[[termname]]) > 0) {
        if (length(currTool[[termname]][[1]][[termname2]]) > 0) {
          subTool <- lapply(currTool[[termname]], function(x) lapply(x[[termname2]], function(y) y[[termname3]]))
        } else {
          subTool <- NULL
        }
      } else {
        subTool <- NULL
      }
    }
    if (length(subTool) > 0) {
      while (length(subTool[[1]][[1]]) > 0 & is.null(names(subTool[[1]])) & paste(subTool[[1]][[1]], collapse="") != paste(subTool[[1]], collapse="")) {
        subTool <- unlist(subTool, recursive=F)
      }
      collectTopics[[unlist(currTool$name)]] <- sapply(subTool, function(x) {y<-unlist(x[[tags[1]]]);names(y) <- unlist(x[[tags[2]]]);sort(y)})
    }
  }
  collectTopics
}

#collectTopics <- extractStats(AllTools, "function", "operation")
#collectTopics <- extractStats(AllTools, "function","input", "format")
collectTopics <- extractStats(AllTools, "license", tags = c(1,1))
## Annotation depth: Number of tools with how many terms
anno_depth <- sapply(collectTopics, length)
hist(anno_depth, c(0:(max(anno_depth)+1))-0.5, border=0, xlab="completeness")



## Making wordcloud of topics
edam_stats <- table(unlist(collectTopics))
## Most used terms
barplot(sort(edam_stats, decreasing=T)[1:30], las=2, border=0, cex.names = 0.9)
edam_stats <- data.frame(topic=names(edam_stats), freq=as.vector(edam_stats))
edam_stats[,2] <- sqrt(edam_stats[,2])

my_graph <- wordcloud2(edam_stats, size=0.5, shape="pentagon")
my_graph


## Looking for cooccurrences and making a relationship graph
library(cooccur)
library(visNetwork)
rel <- matrix(0,nrow=length(collectTopics), ncol=length(unique(unlist(collectTopics))))
colnames(rel) <- (unique(unlist(collectTopics)))
rownames(rel) <- names(collectTopics)
for (i in 1:length(collectTopics)) {
  if (length(unlist(collectTopics[[i]])) > 0)
    rel[i, collectTopics[[i]]] <- 1
}
rel <- rel[rowSums(rel) > 0,]
rel <- rel[,colSums(rel) > 10]

heatmap(rel, scale="none")
mydist <- function(data) { dist(data, method="binary")}
heatmap(rel, dist=mydist, scale="none", cexCol = 0.6)

co <- print(cooccur(rel, spp_names = TRUE))

# Create a data frame of the nodes in the network. 
nodes <- data.frame(id = 1:nrow(rel),
                    label = rownames(rel),
                    color = "#60642",
                    shadow = TRUE)

heatmap(as.matrix(dist(rel, method="binary")), scale="none")


## Comparison purposes
randTools <- fullToolContent[sample(1:length(fullToolContent), size=10000)]
#collectTopics <- extractStats(randTools, "function","input", "format")
collectTopics <- extractStats(randTools, "language", tags=c(1,1))
# Find significant pairwise co-occurrences.



