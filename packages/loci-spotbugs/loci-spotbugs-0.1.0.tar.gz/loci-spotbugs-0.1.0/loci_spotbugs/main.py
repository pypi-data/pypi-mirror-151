import click

import loci_spotbugs.utils as lcu
from loci_spotbugs.run import run
from loci_spotbugs.summary import summary


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    lcu.print_version()
    ctx.exit()


@click.group()
@click.option("-v", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def loci_spotbugs():
    pass


loci_spotbugs.add_command(run)
loci_spotbugs.add_command(summary)


if __name__ == "__main__":
    loci_spotbugs()
