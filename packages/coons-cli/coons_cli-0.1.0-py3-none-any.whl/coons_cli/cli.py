import click
import requests
import os
import re

@click.group()
def cli():
    pass

@cli.command()
@click.option('-q', '--query', type=str, default="*")
@click.argument('size', type=int)
def get(size, query):
    """Get a flat list of object from a coons instance."""
    token = os.environ.get('COONS_TOKEN')
    url = f'https://coons.rero.ch/api/objects?access_token={token}&size={size}&facets=&q={query}'
    res = requests.get(url)
    data = res.json()
    for hit in data.get('hits', {}).get('hits'):
        name = hit['metadata'].get('name')
        type = hit['metadata'].get('type')
        click.echo(f'{name}:{type}')
        for link in  hit['metadata'].get('objects', []):
            click.echo(f'  {link.get("predicate")} -> {link.get("name")}:{link.get("type")}')

def create(data, url):
    ids = []
    for key, links in data.items():
        predicate, name, type = None, None, None
        if res := re.match(r'^\s*(.*?)\s+->\s+(.*?):(.*?)\s*$', key):
            (predicate, name, type) = res.groups()
        elif res := re.match(r'^\s*(.*?):(.*?)\s*$', key):
            (name, type) = res.groups()
        metadata = dict(name=name, type=type)
        if links:
            metadata['objects'] = links
        res = requests.post(url, json=dict(metadata=metadata))
        _id = res.json().get('id')
        click.secho(f'{name}:{type} ({_id}) created', fg='green')
        ids.append({
            'predicate': predicate,
            '$ref': f'https://coons.rero.ch/api/objects/{_id}'
        })
     
    return ids

def parse(lines, url, level=0):
    data = {}
    while lines:
        line = lines.pop(0)
        nspaces = len(re.match(r'^(\s*)\w+.*?', line)[1])
        line = line.strip()
        if lines:
            next_nspaces = len(re.match(r'^(\s*)\w+.*?', lines[0])[1])
            links = []
            if next_nspaces > nspaces:
                links = parse(lines, level=next_nspaces, url=url)
            data[line] = links
            if next_nspaces < nspaces:
                return create(data, url=url)
        else:
            data[line] = []
            return create(data, url)
    return create(data, url)

	
@cli.command()
@click.argument('input', type=click.File('r'))
def add(input):
    """Create object form a text file."""
    token = os.environ.get('COONS_TOKEN')
    url = f'https://coons.rero.ch/api/objects?access_token={token}'
    parse(input.readlines(), url=url)


@cli.command()
@click.argument('query')
def delete(query):
    """Delete object from a query, confirmation is required."""
    token = os.environ.get('COONS_TOKEN')
    base_url = 'https://coons.rero.ch/api/objects'
    url = f'{base_url}?access_token={token}&size=500&facets=&query={query}'
    res = requests.get(url)
    ids = [r['id'] for r in res.json().get('hits', {}).get('hits', [])]
    if click.confirm(f'Do you want to delete {len(ids)} objects?'):
        with click.progressbar(ids) as bar:
            for _id in bar:
                url = f'{base_url}/{_id}?access_token={token}'
                res = requests.delete(url)
                if res.status_code != 204:
                    click.secho(res.text ,fg='red')

if __name__ == '__main__':
    cli()
