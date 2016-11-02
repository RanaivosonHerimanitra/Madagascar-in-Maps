# Real time data monitor:

The aims of this project is to build a real time data pipeline to monitor and visualize crimes committed in Madagascar but also demands and job offers, flood events, market share of online sell among many others disaggregated by administrative area.
By real time, I mean, data are continuously scraped from links over the web.

Scripts are divided in 02 instances are continuously reading and writing in a RDS database on AWS.
May need more instances on the future to mimic and achieve real time...

# TODOS:

* Data Quality assessments: duplicates, dates of appearance, locations knowing that same name may belongs to different locations,Number of (crimes) in a given page report
* Set up the cloud with the database==>DONE
* Update all codes to deal with the database==>DONE
* Test bugs and potential errors with scripts
* Set up the platform for visualizing data (current option: R/shiny)
* Invite interested developers to join the project
* Make this repository private after the first release of the dataviz platform
