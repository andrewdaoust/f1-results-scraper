import sys
import typer

import scraper
import helpers


app = typer.Typer()


@app.command()
def years(output_file: str | None = None):
    year = scraper.get_years()
    helpers.json_output(year, output_file)


@app.command()
def races(year: str, output_file: str | None = None):
    races = scraper.get_races(year)
    helpers.json_output(races, output_file)


@app.command()
def result(year: str, race_stub: str, session: str = "race", output_file: str | None = None):
    match session:
        # Race
        case "race":
            results = scraper.get_result(year, race_stub, "race-result")
        case "fastest-laps":
            results = scraper.get_result(year, race_stub, "fastest-laps")
        case "pit-stops":
            results = scraper.get_result(year, race_stub, "pit-stop-summary")
        # Quali
        case "qualifying" | "quali":
            results = scraper.get_result(year, race_stub, "qualifying")
        # Practice
        case "fp1":
            results = scraper.get_result(year, race_stub, "practice/1")
        case "fp2":
            results = scraper.get_result(year, race_stub, "practice/2")
        case "fp3":
            results = scraper.get_result(year, race_stub, "practice/3")
        # Sprint
        case "sprint-qualifying" | "sprint-quali":
            results = scraper.get_result(year, race_stub, "sprint-qualifying")
        case "sprint":
            results = scraper.get_result(year, race_stub, "sprint-results")
        # Grids
        case "grid":
            results = scraper.get_result(year, race_stub, "starting-grid")
        case "sprint-grid":
            results = scraper.get_result(year, race_stub, "sprint-grid")
        case _:
            typer.echo("Invalid session name")
            sys.exit(1)

    helpers.json_output(results, output_file)


@app.command()
def season_result(year: str, result_type: str = "drivers", output_file: str | None = None):
    match result_type:
        case "drivers":
            results = scraper.get_season_result(year, "drivers")
        case "races":
            results = scraper.get_season_result(year, "races")
        case "constructors":
            results = scraper.get_season_result(year, "team")
        case "fastest-laps":
            results = scraper.get_season_result(year, "fastest-laps")
        case _:
            typer.echo("Invalid result type. Try 'drivers', 'constructors', 'races', or 'fastest-laps'.")
            sys.exit(1)
    helpers.json_output(results, output_file)


@app.command()
def weekend_sessions(year: str, race_stub: str, output_file: str | None = None):
    sessions = scraper.get_weekend_sessions(year, race_stub)
    helpers.json_output(sessions, output_file)


if __name__ == "__main__":
    app()
