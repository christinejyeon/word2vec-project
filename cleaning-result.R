### Using R from here
tag_tgm_similarity <- read.csv("tag_tgm_similarity.csv")
names(tag_tgm_similarity) <- "first"
tag_tgm_similarity$second <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 3)
tag_tgm_similarity$third <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 4)
tag_tgm_similarity$fourth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 5)
tag_tgm_similarity$fifth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 6)
tag_tgm_similarity$sixth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 7)
tag_tgm_similarity$seventh <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 8)
tag_tgm_similarity$eighth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 9)
tag_tgm_similarity$ninth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 10)
tag_tgm_similarity$tenth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 11)
tag_tgm_similarity$eleventh <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 12)
tag_tgm_similarity$twelfth <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 13)
tag_tgm_similarity$first <- sapply(strsplit(as.character(tag_tgm_similarity$first),'\t'), "[", 2)

tgmvectors <- read.csv("tgmvectors_horizontal.csv")
names(tgmvectors) <- "temp"
tgmvectors$tgmname <- sapply(strsplit(as.character(tgmvectors$temp),'\t'), "[", 2)
tgmvectors$temp <- NULL
tag_tgm_similarity <- cbind(tgmvectors, tag_tgm_similarity)

tagrepnames <- read.csv("ultimate_rep.csv")
names(tagrepnames) <- "temp"
tagrepnames$tagrepname <- sapply(strsplit(as.character(tagrepnames$temp),'\t'), "[", 2]
names(tag_tgm_similarity)[2:13] <- tagrepnames$tagrepname
