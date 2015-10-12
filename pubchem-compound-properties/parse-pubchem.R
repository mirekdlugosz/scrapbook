library("xml2")
library("data.table")

compound.attributes <- function(file=NULL) {
  compound <- read_xml(file)
  ns <- xml_ns(compound)
  information <- xml_find_all(compound, paste0(
    "//d1:TOCHeading[text()='Computed Descriptors'",
    " or text()='Other Identifiers'",
    " or text()='Synonyms'",
    " or text()='Computed Properties']",
    "/following-sibling::d1:Section/d1:Information"
  ), ns)
  
  properties <- sapply(information, function(x) {
    name <- xml_text(xml_find_one(x, "./d1:Name", ns))
    value <- ifelse(length(xml_find_all(x, "./d1:StringValueList", ns)) > 0,
                    paste(sapply(
                      xml_find_all(x, "./d1:StringValueList", ns),
                      xml_text, trim=TRUE), sep="", collapse="|"),
                    xml_text(
                      xml_find_one(x, "./*[contains(name(),'Value')]", ns),
                      trim=TRUE)
    )
    names(value) <- name
    return(value)
  })
  rm(compound, information)
  properties <- as.list(properties)
  properties$pubchemid <- sub(".*/([0-9]+)/?.*", "\\1", file)
  return(data.frame(properties))
}

compound.retention.index <- function(file=NULL) {
  pubchemid <- sub(".*/([0-9]+)/?.*", "\\1", file)
  compound <- read_xml(file)
  ns <- xml_ns(compound)
  information <- xml_find_all(compound, paste0(
    "//d1:TOCHeading[text()='Kovats Retention Index']",
    "/following-sibling::d1:Information"
  ), ns)
  indexes <- lapply(information, function(x) {
    name <- xml_text(xml_find_one(x, "./d1:Name", ns))
    values <- as.numeric(sapply(
      xml_find_all(x, "./*[contains(name(), 'NumValue')]", ns), 
      xml_text))
    
    data.frame(pubchemid=pubchemid,
               column_class=name,
               kovats_ri=values)
  })
  
  return( do.call("rbind", indexes) )
}

compounds <- c("./5282108.xml", "./5282148.xml", "./91754124.xml")

cd <- rbindlist(
  lapply(compounds, compound.attributes),
  fill=TRUE
)

rti <- do.call("rbind",
               lapply(compounds, compound.retention.index))