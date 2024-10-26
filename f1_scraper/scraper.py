import sys
import requests
from bs4 import BeautifulSoup

import helpers

BASE_URL = "https://www.formula1.com"

# =======================================================================================
#
#                              HTML Requests and base parsing
#
# =======================================================================================

def get_main_page(year = None, result_type = "races"):
    if year != None:
        url = f"{BASE_URL}/en/results/{year}/{result_type}"
    else:
        url = f"{BASE_URL}/en/results"
    # Start at the main results page. This is the entry point for all result info
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # Get the `main` tag from the HTML. This has all the content we care about
    main = soup.main
    return main


def get_result_page(year, race_stub, session_stub = "race-result"):
    url = f"{BASE_URL}/en/results/{year}/races/{race_stub}/{session_stub}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # Get the `main` tag from the HTML. This has all the content we care about
    main = soup.main
    return main

# =======================================================================================
#
#                                   `years` command
#
# =======================================================================================

def get_years():
    main = get_main_page()
    # Find each of the `details` tags. The first one in the list contains all the years
    details = main.find_all('details')
    # First details tag has all the year info 
    years_html = details[0]
    # We know the hrefs are always in the form `/en/results/{year}/races` so no need to
    # Extract them. We cna just use the year itself to build the URL when we need it
    return [year.string for year in years_html.find_all('a')]

# =======================================================================================
#
#                                   `races` command
#
# =======================================================================================

def get_races(year):
    main = get_main_page(year=year)
    # Find each of the `details` tags. This has the list of years (and links to results),
    # The types of results, and the list of races by default. We can use the links from 
    # the result types to scrape other information later
    details = main.find_all('details')
    # Last `details` element has all the links and locations of the races
    races_html = details[2]
    races = []
    for r in races_html.find_all('a'):
        # Grid of all race results for this year, we don't need to include this
        if r.string == "All":
            continue

        href = r.get('href')

        split = href.split('/')
        race_num = split[-3]
        location = split[-2]
        # Race results URLs are always in the form 
        # "en/results/{year}/races/{race_num}/{location}/race-result"
        # so just need to return those
        races.append(f"{race_num}/{location}")
    return races

# =======================================================================================
#
#                                   `results` command
#
# =======================================================================================

def parse_result_table(main):
    table = main.table
    # first get the headers
    raw_headers = table.thead.tr.find_all('th')
    headers = []
    for rh in raw_headers:
        h = rh.p.string.lower()

        # Give a friendlier name to some headers
        if h == "pos":
            h = "position"
        elif h == "no":
            h = "number"
        elif h == "time/retired":
            h = "time"
        elif h == "pts":
            h = "points"
        headers.append(helpers.to_camel_case(h, sep=" "))

    # then get the data
    results = []
    for row in table.tbody.find_all('tr'):
        row_result_data = {}
        row_data = row.find_all('td')
        for i, d in enumerate(row_data):
            # Driver has more data stored in spans,
            # check for this special case first
            driver_data = d.find_all('span')
            if len(driver_data) > 0:
                row_result_data[headers[i]] = {
                    "firstName": driver_data[0].string,
                    "lastName": driver_data[1].string, # TODO: Need to figure out how to decode Unicode
                    "abbr": driver_data[2].string
                }
            else:
                row_result_data[headers[i]] = d.p.string
        results.append(row_result_data)
    return results


def get_result(year, race_stub, session_stub):
    if session_stub == "season":
        main = get_main_page(year)
    else:
        main = get_result_page(year, race_stub, session_stub=session_stub)
    try:
        results = parse_result_table(main)
        return results
    except:
        print("Invalid session for this race. No results.")
        sys.exit(1)

# =======================================================================================
#
#                                 `season-results` command
#
# =======================================================================================

def get_season_result(year, result_type):
    main = get_main_page(year, result_type)
    try:
        results = parse_result_table(main)
        return results
    except:
        print("Invalid season. No results.")
        sys.exit(1)

# =======================================================================================
#
#                                `weekend-sessions` command
#
# =======================================================================================

def get_weekend_sessions(year, race_stub):
    main = get_result_page(year, race_stub)

    uls = main.find_all("ul")
    sessions = []
    for session in uls[3].find_all("li"):
        match session.string:
            case "Race":
                continue
            case "Race Result":
                sessions.append("race")
            case "Practice 1":
                sessions.append("fp1")
            case "Practice 2":
                sessions.append("fp2")
            case "Practice 3":
                sessions.append("fp3")
            case "Pit Stop Summary":
                sessions.append("pit-stops")
            case "Starting Grid":
                sessions.append("grid")
            case _:
                sessions.append(
                    session.string.lower().replace(" ", "-")
                )
    
    return sessions
