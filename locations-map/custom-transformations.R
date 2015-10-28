# Custom transformations of clinics data frame. 
# This file will be sourced after HTML files are read, but before JSON is written
# The idea is that these transformations are likely to be dataset-dependent,
# so it makes sense to make it as easy as possible to plug them out and plug
# something else instead

# Some addresses contain room number - drop it
clinics$Address <- gsub("/P\\.[0-9]+", "", clinics$Address)

# Strip excessive whitespace characters
clinics <- as.data.frame(sapply(clinics, gsub, pattern="\\s+", replacement=" "),
                         stringsAsFactors=FALSE)

# Clean up phone numbers
clinics$Phone <- sub("Telefon: ", "", clinics$Phone, fixed=TRUE)
clinics$Phone <- gsub("[^0-9,]", "", clinics$Phone)
