import typer
import scraper
import helpers
import sys

app = typer.Typer()

@app.command()
def years():
    year = scraper.get_years()
    for y in year:
        typer.echo(y)


@app.command()
def races(year: str):
    races = scraper.get_races(year)
    for r in races:
        typer.echo(r)


@app.command()
def result(year: str, race_stub: str, session: str = "race"):
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

    helpers.json_string(results)


@app.command()
def season_result(year: str, result_type: str = "drivers"):
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
    helpers.json_string(results)


@app.command()
def weekend_sessions(year: str, race_stub: str):
    sessions = scraper.get_weekend_sessions(year, race_stub)
    for session in sessions:
        typer.echo(session)


if __name__ == "__main__":
    app()
