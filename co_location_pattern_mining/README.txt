*****************************************************************************************************
*                                       TOPICS IN AI                                                *
*****************************************************************************************************
*                                      SOUMYA SARKAR                                                *
*                                       2022CSM1013                                                 *
*****************************************************************************************************
*                                  README FOR ASSIGNMENT 1                                          *
*****************************************************************************************************

DATABASE CONFIGURATION:
Database details have been placed in database.ini file.

SMALL DATASET:
1) To setup the database for small dataset, run small_data_create.py . Dataset has been provided for
this (small_data_points.csv)
Please Note: Do change e_type_name as well as add extra if conditions for method read_file() [L44 - ]
2) Once setup, run the algorithm_small.py file. Set threshold, h-value and pattern as per your liking. 
Please note, tables must be created already as per pattern.
Ex: If "ABCD" is our pattern, there should be data available for A, B, C and D.
3) Output can be viewed in output_small.txt in same folder.

LARGE DATASET:
1) To setup the database for small dataset, run large_data_create.py
Please Note: Do change e_type_name as well as add extra if conditions for method read_file() [L69 - ]
2) Once setup, run the algorithm_large.py file. Set threshold, h-value and pattern as per your liking. 
Please note, tables must be created already as per pattern.
Ex: If "ABCD" is our pattern, there should be data available for A, B, C and D.
3) Output can be viewed in output_large.txt in same folder.

NOTE: Do not forget to change the path for base_location in connection.py to current folder.


OBSERVATION:
A dry run was made with threshold  = 0.3 and distance = 120km for the large dataset. This would have
generated all possible combinations - so 20^5 combinations.
Without indexing (algorithm_large_without_index.py => output_large_without_indexing.txt) we get a 
runtime of approximately 10.5 minutes.
With R-tree indexing (algorithm_large.py => output_large_with_indexing.txt) we get a runtime of app-
roximately 8.5 minutes.
Dataset has been provided as large_data_points.csv, along with the output files and 
algorithm_large_without_index in folder test_result.

*****************************************************************************************************
*                                            THANK YOU!                                             *
*****************************************************************************************************