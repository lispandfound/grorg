import re
from PyOrgMode import PyOrgMode
import click
from grorg import selector, property_filter

KEY_VALUE_RE = re.compile('^(?P<property>\w+)(?P<invert>!)?(?P<relationship>=|>|<|{)(?P<value>.*)?$')


class FilterSetParamType(click.ParamType):
    name = 'filter'

    def convert(self, value, param, ctx):
        """ Build a filter object from value (a string
        containing key value pairs separated with commas). """

        prop_filter = property_filter.PropertyFilter()
        kv_pairs = value.split(',')
        for pair in kv_pairs:
            relationship_matches = re.match(KEY_VALUE_RE, pair)
            if not relationship_matches:
                self.fail('{} is not a valid key value pair'.format(pair))
            else:
                filter_prop = relationship_matches.group('property')
                value = relationship_matches.group('value')
                relationship_op = relationship_matches.group('relationship')
                invert = relationship_matches.group('invert') or ''
                relationship_string = invert + relationship_op + value
                relationship = property_filter.relationship_from(relationship_string)
                prop_filter.add_filter(filter_prop, relationship)
        return prop_filter


@click.argument('org_file', type=click.File('r'))
@click.argument('org_selector')
@click.option('--filter', type=FilterSetParamType())
@click.option('--content', type=bool)
@click.option('--todo-keywords')
@click.option('--done-keywords')
@click.command()
def cli(org_file, org_selector='', filter=None, content=None,
        todo_keywords=None, done_keywords=None):
    """ Test documentation """

    org_document = PyOrgMode.OrgDataStructure()

    if todo_keywords:
        todo_keywords = todo_keywords.split(',')
        for keyword in todo_keywords:
            org_document.add_todo_state(keyword)
    elif done_keywords:
        done_keywords = done_keywords.split(',')
        for keyword in done_keywords:
            org_document.add_done_state(keyword)

    document = org_file.read()
    org_document.load_from_string(document)
    nodes = selector.apply_selector(org_selector, org_document)
    result = selector.expand(nodes, recursive=True)
    if filter is not None:
        result = (node for node in result if filter.apply_filter(node))

    for node in result:
        if content is None:
            node.content = []
        click.echo(node.output().strip())


cli()
