# The Guardian coverage of Britney Spears
Text analysis of how The Guardian’s coverage of Britney Spears changed over time.

## The Big Question
How did the Guardian's coverage of Britney Spears change over time?

## Data
Articles are collected from the Guardian Open Platform API (headlines, summary lines, dates and sections). Data was retrieved on 27 October 2026. The data belongs to The Guardian and is not included in this repository, so running the fetch script downloads your own copy.

## Status: IN PROGRESS

### DONE:
- Script that fetches and downloads all matching articles and saves them to a CSV file.

### TO DO:
- Explore data and determine how to clean and filter.
- Create visualisations to understand shape of data.
- Split data into meaningful time eras.
- Research for context to make conclusions.

## How to run:

1) Create and activate a virtual environment.
2) Install the packages in the requirements file.
3) Register for an API key at https://open-platform.theguardian.com/
4) Copy .env.example file to .env and insert your unique API key.
5) Run the fetch script

