import click
import loci_spotbugs.utils as lcu


def get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


@click.command()
@click.option("-i", "--input-file",
              prompt="SpotBugs XML file",
              help="The SpotBugs XML file with the output of a scan",
              required=True,
              type=str)
def summary(input_file):
    """Summarize a SpotBugs XML file"""
    bug_list = lcu.open_results_file_and_get_results(input_file)

    lcu.print_info(f"Summary for Results of [bold]{input_file}[/bold]:")
    total_results = len(bug_list)
    lcu.print_info(f"  Total issues: {total_results}")
    lcu.print_info("-----------------------------------------------")

    results_by_sev_dict = {}
    for i in range(0, 20):
        results_by_sev_dict[str(i)] = []

    for bug in bug_list:
        results_by_sev_dict[str(bug.severity_rank)].append(bug)

    for i in range(20):
        result_list = results_by_sev_dict[str(i)]
        if len(result_list) == 0:
            continue
        lcu.print_info(f"  Rank {i} severity issues: {len(result_list)}")

        result_count = {}
        for result in result_list:
            try:
                result_count[result.bug_type]
            except KeyError:
                result_count[result.bug_type] = 0
            result_count[result.bug_type] += 1

        for w in sorted(result_count, key=result_count.get, reverse=True):
            lcu.print_info(f"    x[bold]{result_count[w]}[/bold] {w}")

        lcu.print_info("----------------------------------------------")

    lcu.print_success("Results summarized. See https://spotbugs.readthedocs.io/en/stable/filter.html#rank for rank"
                      " explanations.")
