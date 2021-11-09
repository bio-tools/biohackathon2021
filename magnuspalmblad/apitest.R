library(jsonlite)
library(stringr)

# N.B. This R script attempts to extract gender bias in the people credited
# in the bio.tools entries in different topics or tool collections. In doing
# this we are limited to the male/female genders as called by genderize.io from
# the first names only. This is in no way an endorsement of gender as a binary
# variable. Also importantly, the script does not store or report genders of
# individual contributors, only aggregate statistics.

tool <- fromJSON('https://bio.tools/api/tool/LimmaRP') # fetch bio.tools record

name <- tool$credit$name[2] # extract name

firstName <- unlist(str_split(name, ' '))[1] # extract first name

genderize <- fromJSON(paste('https://api.genderize.io/?name=', 
                            firstName, sep=''))

male <- 0
female <- 0

if(genderize$gender=='male' && genderize$probability>0.66) male=male+1
if(genderize$gender=='female' && genderize$probability>0.66) female=female+1
