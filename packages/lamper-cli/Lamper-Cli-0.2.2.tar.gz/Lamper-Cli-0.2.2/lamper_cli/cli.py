import click
from .lamper import main


@click.command()
def cli():
	main()
