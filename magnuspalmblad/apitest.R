library(jsonlite)
library(stringr)

# N.B. This R script attempts to extract gender bias in the people credited
# in the bio.tools entries in different topics or tool collections. In doing
# this we are limited to the male/female genders as called by genderize.io from
# the first names only. This is in no way an endorsement of gender as a binary
# variable. Also importantly, the script does not store or report genders of
# individual contributors, only aggregate statistics.

# fetch bio.tools records
tools <- read_json('https://bio.tools/api/tool/?topic=genomics&format=json&page=1')$list

for(i in 2:10) {tools <- c(tools, read_json(
              paste0('https://bio.tools/api/tool/?topic=genomics&format=json&page=',i))$list)
}

male <- 0
female <- 0

for(i in 1:length(tools)) {
  if(length(tools[[i]]$credit)>0) {
    name <- tools[[i]]$credit[[1]]$name
    firstName <- unlist(str_split(name, ' '))[1] 
    if(is.null(firstName) == FALSE) {
      genderize <- fromJSON(paste('https://api.genderize.io/?name=', 
                                firstName, sep=''))
      if(genderize$gender=='male' && genderize$probability>0.66) male=male+1
      if(genderize$gender=='female' && genderize$probability>0.66) female=female+1
    }
  }
}

# topic=metabolomics: 20.3% female (16 female, 63 male)
# topic=proteomics: 11.8% female (10 female, 75 male)
# topic-genomics: 19.5% female (16 female, 66 male)
