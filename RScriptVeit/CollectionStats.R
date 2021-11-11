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


##### Random selection of tools for comparison purposes
RandTools <- fullToolContent[sample(1:length(fullToolContent), size=10000)]

##### Citation counts for all tools
pubs <- tt <- c()
for(i in 1:length(fullToolContent)) {
  if(length(fullToolContent[[i]]$publication)>0) {
    pmid <- fullToolContent[[i]]$publication[[1]]$pmid
    pubs <- cbind(pubs, pmid)
    if (length(pmid) == 1)
      tt <- c(tt, fullToolContent[[i]]$biotoolsID)
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
rciteCount <- sapply(pubMedResults, function(x) x$citedByCount)



################## Here we define the use cases ############
#usecase <- "https://bio.tools/api/t?topic='Metabolomics'&format=json"
#usecase <- "https://bio.tools/api/t?topic='Proteomics'&format=json"
#usecase <- "https://bio.tools/api/t?topic='RNA-Seq'&format=json"
#usecase <- "https://bio.tools/api/t?q=cryo-em&format=json"
usecase <- "https://bio.tools/api/t?q=disordered&format=json"

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
extractStats <- function(toolSet, termname=NULL, tags=c("term","uri")) {
  collectTopics <- list()
  for (i in 1:length(toolSet)) {
    currTool <- toolSet[[i]]
    subTool <- NULL
    if (is.null(termname)) {
      subTool <- currTool
    } else if (length(termname) == 1) {
      subTool <- currTool[[termname]]
    } else if (length(termname) == 2) {
      if (length(currTool[[termname[1]]]) > 0) {
        subTool <- lapply(currTool[[termname[1]]], function(x) x[[termname[2]]])
      } else {
        subTool <- NULL
      }
    } else {
      if (length(currTool[[termname[1]]]) > 0) {
        if (length(currTool[[termname[1]]][[1]][[termname[2]]]) > 0) {
          subTool <- lapply(currTool[[termname[1]]], function(x) lapply(x[[termname[2]]], function(y) y[[termname[3]]]))
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
simpleStats <- function(collection, title, rand=NULL) {
  ## Annotation depth: Number of tools with how many terms
  anno_depth <- sapply(collectTopics, length)
  rand_depth <- sapply(rand, length)
  max_w <- (max(anno_depth,rand_depth)+1)
  p_anno_depth <- hist(anno_depth, c(0:max_w)-0.5, plot=F)
  p_rand_depth <- hist(rand_depth, c(0:(max_w+1))-0.5, plot=F)
  p_rand_depth$counts <- p_rand_depth$counts/length(randTopics) * length(collectTopics)
  plot(p_anno_depth,xlim=c(0,max_w+1)-0.5, border=0, xlab="completeness", main=paste0(title," Number of terms per tool"),
       col="#B05544")
  plot(p_rand_depth, add=T, xlim=c(0,(max_w+1))-0.5, border=NA, col="#33333355")
  
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
  saveWidget(my_graph,"tmp.html",selfcontained = F, title=title)
  webshot2::webshot("tmp.html",file = paste0(title," wordcloud.pdf"), delay =20, vwidth = 1000, vheight=1000)
  
  
  ## Looking for cooccurrences and making a relationship graph
  # library(cooccur)
  # library(visNetwork)
  # rel <- matrix(0,nrow=length(collectTopics), ncol=length(unique(unlist(collectTopics))))
  # colnames(rel) <- (unique(unlist(collectTopics)))
  # rownames(rel) <- names(collectTopics)
  # for (i in 1:length(collectTopics)) {
  #   if (length(unlist(collectTopics[[i]])) > 0)
  #     rel[i, collectTopics[[i]]] <- 1
  # }
  # rel <- rel[rowSums(rel) > 0,]
  # rel <- rel[,colSums(rel) > 10]
  # 
  #heatmap(rel, scale="none", main=title)
  #mydist <- function(data) { dist(data, method="binary")}
  #heatmap(rel, dist=mydist, scale="none", cexCol = 0.6, main=title)
  
  #co <- print(cooccur(rel, spp_names = TRUE))
  
  # Create a data frame of the nodes in the network. 
  # nodes <- data.frame(id = 1:nrow(rel),
  #                     label = rownames(rel),
  #                     color = "#60642",
  #                     shadow = TRUE)
  # 
  #heatmap(as.matrix(dist(rel, method="binary")), scale="none")
}

alledamtypes <- list("topic", c("function", "operation"), c("function", "input", "format"), 
                     c("function", "output", "format"), c("function", "input", "data"), 
                     c("function", "output", "data"))
allnamings <- c("Topic", "Operation", "Input format", "Output format", "Input data", "Output data")
## select term types
for (i in 1:length(alledamtypes)) {
  collectTopics <- extractStats(AllTools, alledamtypes[[i]])
  randTopics <- extractStats(RandTools, alledamtypes[[i]])
  simpleStats(collectTopics, allnamings[i], rand=randTopics)
}

allothertypes <- c("license","toolType","operatingSystem")
for (term in allothertypes) {
  collectTopics <- extractStats(AllTools, term, tags = c(1,1))
  randTopics <- extractStats(RandTools, term, tags= c(1,1))
  simpleStats(collectTopics, term, rand=randTopics)
}



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
citeCount <- sapply(pubMedResults, function(x) x$citedByCount)
x <- hist(citeCount, 0:max(citeCount), main=paste("Citations"), xlab="Citations", probability = T)
y <- hist(rciteCount, 0:max(rciteCount), main=paste("Citations"), xlab="Citations", plot=F, probability = T)
plot(y$mids, y$density, log="xy", type="l", main=paste("log-log plot of citation count"), 
     xlab="Citations", ylab="Counts", col="#33333355")
lines(x$mids, x$density, log="xy", type="l",col="#AA5533", add=T)
text(10,10,sum(citeCount))
lines(x, 3*x^-1.8)

#write.table(titlesAbstracts, "PubMed_genomics.txt", row.names=F, col.names=F)


### OpenEBench
metrics <- NULL
for (i in sapply(AllTools, function(x) x$biotoolsID)) {
  print(i)
  metrics[[i]] <- read_json(paste0("https://openebench.bsc.es/monitor/metrics/", tolower(i)))
}
length(metrics)
barplot(table(as.numeric(sapply(metrics, function(x) x$project$website$https))),  main="Is https page")
hist(sapply(metrics, function(x) x$project$website$operational), 100, main="Operational web page", xlab="")

sourcecode <- lapply(metrics, function(x) if (!is.null(x$distribution$sourcecode)) names(which(unlist(x$distribution$sourcecode))))
barplot(table(unlist(sourcecode)), las=2, main="Source code")

issuetracker <- lapply(metrics, function(x) if (!is.null(x$support) & all(is.logical(unlist(x$support)))) names(which(unlist(x$support))))
barplot(table(unlist(issuetracker)), las=2, main="Issue tracker")

