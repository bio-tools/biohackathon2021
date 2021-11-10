library(jsonlite)

A <- read_json("https://bio.tools/api/t?format=json&page=1")
num_tools <- A$count

#Full dump, takes time
for (i in 1628:(num_tools/10)) {
  AllTools <- c(AllTools, read_json(paste0("https://bio.tools/api/t?format=json&page=",i))$list)  
     
  }
length(AllTools)
