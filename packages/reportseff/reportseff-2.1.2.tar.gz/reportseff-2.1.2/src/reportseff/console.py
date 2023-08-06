"""CLI for reportseff."""
from shutil import which
import sys
from typing import Dict, List, Tuple

import click

from . import __version__
from .db_inquirer import BaseInquirer, SacctInquirer
from .job_collection import JobCollection
from .output_renderer import OutputRenderer


@click.command()
@click.option(
    "--modified-sort",
    default=False,
    is_flag=True,
    help="If set, will sort outputs by modified time of files",
)
@click.option(
    "--color/--no-color",
    default=True,
    help="Force color output. No color will use click defaults",
)
@click.option(
    "--format",
    "format_str",
    default="JobID%>,State,Elapsed%>,TimeEff,CPUEff,MemEff",
    help="Comma-separated list of columns to include. Options "
    "are any valid sacct input along with CPUEff, MemEff, and "
    "TimeEff.  In systems with jobstat caching, GPU usage can be "
    "added with GPUEff, GPUMem or GPU (for both). "
    "A width and alignment may optionally be provided "
    'after "%", e.g. JobID%>15 aligns job id right with max '
    "width of 15 characters. Generally NAME[[%:][ALIGNMENT][WIDTH[e$]?]]. "
    "When an `e` or `$` is present after a width argument, "
    "the output will be truncated to the right."
    "Prefix with a + to add to the defaults. "
    "A single format token will suppress the header line. "
    "Wrap in quotes to pass a string literal, "
    "otherwise alignment may be misinterpreted.",
)
@click.option(
    "--debug", default=False, is_flag=True, help="Print raw db query to stderr"
)
@click.option(
    "-u",
    "--user",
    default="",
    help="Ignore jobs, return all jobs in last week from user",
)
@click.option(
    "-s", "--state", default="", help="Only include jobs with the specified states"
)
@click.option(
    "-S", "--not-state", default="", help="Include jobs without the specified states"
)
@click.option(
    "--since",
    default="",
    help="Only include jobs before this time. Can be valid sacct "
    "or as a comma separated list of time deltas, e.g. d=2,h=1 "
    "means 2 days, 1 hour before current time. Weeks, days, "
    "hours, and minutes can use case-insensitive abbreviations. "
    "Minutes is the minimum resolution, while weeks is the coarsest.",
)
@click.option(
    "--node/--no-node",
    "-n/-N",
    default=False,
    help="Report node-level statistics. Adds `jobid` to format for proper display.",
)
@click.option(
    "--node-and-gpu/--no-node-gpu",
    "-g/-G",
    default=False,
    help=(
        "Report each GPU for each node. "
        "Sets `node` and adds `GPU` to format automatically."
    ),
)
@click.version_option(version=__version__)
@click.argument("jobs", nargs=-1)
def main(
    modified_sort: bool,
    color: bool,
    format_str: str,
    debug: bool,
    user: str,
    state: str,
    not_state: str,
    since: str,
    jobs: tuple,
    node: bool,
    node_and_gpu: bool,
) -> None:
    """Main entry point for reportseff."""
    if format_str.startswith("+"):
        format_str = "JobID%>,State,Elapsed%>,TimeEff,CPUEff,MemEff," + format_str[1:]

    output, entries = get_jobs(
        jobs=jobs,
        format_str=format_str,
        user=user,
        modified_sort=modified_sort,
        state=state,
        not_state=not_state,
        since=since,
        debug=debug,
        node=node,
        node_and_gpu=node_and_gpu,
    )

    if entries > 20:
        click.echo_via_pager(output, color=color)
    else:
        click.echo(output, color=color)


def get_jobs(
    jobs: tuple,
    format_str: str = "",
    user: str = "",
    debug: bool = False,
    modified_sort: bool = False,
    state: str = "",
    not_state: str = "",
    since: str = "",
    node: bool = False,
    node_and_gpu: bool = False,
) -> Tuple[str, int]:
    """Helper method to get jobs from db_inquirer.

    Returns:
        The string to display, tabulated and colored
        The number of jobs found to use paging properly

    Raises:
        Exception: if there is an error processing entries
    """
    job_collection = JobCollection()

    inquirer, renderer = get_implementation(format_str, node, node_and_gpu)

    inquirer.set_state(state)
    inquirer.set_not_state(not_state)

    inquirer.set_since(since)

    add_jobs = False

    try:
        if user:
            inquirer.set_user(user)
            add_jobs = True
        elif inquirer.has_since() and not jobs:  # since is set
            inquirer.all_users()
            add_jobs = True
        else:
            job_collection.set_jobs(jobs)

    except ValueError as error:
        click.secho(str(error), fg="red", err=True)
        sys.exit(1)

    db_output = get_db_output(inquirer, renderer, job_collection, debug)
    for entry in db_output:
        try:
            job_collection.process_entry(entry, add_job=add_jobs)
        except Exception as error:
            click.echo(f"Error processing entry: {entry}", err=True)
            raise error

    found_jobs = job_collection.get_sorted_jobs(modified_sort)
    found_jobs = [j for j in found_jobs if j.state]

    return renderer.format_jobs(found_jobs), len(found_jobs)


def get_implementation(
    format_str: str,
    node: bool = False,
    node_and_gpu: bool = False,
) -> Tuple[BaseInquirer, OutputRenderer]:
    """Get system-specific objects.

    Args:
        format_str: the formatting options specified by user

    Returns:
        A db_inqurirer
        An output renderer
    """
    if which("sacct") is not None:
        inquirer = SacctInquirer()
        renderer = OutputRenderer(
            inquirer.get_valid_formats(),
            format_str,
            node=node or node_and_gpu,
            gpu=node_and_gpu,
        )
    else:
        click.secho("No supported scheduling systems found!", fg="red", err=True)
        sys.exit(1)

    return inquirer, renderer


def get_db_output(
    inquirer: BaseInquirer,
    renderer: OutputRenderer,
    job_collection: JobCollection,
    debug: bool,
) -> List[Dict[str, str]]:
    """Get output from inquirer.

    Returns:
        The db inquirer entries for the provided objects
    """

    def print_debug(info: str) -> None:
        click.echo(info, err=True)

    debug_cmd = None
    if debug:
        debug_cmd = print_debug

    try:
        result = inquirer.get_db_output(
            renderer.query_columns, job_collection.get_jobs(), debug_cmd
        )
    except RuntimeError as error:
        click.secho(str(error), fg="red", err=True)
        sys.exit(1)

    return result
