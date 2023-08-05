# easyscrape-ebaysearch
Scrape Ebay search suggestions in Python

<img src="https://github.com/amazingjoe/amazingjoe.github.io/blob/main/imgs/Easyscrape.png" width="50%"/>

## Instructions

1. Install:

```
pip install easyscrape-ebaysuggest
```

2. Get Ebay Suggestions for a Search Term:

```python
from easyscrape_ebaysuggest import querysuggestions as ES

# Request suggestions for a search term
ESResults = ES.query("Mony Python")
ESResults

['monty python and the holy grail', 'monty python flying circus complete', 'monty python and the holy grail vhs', 'monty python', 'monty python and the holy grail blu ray', 'monty python and the holy grail action figures', 'monty python flying circus complete dvd', 'monty python funko pop', 'monty python and the holy grail dvd', 'monty python shirt']
```

3. ES query returns a list of strings with the results.
