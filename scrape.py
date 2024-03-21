
import argparse
from sys import argv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urldefrag
from PIL import Image
from io import BytesIO
import traceback
import re

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# Dict Keys
css_links = 'css_links'
js_links = 'js_links'
img_links = 'img_links'
font_links = 'font_links'
dir_links = 'all_links'

base_ext = ''
verbose = False


# Function to scrape website and download resources
def scrape_website(url, base_folder, domain, recursive=False, downloaded: dict = None):
    if downloaded is None:
        if verbose:
            print("Initializing Downloaded list")
        global css_links
        global js_links
        global img_links
        global font_links
        global dir_links
        global base_ext
        base_ext = urlparse(url).path
        downloaded = {
            css_links: set(),
            js_links: set(),
            img_links: set(),
            font_links: set(),
            dir_links: set()
        }

    # Fetch the HTML content of the website
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        html_content = response.text
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract CSS links from the HTML and sort the results that are not already downloaded
        linked_css = sorted(
            [link for link in set(format_links([link.get('href') for link in soup.find_all('link', rel='stylesheet')]))
            if link not in downloaded[css_links]])
        
        # Extract JavaScript links from the HTML and sort the results that are not already downloaded
        linked_js = sorted(
            [link for link in set(format_links([script.get('src') for script in soup.find_all('script') if script.get('src')])) 
            if link not in downloaded[js_links]])
        
        # Extract image URLs from the HTML and sort the results that are not already downloaded
        linked_img = sorted(
            [link for link in set(format_links([img.get('src') for img in soup.find_all('img') if img.get('src')])) 
            if link not in downloaded[img_links]])

        # Extract all links from the HTML and sort the results that are not already downloaded
        linked_dirs = sorted(
            [link for link in set(format_download_dirs([link.get('href') for link in soup.find_all('a') if link.get('href')], urlparse(url), domain))
                if link not in downloaded[dir_links]] +
                [link for link in set(format_download_dirs([str(link) for link in soup.find_all('body') if link.get('onload') is not None and link.get('onload').find('window.location=') != -1], urlparse(url), domain))
                if link not in downloaded[dir_links]])
        
        # Extract font URLs from the HTML and sort the results that are not already downloaded
        linked_fonts = []
        for style in soup.find_all('style'):
            for font in style.find_all('font'):
                font_url = font.get('src')
                if font_url and font_url not in downloaded[font_links]:
                    linked_fonts.append(font_url)

        print_dependencies(url, linked_dirs, linked_css, linked_js, linked_img, linked_fonts)

        # Download HTML/PDF file
        download_html(url, html_content, base_folder)
        
        # Download CSS files
        for css_link in linked_css:
            download_file(css_link, base_folder, downloaded[css_links])

        # Download JS files
        for js_link in linked_js:
            download_file(js_link, base_folder, downloaded[js_links])
        
        # Download images
        for img_url in linked_img:
            download_file(img_url, base_folder, downloaded[img_links])
            
        # Download fonts
        for font_url in linked_fonts:
            download_file(font_url, base_folder, downloaded[font_links])


        downloaded[dir_links].add(url)
        if recursive:
            # Recursively scrape and download resources from linked pages
            for link in linked_dirs:
                if link not in downloaded[dir_links]:
                    parsed_link = urlparse(link)
                    if parsed_link.netloc == domain:
                        downloaded[dir_links].add(link)
                        print_move(link)
                        scrape_website(link, base_folder, domain, True, downloaded)
    else:
        downloaded[dir_links].add(url)
        write_failed_response(response.status_code, url)

    return {
        'downloaded': downloaded
    }


# Format a list to allow download from domain 
def format_links(link_list: list):
    for index, link in enumerate(link_list):
        if link[0] == '/' and link[1] != '/':
            link_list[index] = "https://" + domain + link
        elif link[0] == '/' and link[1] == '/':
            link_list[index] = "https://" + link[2:]
        link_list[index] = link_list[index].strip()
    return link_list


# Format the directories list to allow traversal of domain website 
def format_download_dirs(dir_list: list, base_url, domain):
    keep_list = []
    for index, link in enumerate(dir_list):
        if link[0] == '<':
            dir_list[index] = link[link.find('window.location=\"')+len('window.location=\"'):link.find('"\'>')]
        else:
            dir_list[index] = link.strip()

    for link in set(dir_list):
        # replace any leading '../'s if possible
        if re.search('(?:\.\.\/)', link):
            link = remove_relative_directories(link, re.split('/', base_url.path))

        # add https and the domain to the link so that it can be downloaded
        # this is fairly safe as the relative link should be hosted on the same domain
        if link[0] == '/' and len(link) > 1:
            link = "https://" + domain + link

        # assume reference to same level item, if not item will 404 on get request and write failure to failures
        # this is probably wrong
        if not re.search('https?://', link):
            link = "https://" + domain + link

        if re.search('javascript:void\(0\)', link):
            continue

        if link.find('#') != -1:
            link, _ = urldefrag(link)

        parsed_link = urlparse(link)

        # remove query if present
        if (parsed_link.query) != '':
            link = parsed_link._replace(query="").geturl()
        
        # this is a skip for a typo in a url i found that caused issues
        if str(parsed_link.path).find('//') != -1:
            continue

        # skip if not in the correct domain (dont want to download the whole internet)
        if str(parsed_link.netloc).find(domain) == -1:
            continue

        if base_ext not in parsed_link.path:
            continue

        if link.endswith('/'):
            link = link[:-1]

        keep_list.append(link)
    return keep_list


