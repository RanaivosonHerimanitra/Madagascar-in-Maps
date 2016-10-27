# Real time data monitor:

The aims of this project is to build a real time data pipeline to monitor and visualize crimes committed in Madagascar but also demands and job offers, flood events... disaggregated by administrative area. By real time, I mean, data are continuously scraped from links over the web.


* Step0: Define a set of websites from which you are going to retrieve links : `bash 1_link_constitution.sh`

* Step1: Search for other links inside the links previously acquired to gain more depth and reach more links either

`bash 2_download_links.sh "data/all_page.csv" "data/base_links.sh"`  or

`bash 2_download_links.sh "data/base_links.csv" "data/base_links.sh"`

* Step3: Query specific pages because they have well defined syntax for GET request in order to attain archives.

`bash 3_query_pages.sh`

* Step4: Filter collected links with keywords (in .csv but should be in a database). Should also listen to new keywords in production environment:

`bash 4_page_filtering.sh`


They should both run at the same time and  continuously read and write in a database (example: postgresql preferably in a cloud environment: current choice: AWS).

## TODOS:

* Data Quality assessments: duplicates, dates of appearance, locations knowing that same name may belongs to different locations,Number of (crimes) in a given page report
* set up the cloud with the database
* update all codes to deal with the database
* set up the platform for visualizing data (current option: R/shiny)
