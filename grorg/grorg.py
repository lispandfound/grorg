from PyOrgMode import PyOrgMode
import click
from grorg import selector, property_filter


PROPERTY_DRAWER_RX = r'property\[(?P<property_name>\w+)\]'


def property_drawer_filter(rx_match, header):
    ''' Match find a specific property from the PROPERTIES drawer in an org
    mode header. '''
    property_name = rx_match.group('property_name').upper()
    property_drawer = selector.drawer_from(header)

    if not property_drawer:
        return None

    for drawer_property in property_drawer.content:
        if drawer_property.name == property_name:
            value = drawer_property.value
            return property_filter.parse_value(value)

    return None


class FilterSetParamType(click.ParamType):
    """ A click parameter type that constructs property filters. """
    name = 'filter'

    def convert(self, value, param, ctx):
        """ Build a filter object from value (a string
        containing key value pairs separated with commas). """

        prop_filter = property_filter.PropertyFilter()
        prop_filter.add_hook(PROPERTY_DRAWER_RX, property_drawer_filter)
        kv_pairs = value.split(',')
        for pair in kv_pairs:
            try:
                filter_prop, relationship = property_filter.relationship_from(pair)
                prop_filter.add_filter(filter_prop, relationship)
            except property_filter.RelationshipParseError:
                self.fail('{} is not a valid key value pair'.format(pair))

        return prop_filter


@click.argument('org_file', type=click.File('r'))
@click.argument('org_selector')
@click.option('--filter', type=FilterSetParamType(), help='Filters to apply to selected nodes.')
@click.option('--content', is_flag=True)
@click.option('--todo-keywords', help='Add extra keywords that are recognized as todo items.')
@click.option('--done-keywords', help='Add extra keywords that are recognized as done items.')
@click.command()
def cli(org_file, org_selector='', filter=None, content=None,
        todo_keywords=None, done_keywords=None):
    """ grorg, grep for org-mode.\n
    Search all headings selected by ORG_SELECTOR in the file
    ORG_FILE. Use the --filter option to filter by specific properties
    or pipe to grep. """

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
        if not content:
            node.content = []
        click.echo(node.output().strip())


cli()
