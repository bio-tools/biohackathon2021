library(jsonlite)
library(igraph)
library(RCy3)
library(GraphAlignment)

# This is still work in progress, but does construct an igraph object from a bio.tools
# tool function description and uploads this to Cytoscape, as a single network or a
# collection of networks with one network per bio.tools function.

tool <- read_json('https://bio.tools/api/tool/?biotoolsID="hmmer3"&format=json&page=1')$list

G <- make_empty_graph()

nNodes <- 0
for(i in 1:length(tool[[1]]$`function`)) {
  nInputs <- 0; nOperations <- 0; nOutputs <- 0
  if(length(tool[[1]]$`function`[[i]]$input)>0) {
    for(j in 1:length(tool[[1]]$`function`[[i]]$input)) {
     G <- add.vertices(G, 1, 
                        type = 'input',
                        term = tool[[1]]$`function`[[i]]$input[[j]]$data$term,
                        uri = tool[[1]]$`function`[[i]]$input[[j]]$data$uri)
      nInputs <- nInputs + 1
    }
  }

  if(length(tool[[1]]$`function`[[i]]$operation)>0) {
    for(j in 1:length(tool[[1]]$`function`[[i]]$operation)) {
      G <- add.vertices(G, 1, 
                        type = 'operation',
                        term = tool[[1]]$`function`[[i]]$operation[[j]]$term,
                        uri = tool[[1]]$`function`[[i]]$operation[[j]]$uri)
      nOperations <- nOperations + 1
    }
  }

  if(length(tool[[1]]$`function`[[i]]$output)>0) {
    for(j in 1:length(tool[[1]]$`function`[[i]]$output)) {
      G <- add.vertices(G, 1, 
                        type = 'output',
                        term = tool[[1]]$`function`[[i]]$output[[j]]$data$term,
                        uri = tool[[1]]$`function`[[i]]$output[[j]]$data$uri)
      nOutputs <- nOutputs + 1
    }
  }
  
  if(nInputs>0) {
    for(i in 1:nInputs) {
      for(j in 1:nOperations) G <- add.edges(G, nNodes+c(i,nInputs+j))
    }
  }
  
  if(nOutputs>0) {
    for(i in 1:nOperations) {
      for(j in 1:nOutputs) G <- add.edges(G, nNodes+c(nInputs+i,nInputs+nOperations+j))
    }
  }
  nNodes <- nNodes + nInputs + nOperations + nOutputs
}

createNetworkFromIgraph(G, title="From igraph")

dG <- decompose.graph(G)

for(i in 1:length(dG)) {
  createNetworkFromIgraph(dG[[i]], title = paste('Subgraph', i))
}

attributes(G)
