# Main file that will parse HTML files in this directory and create JSON with data
library("ggmap")
library("rjson")

source("./read-data.R")

clinics <- do.call("rbind",
                   lapply(list.files("./", "poradnie"), read_clinics_file))
clinics <- as.data.frame(clinics, stringsAsFactors=FALSE)

source("./custom-transformations.R")

coordinates <- geocode(clinics$Address, source="google")
clinics <- cbind(clinics, coordinates)

writeLines(toJSON(clinics), "./clinics.json")