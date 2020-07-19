#!/bin/bash
ROOT_HTML_DIR="./whose/"
MARKDOWN_DIR="./markdown/"
PROCESSED_HTMLS="$(mktemp -d)"

echo "Downloading WHOSE website"
httrack "http://whose.associationforsoftwaretesting.org/index.php?title=Main_Page" -O "$ROOT_HTML_DIR" "+*index.php?title=*" "-*action=*" "-*Special:*" "-*&printable=*" "-*User_talk*" "-*oldid=*" "-*User:*" -v -N "web/%[title].html"

echo "Removing redundant files"
rm -- "$ROOT_HTML_DIR/web/.html" "$ROOT_HTML_DIR"/web/\-*.html

echo "Removing recurring fragments from HTML files"
python3 ./process-pages.py -i "$ROOT_HTML_DIR/web/" -o "$PROCESSED_HTMLS"

echo "Converting HTML to markdown"
mkdir "$MARKDOWN_DIR" 2>/dev/null

for html in "$PROCESSED_HTMLS"/*.html; do
    pandoc -f html -t markdown-escaped_line_breaks-header_attributes "$html" |grep -v '^:::' > "$MARKDOWN_DIR/$(basename "$html" .html).md"
done