# Downloads HTML/PDF files as some url may respond with either
def download_html(url, html_content, base_folder):
    if verbose:
        print(f'Downloading HTML/PDF for {url}')
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    # if os.path.basename(parsed_url.path).find('GUID') != -1:
    #     # We dont care about GUID pages as these are individual people who may or may not be here
    #     return

    # Some formatting of the name may be required
    if file_name.find('.pdf') == -1 and file_name.find('.html') == -1:
        file_name = 'index.html'

    # Create directories if they don't exist
    relative_path = ''
    if parsed_url.path:
        relative_path = parsed_url.path[1:] if parsed_url.path[0] == '/'  else parsed_url.path

    # Remove the file name from the path if it exists
    if relative_path.find(file_name) != -1:
        relative_path = relative_path[:relative_path.find(file_name)-1]

    download_folder = os.path.join(base_folder, relative_path)
    os.makedirs(download_folder, exist_ok=True)
    with open(os.path.join(download_folder, file_name), 'w', encoding='utf-8') as f:
        f.write(html_content)
        if verbose:
            print(f'SUCCESS: {relative_path}\n')


# Function to download files
def download_file(url, base_folder, downloaded: set): 
    if verbose:
        print(f'Beginning Download: {url}')
    if (url.find("base64") != -1):
        if verbose:
            print("Ignoring Base64 images")
        return
    try:
        response = requests.get(url.strip(), headers=header)
        if response.status_code == 200:
            # Get the relative path of the file
            parsed_url = urlparse(url)
            relative_path = ''
            if parsed_url.path:
                relative_path = parsed_url.path[1:] if parsed_url.path[0] == '/'  else parsed_url.path
            # if parsed_url.query:
            #     relative_path += "?" + parsed_url.query
            filename = os.path.basename(relative_path)

            # Create directories if they don't exist
            download_folder = os.path.join(base_folder, os.path.dirname(relative_path))
            os.makedirs(download_folder, exist_ok=True)

            # Save the file with the relative path 
            if filename.find(".png") != -1:
                png = Image.open(BytesIO(response.content))
                png.save(os.path.join(download_folder, filename))
                if verbose:
                    print(f'SUCCESS: {relative_path}\n')
                    
            else:
                with open(os.path.join(download_folder, filename), 'wb') as f:
                    f.write(response.content)
                    if verbose:
                        print(f'SUCCESS: {relative_path}\n')
            
            # Download and save complete, add to downloaded dict
            downloaded.add(url)
        else:
            write_failed_response(response.status_code, url)

    except Exception as e:
        write_failed_exception(e, url)


# Splits the link into an array. Then uses an array of the original path to replace the relative directory symbols with the real path
def remove_relative_directories(link, path_array):
    download_array = re.split('(?:\.\.\/)', link)
    download_array = download_array[0:-1] + re.split('/', next(s for s in download_array if s))

    # Remove any empty ending arrays potentially caused by the split
    while download_array[len(download_array)-1] == '':
        del download_array[len(download_array)-1]

    # need to make the base-most path the same on both arrays    
    first_directory = next(s for s in download_array if s)
    starting_point = download_array.index(first_directory)
    difference = abs(path_array.index(first_directory) - starting_point)
    if difference != 0:
        for _ in range(0, difference):
            path_array.insert(0, '')

    # Replace the empty indices in download_array with the values in path_array as we know this is a valid path
    for index in range(starting_point-1, -1, -1):
        download_array[index] = path_array[index]

    # Remove all empty indices and replace with a single empty to make a valid url path via the join
    download_array = [path for path in download_array if path != '']
    download_array.insert(0, '')

    return '/'.join(download_array)


def print_dependencies(url, linked_dirs, linked_css, linked_js, linked_img, linked_fonts):
    if verbose:
        print(
        f'''
-------------------------------------------------------------------------
Parsing URL: {url}
This page has the following dependencies not already downloaded:
Referenced Links: {linked_dirs}
Referenced CSS: {linked_css}
Referenced JS: {linked_js}
Referenced Images: {linked_img}
Referenced fonts: {linked_fonts}
-------------------------------------------------------------------------
Starting Downloads.......................................................

        '''
        )


def print_move(link):
    if verbose:

        print(
        f'''
********************************************************************

Moving to first linked dependency: {link}

********************************************************************
        '''
            )


def write_failed_response(status_code, url):
        with open("Scrape_failures.txt", 'a') as txt:
            txt.write(
                f'''
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                FAILURE: {str(status_code)}
                Could not download: {url}
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ''')


def write_failed_exception(e, url):
        with open("Scrape_Failures.txt", 'a') as txt:
            txt.write(
                f'''
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                FAILURE:
                Exception occurred during download of: {url}
                Exception: {e}
                Traceback: {traceback.format_exc()}
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ''')
    
def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="The url to scrape. No url validity checks are performed. Valid URL is assumed.")
    parser.add_argument("-d", "--directory", default="output", help="The specified output directory. Defaults to 'output'. Will be created if non-existent.")
    parser.add_argument("-r", action='store_true', help="Determines whether scraper should recursively scrape links found in url.")
    parser.add_argument("-v", action='store_true', help="Verbose logging")
    return parser.parse_args()



if __name__=="__main__": 
    args = setup_args()
    verbose = args.v
    url = args.url
    directory = args.directory
    domain = urlparse(url).netloc

    if not os.path.exists(directory):
        os.makedirs(os.path.join(os.getcwd(), directory))
        
    data = scrape_website(url=url, base_folder=directory, domain=urlparse(url).netloc, recursive=args.r)
    print(data)