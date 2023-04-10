# SC3020 - Project 2
This project aims to implement a program that enables users from a non-technological background to understand changes made across their SQL queries when working with database management systems. The project particularly dives deeper into the query optimization process, wherein users can see in real time how editing their SQL queries can alter the generated output. The program should be able to:
* Take in an old query and a new query
* Generate a Query Execution Plan (QEP) for each query
* Compute the difference across both QEPs
* Auto generate english explanations of how the queries have evolved
* Display the QEP to try to visualize how the new query differs from the old.

## Installation Guide
* Download the project folder with all of its content
* Make sure you have Python 11.3 installed on your machine
* Open the terminal/cmd and navigate to inside the project folder
* Install the requirements from requirements.txt using  'pip install -r requirements.txt'
* Enable "Dark" mode on your machine's appearance settings to get a better design
* Run the application using the command 'python3 project.py' in your terminal/cmd