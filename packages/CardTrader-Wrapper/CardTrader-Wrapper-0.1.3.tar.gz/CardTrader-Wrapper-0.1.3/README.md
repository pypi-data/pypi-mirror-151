# CardTrader Wrapper

[![PyPI - Python](https://img.shields.io/pypi/pyversions/CardTrader-Wrapper.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/CardTrader-Wrapper/)
[![PyPI - Status](https://img.shields.io/pypi/status/CardTrader-Wrapper.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/CardTrader-Wrapper/)
[![PyPI - Version](https://img.shields.io/pypi/v/CardTrader-Wrapper.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/CardTrader-Wrapper/)
[![PyPI - License](https://img.shields.io/pypi/l/CardTrader-Wrapper.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Black](https://img.shields.io/badge/Black-Enabled-000000?style=flat-square)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/Flake8-Enabled-informational?style=flat-square)](https://github.com/PyCQA/flake8)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/CardTrader-Wrapper.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/CardTrader-Wrapper/graphs/contributors)

[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/CardTrader-Wrapper/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/CardTrader-Wrapper/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/CardTrader-Wrapper/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/CardTrader-Wrapper/actions/workflows/testing.yaml)

A [Python](https://www.python.org/) wrapper for the [CardTrader](https://cardtrader.com) API.

## Installation

### Poetry

```bash
$ poetry add CardTrader-Wrapper
```

### Local Setup

1. Fork this repo
2. Create the env variable `CARDTRADER_ACCESS_TOKEN` with your access token from [CardTrader](https://cardtrader.com).
3. Make sure you have [Python](https://python.org/) installed: `python --version`
4. Make sure you have [Poetry](https://python-poetry.org/) installed: `poetry --version`
5. Clone the repo: `git clone https://github.com/<Username>/CardTrader-Wrapper`
6. Install the project and its dependencies via poetry: `poetry install`

## Example Usage

```python
from cardtrader.service import CardTrader
from cardtrader.sqlite_cache import SQLiteCache

session = CardTrader(access_token="Access Token", cache=SQLiteCache())

# List Games
results = session.games()
for game in results:
    print(f"{game.id_} | {game.display_name}")

# List Magic: the Gathering Expansions
results = [x for x in session.expansions() if x.game_id == 1]
for expansion in results:
    print(f"{expansion.id_} | {expansion.code} - {expansion.name}")

# List Magic: the Gathering - Game Night Cards for sale
blueprints = session.blueprints(expansion_id=1)
for card_blueprint in blueprints:
    products = session.products_by_blueprint(blueprint_id=card_blueprint.id_)
    for product in products:
        print(f"{product.price.formatted} | {card_blueprint.name}")
```

## Socials

[![Social - Discord](https://img.shields.io/badge/Discord-The--DEV--Environment-7289DA?logo=Discord&style=flat-square)](https://discord.gg/nqGMeGg)
