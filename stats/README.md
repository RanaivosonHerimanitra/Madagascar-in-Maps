# Real time data monitor:

The aims of this project is to build a real time data pipeline to monitor and
visualize crimes committed in Madagascar but also demands and job offers,
flood events, market share of online sells among many others ,preferably,
disaggregated by administrative area.
By real time, I mean, data are continuously scraped from links over the web.

Scripts have been dispatched in 02 instances on AWS. They are continuously reading links
over the web and writing in a RDS on this same cloud platform.
We may need more instances on the future to mimic this real time...

# Roadmap:

* Set up the cloud platform with the database==>DONE
* Update all codes to deal with the database==>DONE
* Data Quality assessments: duplicates, dates of appearance, locations knowing that same name may belongs to different locations,Number of (crimes) in a given page report
* Test bugs and potential errors with scripts
* Set up the platform for visualizing data (current option: R/shiny)
* Invite interested developers to join the project
* Make this repository private after the first release of the dataviz platform
* Promote the application to interested policymakers and NGOs.
