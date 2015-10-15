library("stringr")

singles_file <- readLines("./sample-data.txt")

file_from <- grep("^TW", singles_file) + 2
file_to <- grep("UNDER THE HOT 100", singles_file) - 2

singles_file <- singles_file[file_from:file_to]
delimiters <- grepl("------", singles_file, fixed = TRUE)
singles_file <- singles_file[! delimiters]

parse_record <- function(x) {
  if (length(x)) {
    begin <- grepl("^\\t\\s{5}\\S", x)
    begin[1] <- TRUE
    x <- gsub("^\\s+|\\s+$", "", x)
    x <- c(
      paste(x[begin], collapse = " "),
      paste(x[!begin], collapse = " ")
    )
  }
  first <- unlist(strsplit(x[1], "\\s{2,}"))
  second <- str_match(x[2],
                      paste0("\\s*(.*)",
                             " \\((.*)\\)-([0-9]+)",
                             ".*",
                             " \\(([0-9]+)\\)"))[,-1]
  return(c(first, second))
}

parsed <- tapply(singles_file, 
                 cumsum(grepl("^\\s?[0-9]", singles_file)),
                 parse_record)

parsed <- unlist(parsed)
singles <- matrix(parsed, ncol = 7, byrow = TRUE)
singles <- data.frame(singles, stringsAsFactors = FALSE)

singles[, c(1,2,6,7)] <- lapply(singles[, c(1,2,6,7)], as.numeric)
colnames(singles) <- c("this.week", "last.week", "title",
                       "artist", "label", "weeks.on.chart",
                       "peak.position")
