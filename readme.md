# Scrape.py Usage

## Inputs

| Short Switch | Full Switch | Required | Default Value | Description |
|--------------|-------------|:----------:|:---------------:|-------------|
| -u | --url | True | No Default | The url to scrape. No url validity checks are performed. Valid URL is assumed. |
| -d | --directory | False | output | The specified output directory. Defaults to 'output'. Will be created if non-existent. |
| -r | none | False | False | Determines whether scraper should recursively scrape links found in url. Without this switch present scrape will only scrape the top level of the given url |
| -v | none | False | False | Toggles Verbose logging. Without this switch present only the final dictionary of downloaded content will be printed

## Outputs
### Successful Cases
The script will attempt to find all html content, pngs, svgs, pdfs, javascript, css, and other assets and dump them, in the same directory structure as the initial url, into the specified output directory. Please see [Known Limitations](#known-limitations) for some clarifying details on what may not scrape correctly.

### Failure Cases
Any failures will be automatically output into a text file titled ```Scrape_Failures.txt``` in the calling directory. This can include failures such as:
1. URL Response Status Code was not 200
2. An exception occurred during either download/read/write stages

## Usage
This script can be used to either scrape a top level url and its content and assets or recursively scrape a domain for its content and assets. See [Usage Examples](#usage-examples) for specific commands to call.

## Known Limitations
This script is far from perfect as it was created in a hurry to assist in the Developer Portal migration. Currently you may see the following issues when scraping:

- This script was created with the express intention of scraping Developer.Vmware.com. As such it may not be able to scrape all domain names equally well. User should attempt to host their scraped content locally to ensure proper scraping of content.
- Base64 images are not downloaded. 
- Some extensions may not be downloaded directly, the script may attempt to create a directory with the extensions name and then download into that directory. For example,
you may see a directory hierarchy such as ```assets/images/example.png/example.png``` where the first example.png is a directory and the second is the actual png. 
- PDF's may download as blank pages depending on how it was encoded by the server. Please check the downloaded pdfs to ensure correctness. Enabling verbose logging will also print the url it was downloaded from to help manual downloading if the download was not correctly downloaded.

## Usage Examples
### Non-Recursive
```bash
python3 scrape.py -u https://example.com
```
The above example will scrape just the top-most html and assets of example.com and place it into the default 'output' folder.

```bash
python3 scrape.py -v -u https://example.com
```
Same as above example but will output all logs as well


```bash
python3 scrape.py -d customDirectory -u https://example.com
```
Same as first example but outputting to specified directory 'customDirectory'. The script will create this directory if it does not already exist

```bash
python3 scrape.py -v -d customDirectory -u https://example.com
```
Same as previous example but will output all logs as well.


-----
### Recursive 
```bash
python3 scrape.py -r -u https://example.com
```
The above example will scrape the domain 'example.com' recursively trying to find all links and assets and output the downloads to the default output directory 'output'

```bash
python3 scrape.py -v -r -u https://example.com
```
Same as previous example but will output all logs as well.

```bash
python3 scrape.py -r -d customDirectory -u https://example.com
```
Same as first example but outputting to specified directory 'customDirectory'. The script will create this directory if it does not already exist

```bash
python3 scrape.py -v -r -d customDirectory -u https://example.com
```
Same as previous example but will output all logs as well

## Important Note
The recursive feature of this script will ignore any paths that do not follow at least the base url given regardless of if the path exists in the 

For Example:

```bash
python3 scrape.py -v -r -u https://example.com/some/url/path
```
Will start the scraping specifically from ```/some/url/path```. It will not try to scrape the main page, ```example.com```, nor even the previous indexes on the path ```/some/``` or ```/url/```, even if they exist. However, it will continue to scrape further along the given path. IE, if there exists some ```some/url/path/that/continues``` it will attempt to scrape any indexes found on that path, and so on.