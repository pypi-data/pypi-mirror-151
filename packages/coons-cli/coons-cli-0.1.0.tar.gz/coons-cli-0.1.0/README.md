# COONS-CLI
A command line tools to interact with a coons instance.

## Installation

### Using PIP

```bash
pip install coons-cli
```

## Configuration

You can set your generated personal token in a environment variable `COONS_TOKEN`.

## Commands

Once the `coons-cli` package is installed you can run `coons --help` command.

### Get

#### Usage

```bash
Usage: coons get [OPTIONS] SIZE

  Get a flat list of object from a coons instance.

Options:
  -q, --query TEXT
  --help            Show this message and exit.
```

### Add

#### Usage

```bash
Usage: coons add [OPTIONS] INPUT

  Create object form a text file.

Options:
  --help  Show this message and exit.
```

#### Input file

The input file is an ascii(text) file of the form:

```
Informatic:interest
    development -> Coons:project
        realisation -> coons:web service
            dependency -> invenio:software
            dependency -> flask:software
        realisation -> coons-ui:software
            dependency -> angular:software
        realisation -> coons-cli:software
            dependency -> poetry:software
    skills -> python:language
        example -> misc:snippet
        documentation -> python:web page
    skills -> typescript:language

```
Each line is an object of the form `name:type`. The `predicate -> name:type` represents a link.

A sample of file can be found [here](https://github.com/chezjohnny/coons-cli/blob/main/contrib/data.txt).

### Delete

#### Usage

```bash
Usage: coons delete [OPTIONS] QUERY

  Delete object from a query, confirmation is required.

Options:
  --help  Show this message and exit.
```
