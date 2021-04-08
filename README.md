# Scripting Analysis
## Prompt D: Write a script that will programmatically check whether all the impression pixels are valid

### Running pixel_checker:
Python 3 is required to run this script. You can install using Homebrew or directly from python.org. See instructions
[here](https://docs.python-guide.org/starting/install3/osx/)

Install dependencies:
`$ pip install -r requirements.txt`

Run pixel_checker
`$ python main.py`

pixel_checker will prompt for an absolute file path to the csv for ingestion, make sure to enter using full file name,
 including `.csv`

Progress bar will run until the program is complete

Output will indicate which tactic ids have failed including url that failed along with count of Success and Failure 
for each url

### Unit Tests:
Run unit tests directly from terminal using
`pytest -q test.py`

