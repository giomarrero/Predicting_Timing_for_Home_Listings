# Predicting Time on the Market for New Home Listings

## Description

Welcome to our (Team 21's) Github! This contains the summary of our efforts in MGT 6203's group project. We tackled attempting to model Median Time on the Market sourced from Realtor.com's data using a wide variety of data sources as well as a few different modeling approaches. 

## Directory Structure

Critical folders in the directory structure are Code/data_eng for ETL.ipynb, and then Code/models for all_models_compare.ipynb. Incremental versions of work can be found in our various branches, but those are the two notebooks that are needed to replicate our work. A final, downloadable, .html version of our final notebook can be found in the Final Reports directory.

## How To Replicate our results 

Please run each of the below files in a Jupyter environment. Environment details are listed in our requirements.txt file.

1) First, we started with our extract, transform, and load tasks. Our core data is available at [realtor.com](https://www.realtor.com/research/data/). The version we are using is the monthly zip data found [here](https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_Zip_History.csv). 

2) The notebook ETL.ipynb is found within the data_eng folder (Team-21/Code/data_eng/ETL.ipynb). Please change the path in the second cell to where the realtor.com .csv is stored on your machine. The ETL.ipynb notebook will retrieve and merge the ancillary data via an API (The key API key is the code). Each notebook will build on the data created in the ETL process, using the SQL Lite table view that will be used for the modeling. We used the latter to simulate a real-world operation and to make join computations easier. One note for the random forest model is that we commented out the optimization section to keep runtime and memory usage to a minimum. It runs with the optimized parameters without that code block. 

3) Next, our actual modeling approaches are contained within the models folder (Team-21/Code/models). Our most successful approach was an optimized random forest model. It yields the lowest MSE, our loss function. To run all the models in one notebook please run the Code/models/all_models_compare.ipynb notebook. 
We used both an artificial neural network and a few iterations of multiple linear regression models. Much like the random forst model our loss function is the MSE to make model comparisons easier. 


## Credits

Big shoutout to @chau2450 (Nildip Chaudhuri) as he took on the bulk of the initial modeling work, as well as the final version of our ETL framework. 

@eeuler3 (Erik Euler) handled the initial ETL approach, stitching together our data sources together for our progress report and initial exploratory modeling, as well as visualizations and consolidation and cleaning of the modeling approach into the final notebook. 

@gmarrero30 (Gio Marrero) did the exploratory modeling for the progress report, data manipulation, and detailed the modeling approaches for the final paper. 

@mpaknejad3 (Mary Paknejad) handled the consolidation of the progress report and final paper, as well as some of the visualizations. 

@nsienicki3 (Nick Sienicki) handled the documentation of the approach and motivations for the progress report, as well as the results discussion and conclusion for the final paper. 

Throughout, each of the group members plugged in where neccesary, forming a great partnership.   
