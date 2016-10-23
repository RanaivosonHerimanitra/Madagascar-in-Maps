# Crimes mapping project:

The aims of this project is to build a real time data pipeline to visualize crime events in Madagascar disaggregated by administrative area. By real time, I mean, data are continously scraped from links over the web.


* Step0 : Define a set of websites from which you are going to retrieve links : `bash 1_link_constitution.sh`

* Step1: Search for other links inside the links previously acquired to gain either `bash 2_download_links.sh "data/all_page.csv" "data/base_links.sh"` or `bash 2_download_links.sh "data/base_links.csv" "data/base_links.sh"`

They should both run in the same time and continiously read and write in a database (example: postgresql)
