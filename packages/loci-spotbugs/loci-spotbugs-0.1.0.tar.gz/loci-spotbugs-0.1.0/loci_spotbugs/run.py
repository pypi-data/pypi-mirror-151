import click
import os
from rich.progress import Progress
import loci_spotbugs.utils as lcu


@click.command()
@click.option("-i", "--input-file",
              prompt="SpotBugs XML file",
              help="The SpotBugs XML file with the output of a scan",
              required=True,
              type=str)
@click.option("-r", "--rank",
              help="Max severity rank (lower is more severe, see "
                   "https://spotbugs.readthedocs.io/en/stable/filter.html#rank)",
              required=True,
              type=int,
              default=12)
def run(input_file, rank):
    """Process a SpotBugs XML file and add results to Loci Notes"""

    lcu.print_info("Getting directory project information...")
    project_id, project_name = lcu.get_project_id_from_config_in_dir(os.getcwd())
    if project_id is None or project_name is None:
        lcu.print_error("Unable to determine associated project. To correct this, run this under a directory "
                        "associated with a Loci Notes project.")
        quit(-1)
    lcu.print_success(f"Using [bold]{project_name}[/bold].")

    # Here we need to get a full listing of filenames because the results of SpotBugs only includes the Java
    # source path, which is not enough to resolve this to a full artifact.
    bug_list = lcu.open_results_file_and_get_results(input_file)
    basepath = lcu.open_results_file_and_get_basepath(input_file)

    fq_files_list = []

    for subdir, dirs, files in os.walk(basepath):
        for file in files:
            fq_files_list.append(subdir + os.sep + file)

    if len(fq_files_list) == 0:
        lcu.print_error(f"Failed to find the directory '{basepath}'. Please make sure you run this from the same "
                        "machine where SpotBugs was originally run.")
        quit(-1)

    # First count up total number of results to get a semi-accurate count of the results for the progress bar
    valid_bugs_found = 0
    for bug in bug_list:
        if bug.severity_rank <= rank:
            valid_bugs_found += 1

    with Progress() as progress_bar:
        # The times 3 is because there are 3 requests per finding.
        task = progress_bar.add_task("Importing results...", total=valid_bugs_found * 3)

        for bug in bug_list:
            if bug.severity_rank > rank:
                # This filters out incorrect results that don't match the query
                continue

            # In the future, we can probably ask the user if they want to add a note for EVERY
            # node along the path, but for now we just add the top and bottom path nodes, and
            # everything in between is implicit.

            if (bug.sink_line == ""):
                # Sink line is empty, something weird happened.
                lcu.print_warning(f"A bug in {bug.sink_filename} had an empty sink line. This is unexpected.")
                progress_bar.update(task, advance=3)
                continue

            # We need to resolve the src and sink of each result against our fully-qualified files list.
            sink_artifact = ""
            sink_artifact_set = False
            for fq_file in fq_files_list:
                if fq_file.endswith(bug.sink_filename):
                    sink_artifact = lcu.calculate_artifact_from_fq_filename(fq_file) + ":" + bug.sink_line
                    sink_artifact_set = True
                    break
            if not sink_artifact_set:
                lcu.print_warning(f"Could not normalize the source filename {bug.sink_filename} as a sink. "
                                  "If this falls under the application repo, make sure this is run on the same"
                                  " machine where SpotBugs was originally run. Skipping import of this bug.")
                progress_bar.update(task, advance=3)
                continue

            src_artifact = ""
            src_artifact_set = False
            for fq_file in fq_files_list:
                if fq_file.endswith(bug.src_filename):
                    src_artifact = lcu.calculate_artifact_from_fq_filename(fq_file) + ":" + bug.src_line
                    src_artifact_set = True
                    break
            if not src_artifact_set:
                lcu.print_warning(f"Could not normalize the source filename {bug.sink_filename} as an input source. "
                                  "If this falls under the application repo, make sure this is run on the same"
                                  " machine where SpotBugs was originally run. Skipping import this bug.")
                progress_bar.update(task, advance=3)
                continue

            # Send the info to the LN server for the sink node
            new_note = {}
            new_note["artifact_descriptor"] = sink_artifact
            new_note["submission_tool"] = "SpotBugs"
            new_note["note_type"] = "LOG"
            new_note["contents"] = "**Security Issue Sink Found**\n\n"
            new_note["contents"] += "**Bug Type** - " \
                f"[{bug.bug_type}](https://find-sec-bugs.github.io/bugs.htm#{bug.bug_type})\n"
            new_note["contents"] += "**Bug Severity** - " \
                f"[{bug.severity_rank}](https://spotbugs.readthedocs.io/en/stable/filter.html#rank)"

            # Detection and prevention of duplicate notes is handled by the server.
            lcu.loci_api_req(f"/api/projects/{project_id}/notes", method="POST",
                             data=new_note, show_loading=False)

            progress_bar.update(task, advance=1)

            if ((src_artifact == sink_artifact and bug.src_line == bug.sink_line) or bug.src_line == ""):
                # Sink and source are the exact same, we don't need the source or the link notes.
                progress_bar.update(task, advance=2)
                continue

            # Send the info to the LN server for the bottom (sink) node
            new_note = {}
            new_note["artifact_descriptor"] = src_artifact
            new_note["submission_tool"] = "SpotBugs"
            new_note["note_type"] = "LOG"
            new_note["contents"] = "**Source for Security Issue**\n\n"
            new_note["contents"] += "**Bug Type** - " \
                f"[{bug.bug_type}](https://find-sec-bugs.github.io/bugs.htm#{bug.bug_type})\n"

            # Detection and prevention of duplicate notes is handled by the server.
            lcu.loci_api_req(f"/api/projects/{project_id}/notes", method="POST",
                             data=new_note, show_loading=False)

            progress_bar.update(task, advance=1)

            # Next, link the two artifacts. The server will automatically add a link in each
            # direction with a single call, so we only need to send one request.
            new_note = {}
            new_note["artifact_descriptor"] = src_artifact
            new_note["submission_tool"] = "SpotBugs"
            new_note["note_type"] = "LINK"
            new_note["contents"] = sink_artifact

            # Detection and prevention of duplicate notes is handled by the server.
            lcu.loci_api_req(f"/api/projects/{project_id}/notes", method="POST",
                             data=new_note, show_loading=False)

            progress_bar.update(task, advance=1)
