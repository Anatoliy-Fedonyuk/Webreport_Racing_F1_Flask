"""This module create CLI for application"""
import click
from loguru import logger

from packaging_tutorial.report_FEDONYUK.report import get_drivers, print_report

logger.add('debug.log', colorize=True, format='{time} {level} {message}', level='DEBUG')


@click.command()
@click.option('--file', type=click.Path(exists=True), required=True, help='Specify the path to the source files.')
@click.option('--asc', is_flag=True, help='Get the F1 Monaco report in ascending lap time.')
@click.option('--desc', is_flag=True, help='Get the F1 Monaco report by descending lap times.')
@click.option('--driver', help='Get the F1 Monaco report for a specific rider')
def main_cli(file: str, asc: bool, desc: bool, driver: str = None) -> None:
    """Create and report the results of the F1 Monaco 2018 race from the input race log files.

        Args:
            file (str): The path to the source files.
            asc (bool): Get the F1 Monaco report in ascending lap time.
            desc (bool): Get the F1 Monaco report by descending lap times.
            driver (str): Get the F1 Monaco report for a specific rider.

        Raises:
            click.UsageError: Raised if the provided options are invalid.

        Note:
            This CLI application provides options to generate reports from F1 Monaco 2018 race log files.

        Example:
            To generate an overall report in ascending lap time:
            $ python report_cli.py --file path/to/files --asc

            To generate a report for a specific driver (e.g., Lewis Hamilton):
            $ python report_cli.py --file path/to/files --driver "Lewis Hamilton"
    """
    try:
        if not file:
            logger.error("[CLI] Option --file is required!")
            raise click.UsageError("---Option --file is required!!!---")
        elif (asc and desc) or (asc and driver) or (driver and desc):
            logger.error("[CLI] Options --asc,--desc,--driver cannot be used together!")
            raise click.UsageError("--Options --asc,--desc,--driver cannot be used together!--")
        elif driver:
            if driver in (dr.name for dr in get_drivers(file)):
                driver_id = [dr.driver_id for dr in get_drivers(file) if dr.name == driver][0]
                print_report(True, driver_id, file)  # Call a function to get a separate report.
            else:
                logger.error("[CLI] No such driver name!")
                raise click.UsageError("--Please enter a valid driver name!--")
        else:
            if not asc and not desc:
                asc = True  # Default to ascending order if neither --asc nor --desc is provided.
            print_report(asc, None, file)  # Call a function to get the overall report.
    except FileNotFoundError:
        logger.error("[CLI] the file at the specified path does not exist!")
        raise click.UsageError(f"File not found: {file}")


if __name__ == '__main__':
    main_cli()
