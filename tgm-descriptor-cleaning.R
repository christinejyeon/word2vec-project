setwd("/Users/Christine/Documents/everyday-practice-r")

tgmfile <- read.delim("tgm1.xml")
# tgmfile1 <- read.delim("tgm1.txt")

names(tgmfile)[1] <- "Description"
tgmfile$Description <- as.character(tgmfile$Description)
tgmfile$Description <- gsub("^ ", "", tgmfile$Description)
tgmfile <- subset(tgmfile, (substr(Description,1,4)=="<NON")|(substr(Description,1,4)=="<DES"))
tgmfile$Description <- gsub("^<NON-DESCRIPTOR>","", tgmfile$Description)
tgmfile$Description <- gsub("^<DESCRIPTOR>","", tgmfile$Description)

# tgmfile$Description <- ifelse(substr(tgmfile$Description,1,4)=="<NON",gsub("<NON-DESCRIPTOR>","", tgmfile$Description), gsub("<DESCRIPTOR>","",tgmfile$Description))
tgmfile$Description <- gsub("</NON-DESCRIPTOR>$","",tgmfile$Description)
tgmfile$Description <- gsub("</DESCRIPTOR>$","",tgmfile$Description)
