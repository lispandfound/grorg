from org import parser
import click

@click.command()
@click.argument('org_file', type=click.File('r'))
@click.argument('selector')
def cli(org_file, selector):
    """ Test documentation """
    document = org_file.read()
    org_document = parser.parse(document)
    print(org_document)
