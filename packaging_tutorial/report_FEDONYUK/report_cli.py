import click
import report


@click.command()
@click.option('--file', type=click.Path(exists=True), required=True, help='Specify the path to the source files.')
@click.option('--asc', is_flag=True, help='Get the F1 Monaco report in ascending lap time.')
@click.option('--desc', is_flag=True, help='Get the F1 Monaco report by descending lap times.')
@click.option('--driver', help='Get the F1 Monaco report for a specific rider')
def main_cli(file: str, asc: bool, desc: bool, driver: str = None) -> None:
    """This application will create and report the results of the F1 Monaco 2018 race from the
    input race log files, the path to which you specify in the --file command. There are several
    options for getting the report."""
    if not file:
        raise click.UsageError("---Option --file is required!!!---")
    elif (asc and desc) or (asc and driver) or (driver and desc):
        raise click.UsageError("--Options --asc,--desc,--driver cannot be used together!--")
    elif driver:
        if driver in (dr.name for dr in report.get_drivers(file)):
            driver_id = [dr.driver_id for dr in report.get_drivers(file) if dr.name==driver][0]
            report.print_report(True, driver_id, file)  # Call a function to get a separate report.
        else:
            raise click.UsageError("--Please enter a valid driver name!--")
    else:
        if not asc and not desc:
            asc = True  # Default to ascending order if neither --asc nor --desc is provided.
        report.print_report(asc, None, file)  # Call a function to get the overall report.


if __name__ == '__main__':
    main_cli()