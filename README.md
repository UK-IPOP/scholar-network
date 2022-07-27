# Welcome to Scholar Network

This package is intended for people wanting to scrape Google Scholar
to build graph networks of Google Scholar authors and identify network
connections as opportunities for collaboration.

## Documentation

API Reference Documentation available [here](https://uk-ipop.github.io/scholar-network/)

## Features

1. Selenium based web scraping
2. Poetry based dependency management
3. Basic Graph algorithms and metrics

## Requirements

- A Selenium web driver [link](https://selenium-python.readthedocs.io/installation.html#drivers)
  - Chrome 
    - `brew install --cask chromedriver`
  - Firefox
    - `brew install geckodriver`
  - Safari
    - Comes included in Safari 10+

## ToDo:

- Write tests

## Usage

To get started you can clone the repo and activate the poetry environment.

```
git clone https://github.com/UK-IPOP/scholar-network.git
cd scholar-network
poetry install --no-dev
poetry shell
```

Then start hacking! 😃

### Examples

_You must know each author's Google Scholar ID for this package to work._

Scraping one author (my wife, for example):

```python
>>>import scholar_network as sn
>>>sn.scrape_single_author(scholar_id='ZmwzVQUAAAAJ', scholar_name='Michelle Duong')
```

The data for the author will then be in your `data/scraped.json` file.

This defaults to the Safari web driver which we could have manually specified, or, alternatively, 
we could request to use the Chrome web driver.

```python
>>>import scholar_network as sn
>>>sn.scrape_single_author(scholar_id='ZmwzVQUAAAAJ', scholar_name='Michelle Duong', preferred_browser='chrome')
```

To create a graph from this new data is easy:
```python
>>>g = sn.build_graph()
```

Then, to see the most common five (5) connections:
```python
>>>g.edge_rank(limit=5)
Out[4]:
[(('David Burgess', 'Donna Burgess'), 64),
 (('Ashley Martinez', 'Daniela Moga'), 64),
 (('Daniela Moga', 'Erin Abner'), 62),
 (('Donna Burgess', 'Katie Wallace'), 62),
 (('Chang-Guo Zhan', 'Fang Zheng'), 60)]
```
