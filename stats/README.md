# Real time data monitor:

The aims of this project is to build a real time data pipeline to monitor and visualize crimes committed in Madagascar but also demands and job offers, flood events... disaggregated by administrative area. By real time, I mean, data are continuously scraped from links over the web.

Scripts divided in 02 instances are continuously reading and writing in a RDS database on AWS.
May need more instances on the future to mimic and achieve real time...

# TODOS:

* Data Quality assessments: duplicates, dates of appearance, locations knowing that same name may belongs to different locations,Number of (crimes) in a given page report
* set up the cloud with the database==>DONE
* update all codes to deal with the database==>DONE
* Test bugs and potential errors with scripts
* set up the platform for visualizing data (current option: R/shiny)
