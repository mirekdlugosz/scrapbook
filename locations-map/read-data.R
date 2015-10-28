# Functions to read HTML file with clinics data
library("xml2")

read_clinics_file <- function(file=NULL, encoding="UTF-8") {
  data <- read_html(file, encoding = encoding)
  clinics <- xml_find_all(data, "//div[@class='ResultContnet']")
  clinics <- lapply(clinics, .parse_clinic_node)
  do.call("rbind", clinics)
}

.parse_clinic_node <- function(node) {
  content <- xml_text(xml_find_one(node, ".//div[@class='BasicInfo']"), 
                      trim=TRUE)
  content <- unlist(strsplit(content, "\n", fixed = TRUE))
  content <- gsub("^\\s+|\\s+$", "", content)
  name <- content[1]
  address <- content[grep("ul.", content, fixed = TRUE)]
  if (! length(address)) return()
  phone <- content[grep("Telefon", content, fixed = TRUE)]
  
  days <- xml_text(xml_find_all(node, ".//div[@class='TTDay']"), TRUE)
  hours <- xml_text(xml_find_all(node, ".//div[@class='TTHours']"), TRUE)
  
  results <- c(name, address, phone, hours)
  names(results) <- c("Name", "Address", "Phone", days)
  results
}