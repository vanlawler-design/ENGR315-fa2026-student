import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

from pathlib import Path

data_file = Path(__file__).resolve().parents[2] / 'data' / 'covid' / 'us-counties.csv'

if len(sys.argv) > 1:
    data_file = Path(sys.argv[1])

all_data = parse_nyt_data(str(data_file))

for county in ['Harrisonburg city', 'Rockingham']:
    county_data = []

    for record in all_data:
        if record[1] == county and record[2] == 'Virginia':
            county_data.append(record)

    # Dates use YYYY-MM-DD
    county_data.sort()

    dates = []
    new_cases = []
    first_case_date = ''
    previous_cases = 0

    for record in county_data:
        current_date = record[0]
        total_cases = record[4]

        # Save the first date with a positive cumulative case count.
        if first_case_date == '' and total_cases > 0:
            first_case_date = current_date

        # Subtract yesterday's cumulative total to find today's new cases.
        dates.append(current_date)
        new_cases.append(total_cases - previous_cases)
        previous_cases = total_cases

    print('\n' + county + ', Virginia')
    print('Question 1: First reported positive case:', first_case_date)

    # Find the largest daily increase
    most_new_cases = max(new_cases)
    print('Question 2: Greatest daily increase:', most_new_cases, 'cases')
    for i in range(len(new_cases)):
        if new_cases[i] == most_new_cases:
            print('  Date:', dates[i])



    # This CSV has consecutive daily records for both localities.
    seven_day_totals = []
    for i in range(len(new_cases) - 6):
        week_total = 0
        for j in range(i, i + 7):
            week_total = week_total + new_cases[j]
        seven_day_totals.append(week_total)

    # Find the largest seven-day total
    most_weekly_cases = max(seven_day_totals)
    print('Question 3: Worst seven-day total:', most_weekly_cases, 'cases')
    for i in range(len(seven_day_totals)):
        if seven_day_totals[i] == most_weekly_cases:
            print('  Period:', dates[i], 'through', dates[i + 6], '(inclusive)')

# Negative daily changes are retained because they are data corrections.