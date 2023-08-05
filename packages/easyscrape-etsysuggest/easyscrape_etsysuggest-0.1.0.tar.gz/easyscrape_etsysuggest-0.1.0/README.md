# easyscrape-etsysuggest
Scrape Etsy search suggestions with Python

<img src="https://github.com/amazingjoe/amazingjoe.github.io/blob/main/imgs/Easyscrape.png" width="50%"/>

## Instructions

1. Install:

```
pip install easyscrape-etsysuggest
```

2. Get Etsy Suggestions for a Search Term:

```python
from easyscrape_etsysuggest import querysuggestions as ES

# Request suggestions for a search term
ESResults = ES.query("Mony Python")
ESResults

['monty python', 'monty python doormat', 'monty python sticker', 'monty python shirt', 'monty python holy grail', 'monty python t-shirt', 'monty python clock', 'monty python car decal', 'monty python costume', 'monty python rugs', 'monty python pin']
```

3. ES query returns a list of strings with the results.