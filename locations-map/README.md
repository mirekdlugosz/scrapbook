This tool helped me to find clinic in my close neighborhood. I had to register to new doctor when I moved to new flat. NFZ (public funder of health care here in Poland) provides [web-based clinics search engine](https://zip.nfz.gov.pl/GSL/GSL/POZ), but for some reason "Map" tab does not work on my computer. Instead of manually searching every clinic, I decided to mark all clinics in my neighborhood on single map.

On technical level, it uses R to extract data from HTML file, clean it up a bit and export it to JSON. Website reads that JSON and creates map with markers. Markers are click-able - popover window displays name, address, phone number and opening hours (in case that closest clinic has insane working hours).

Query results from NFZ database are put in `poradnie[1-5].html` files. Results on website are loaded dynamically and there is no easy way to get them from R directly.

R code is my own, but website is modified version of [Live Earthquake Map](http://r-video-tutorial.blogspot.com/2015/05/live-earthquake-map-with-shiny-and.html).
