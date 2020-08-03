# Covid Scraper

Web scraper for grabbing daily total cases for Southern CA counties, California, and US.

If you don't already have these packages. Run the following commands:

```
  pip install requests
  pip install beautifulsoup4
  pip install tabula-py
```

Run the script:

```
> python scrape-covid-data.py
```

It outputs the following total cases separated by semicolon:
San Marcos Zip, San Marcos, San Diego County, Orange County, LA County, California, US

E.g.

```
250;594;29577;37391;192177;511836;4644565
```

This can be pasted into a Google Sheets doc and split to multiple columns
