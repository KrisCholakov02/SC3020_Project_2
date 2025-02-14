# SC3020 - SQL Query Evolution Analyzer

**SQL Query Evolution Analyzer** is a user-friendly tool designed to help users—even those without a technical background—understand and optimize their SQL queries. By comparing an original query with a modified version, the application visually displays changes in the Query Execution Plan (QEP) and provides a plain English explanation of the differences, empowering users to make informed performance improvements.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Employed](#technologies-employed)
- [Key Algorithms](#key-algorithms)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [GitHub Repository](#github-repository)

## Overview
SQL Query Evolution Analyzer simplifies the process of query optimization. The application:
- Generates QEPs for both the original and modified SQL queries.
- Computes and highlights differences between the two execution plans.
- Provides a natural language explanation of how the queries have evolved.
- Visualizes the changes to help users understand the impact on performance.

## Features
- **Dual Query Analysis**: Compare an old SQL query with a new one to see what has changed.
- **Visual QEP Display**: Intuitive, graphical visualization of query execution plans.
- **Auto-generated Explanations**: Clear, plain English descriptions of the differences between the queries.
- **Cost Analysis**: Detailed breakdown of cost metrics (e.g., startup and total costs) to help gauge query efficiency.
- **User-Friendly Interface**: Modern dark-themed GUI built with Python’s Tkinter libraries.
- **History Management**: Save and recall previous database connections and query comparisons for convenience.

## Installation
1. **Download the Project**: Clone or download the project folder with all its contents.
2. **Ensure Python 11.3 is Installed**: Verify that your machine has Python 11.3.
3. **Install Dependencies**: Open your terminal or command prompt, navigate to the project folder, and run:
   ```
   pip install -r requirements.txt
   ```
4. **Enable Dark Mode (Optional)**: For an enhanced visual experience, enable dark mode on your system.
5. **Run the Application**: Launch the program by executing:
   ```
   python3 project.py
   ```

## Usage
1. **Connect to the Database**: Enter your PostgreSQL connection details. The application supports saving multiple connection histories.
2. **Input Queries**: On the query comparison screen, enter both the original and the new SQL queries.
3. **View Analysis**: The tool generates and displays the QEP for each query, highlighting the differences visually and textually.
4. **Interpret Results**: Use the detailed cost metrics and auto-generated explanations to understand and optimize your queries.

## Technologies Employed
- **Python**: Core programming language.
- **Tkinter & CustomTkinter**: For building a responsive and modern GUI.
- **psycopg2-binary**: PostgreSQL adapter for establishing database connections.
- **Graphviz**: Used for generating and displaying visual QEP trees.
- **sqlparse & sqlvalidator**: Libraries for parsing, formatting, and validating SQL queries.
- **Darkdetect**: Automatically adjusts the UI based on the system’s theme settings.
- **Pmw & PySimpleGGUI**: Additional libraries to enhance the user interface.

## Key Algorithms
- **Database Connection Management**: Securely establishes a single instance of a PostgreSQL connection using psycopg2.
- **QEP Generation**: Executes SQL `EXPLAIN` queries (in JSON format) to retrieve detailed query execution plans.
- **QEP Comparison**: Uses depth-first traversal to compare two QEPs and detect differences in attributes like join types, cost metrics, and more.
- **English Explanation Generator**: Leverages text comparison techniques to produce an easy-to-understand explanation of the query differences.
- **Tree Visualization**: Recursively builds a visual representation of the QEP for clear, step-by-step comparison.
