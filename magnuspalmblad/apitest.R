library(jsonlite)
library(stringr)

tool <- fromJSON('https://bio.tools/api/tool/LimmaRP') # fetch bio.tools record

name <- tool$credit$name[2] # extract name

firstName <- unlist(str_split(name, ' '))[1] # extract first name

genderize <- fromJSON(paste('https://api.genderize.io/?name=', firstName, sep=''))

male <- 0
female <- 0

if(genderize$gender=='male' && genderize$probability>0.66) male=male+1
if(genderize$gender=='female' && genderize$probability>0.66) female=female+1
