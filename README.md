# pagefinder
page finder project
*********************************************************************************************************************
OVERVIEW

This project is built as part of a course on an online platform, Coursera. The course is Capstone:Retreiving, Processing and Visualising data with Python.
The project aims to help the people searching web archives and deliver them with the best websites they can look based on their search query. The project uses the number of times a version of a particular website has been captured at "https://archive.org/web/" in a year and gives the best 10 options to use. Feel free to have a look at "https://archive.org/web/" in order to get a much more better picture of what the program can achieve.
*************************************************************************************************************************
REQUIREMENTS
The project uses many libraries and they have been embedded right in the project folder only in order to make things fast and simple. However in order to run this project, you must have the following installed on your system:
1. Python 3.8.2 or higher
2. Chrome Browser (only till version 83 are supported uptil now - if you have a higher version then you must download the latest chromedriver and replace it with the chromedriver already present in the project folder)
3. A standard internet connection
Rest all the things are there in the folder itself.
*****************************************************************************************************************************
HOW TO RUN

There are two modes to run this project:-

1. ALL IN ONE Mode
All the different modules of the project are embedded within one single file "RunDirect.py" which asks the user about what he/she wants to search and shows the results in a form of bar chart.
Just go to your command prompt, and run the file as a python file. 

2. COMPLETE Mode
Here, the user will have to run diiferent modules themselves
(a) PagePuller.py - This program takes on the search keyword and stores the html received from the internet in a sqlite database.
(b) cleanup.py - This program takes on the html from the PagePuller program's database, parses it and then stores it in a nice format in a new sqlite database.
(c) csv_maker.py - This program takes the cleaned database and converts it into a csv file in order to be visualised.
(d) index.html - The user must open it a browser in order to get the final visualisation.
********************************************************************************************************************************* 
 FURTHER INFO:

Please drop a mail at "tushargarg875@gmail.com" for any kind of further assistance you want on this project!
*********************************************************************************************************************************
