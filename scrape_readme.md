# Scrape.py Usage

## Inputs

| Short Switch | Full Switch | Required | Default Value | Description |
|--------------|-------------|----------|---------------|-------------|
| -u | --url | True | No Default | The url to scrape. No url validity checks are performed. Valid URL is assumed. |
| -d | --directory | False | output | The specified output directory. Defaults to 'output'. Will be created if non-existent. |
| -r | none | False | False | Determines whether scraper should recursively scrape links found in url. Without this switch present scrape will only scrape the top level of the given url |
| -v | none | False | False | Toggles Verbose logging. Without this switch present only the final dictionary of downloaded content will be printed
