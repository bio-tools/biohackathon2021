library(europepmc)
library(jsonlite)
library(eulerr)
library(dplyr)
library(wordcloud2)
library(webshot2)
library(htmlwidgets)


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
fullToolContent <- read_json("bio.toolsFullDump.json")


### Getting all tool names
fullToolNames <- read_json("bio.toolsFullDump.json")
fullToolNames <- unlist(sapply(fullToolNames, function(x) x$name[[1]]))


################## Here we define the use cases ############
usecase <- "https://bio.tools/api/t?topic='Proteomics'&format=json"
#usecase <- "https://bio.tools/api/t?q=cryo-em&format=json"

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


### function to create simple stat figures
simpleStats <- function(collection, title) {
  ## Annotation depth: Number of tools with how many terms
  anno_depth <- sapply(collectTopics, length)
  hist(anno_depth, c(0:(max(anno_depth)+1))-0.5, border=0, xlab="completeness", main=paste0(title," Number of terms per tool"))
  
  
  
  ## Making wordcloud of topics
  edam_stats <- table(unlist(collectTopics))
  ## Most used terms
  selected_terms <- sort(edam_stats, decreasing=T)[1:30]
  x <- barplot(selected_terms, las=2, border=0, xaxt="none", main=paste(title," Top 30 terms"))
  text(cex=0.7, x=x+0.85, y=-0.5, names(selected_terms), xpd=TRUE, srt=45, pos=2)
  edam_stats <- data.frame(topic=names(edam_stats), freq=as.vector(edam_stats))
  edam_stats[,2] <- sqrt(edam_stats[,2])
  
  my_graph <- wordcloud2(edam_stats, size=0.4, shape="pentagon")
  my_graph
  saveWidget(my_graph,"tmp.html",selfcontained = F)
  webshot2::webshot("tmp.html",file = paste0(title," wordcloud.pdf"), delay =20, vwidth = 1000, vheight=1000)
  
  
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
  
  heatmap(rel, scale="none", main=title)
  mydist <- function(data) { dist(data, method="binary")}
  heatmap(rel, dist=mydist, scale="none", cexCol = 0.6, main=title)
  
  #co <- print(cooccur(rel, spp_names = TRUE))
  
  # Create a data frame of the nodes in the network. 
  nodes <- data.frame(id = 1:nrow(rel),
                      label = rownames(rel),
                      color = "#60642",
                      shadow = TRUE)
  
  heatmap(as.matrix(dist(rel, method="binary")), scale="none")
}


## select term types
collectTopics <- extractStats(AllTools, "topic")
simpleStats(collectTopics, "Topic")
collectTopics <- extractStats(AllTools, "function", "operation")
simpleStats(collectTopics, "Operation")
collectTopics <- extractStats(AllTools, "function","input", "format")
simpleStats(collectTopics, "Input format")
collectTopics <- extractStats(AllTools, "function","output", "format")
simpleStats(collectTopics, "Output format")
collectTopics <- extractStats(AllTools, "function","input", "data")
simpleStats(collectTopics, "Input data")
collectTopics <- extractStats(AllTools, "function","output", "data")
simpleStats(collectTopics, "Output data")
collectTopics <- extractStats(AllTools, "license", tags = c(1,1))
simpleStats(collectTopics, "license")
collectTopics <- extractStats(AllTools, "toolType", tags = c(1,1))
simpleStats(collectTopicsm, "tool type")
collectTopics <- extractStats(AllTools, "operatingSystem", tags = c(1,1))
simpleStats(collectTopics, "operating system")




###### Running stats on citation counts
pubs <- tt <- c()
for(i in 1:length(AllTools)) {
  if(length(AllTools[[i]]$publication)>0) {
    pmid <- AllTools[[i]]$publication[[1]]$pmid
    pubs <- cbind(pubs, pmid)
    if (length(pmid) == 1)
      tt <- c(tt, AllTools[[i]]$biotoolsID)
  }
}
names(pubs) <- tt
titlesAbstracts <- ''
pubMedResults <- list()
for(i in 1:length(pubs)) {
  print(i)
  pubMedResults[[names(pubs)[i]]] <- epmc_search(paste0(query = 'EXT_ID:', pubs[i], '&resultType=core'))
  titlesAbstracts <- paste0(titlesAbstracts, pubMedResults$title, pubMedResults$abstractText, '\n')
}

# distribution of citations
citeCount <- sapply(pubMedResults, function(x) x$citedByCount, main=paste(title,"Citations"))
x <- hist(citeCount, 0:max(citeCount))
plot(x$mids, x$counts, log="xy", type="h", main=paste(title,"log-log plot of citation count"))
text(10,10,sum(citeCount))

#write.table(titlesAbstracts, "PubMed_genomics.txt", row.names=F, col.names=F)



##### Random selection of tools for comparison purposes
AllTools <- fullToolContent[sample(1:length(fullToolContent), size=10000)]
# Find significant pairwise co-occurrences.



### OpenEBench

metrics <- NULL

for (i in sapply(AllTools, function(x) x$biotoolsID)) {
  print(i)
  metrics[[i]] <- read_json(paste0("https://openebench.bsc.es/monitor/metrics/", tolower(i)))
}
length(metrics)
