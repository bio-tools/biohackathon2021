library(jsonlite)
library(stringr)
library(ggplot2)
library(forcats)
library(ggsci)
library(europepmc)

# This is just a sandbox created during BioHackathon 2021

# Example 1: get first credited person for 100 top tools for certain EDAM topic,
# extract and genderize first names, and visually compare topics. 
# N.B. This R script attempts to extract gender bias in the people credited
# in the bio.tools entries in different topics or tool collections. In doing
# this we are limited to the male/female genders as called by genderize.io from
# the first names only. This is in no way an endorsement of gender as a binary
# variable. Also importantly, the script does not store or report genders of
# individual contributors, only aggregate statistics.

# fetch bio.tools records:
tools <- read_json('https://bio.tools/api/tool/?topic="biodiversity"&format=json&page=1')$list

for(i in 2:8) {tools <- c(tools, read_json(
              paste0('https://bio.tools/api/tool/?topic="biodiversity"&format=json&page=',i))$list)
}

male <- 0
female <- 0
unknown <- 0

for(i in 1:length(tools)) {
  if(length(tools[[i]]$credit)>0) {
    name <- tools[[i]]$credit[[1]]$name
    firstName <- unlist(str_split(name, ' '))[1] 
    if(is.null(firstName) == FALSE) {
      genderize <- fromJSON(paste('https://api.genderize.io/?name=', 
                                firstName, sep=''))
      if(genderize$gender=='male' && genderize$probability>0.66) male=male+1
      if(genderize$gender=='female' && genderize$probability>0.66) female=female+1
      if(genderize$probability<=0.66) unknown=unknown+1
    }
  }
}

# topic=proteomics: 14 female, 74 male, 7 unknown (100+ hits)
# topic=metabolomics: 13 female, 59 male, 11 unknown (100+ hits)
# topic-genomics: 15 female, 67 male, 15 unknown (100+ hits)
# topic-biodiversity: 8 female, 33 male, 17 unknown (76 hits)

df <- data.frame(topic=c(rep('biodiversity',3), rep('genomics',3),
                         rep('proteomics',3), rep('metabolomics',3)),
                 gender=rep(c('female', 'unknown', 'male'),4),
                 sorting=c(1,1,1,1,2,2,2,2,3,3,3,3),
                 credits=c(8*100/76,17*100/76, 33*100/76,
                           15,15,67,
                           14,7,74,
                           13,11,59))
ggplot(data=df, aes(x=topic, y=credits, fill=fct_reorder(df$gender, df$sorting))) +
  geom_bar(stat="identity") +
  xlab('EDAM topic') +
  ylim(c(0,100)) +
  ylab("credits/100 bio.tools tools") +
  labs(fill='genderized') +
  scale_fill_startrek()


# Example 2: get first (main) publication for all bio.tools records with topic="proteomics"
# and use EuropePMC API to retrieve titles and abstracts for text mining.

count <- read_json('https://bio.tools/api/tool/?topic="proteomics"&format=json')$count
tools <- read_json('https://bio.tools/api/tool/?topic="proteomics"&format=json&page=1')$list

for(i in 2:round(0.5+count/10)) {tools <- c(tools, read_json(
  paste0('https://bio.tools/api/tool/?topic="proteomics"&format=json&page=',i))$list)
}

pubs <- c()
for(i in 1:length(tools)) {
  if(length(tools[[i]]$publication)>0) {
    pmid <- tools[[i]]$publication[[1]]$pmid
    pubs <- cbind(pubs, pmid)
  }
}

# write.table(as.numeric(pubs), "proteomics_pmids.txt", row.names=F, col.names=F)

titlesAbstracts <- ''
for(i in 1:length(pubs)) {
  pubMedResults <- epmc_search(paste0(query = 'EXT_ID:', pubs[i], '&resultType=core'))
  titlesAbstracts <- paste0(titlesAbstracts, pubMedResults$title, pubMedResults$abstractText, '\n')
}
write.table(titlesAbstracts, "PubMed_proteomics.txt", row.names=F, col.names=F)
