import requests
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def generate_cik_url(cik):
    """Converts a given CIK value to the SEC 13F-HR Page URL.

    Args:
        cik (str): Ticker or CIK.

    Returns:
        string: the complete URL of the 13F-HR page for the CIK on sec.gov.
    """
    return ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
            + str(cik) + "&type=13F-HR&dateb=&owner=exclude&count=20")

def generate_most_recent_13f(target_url):
    """Returns the URL for the most recent 13F-HR filing on sec.gov.

    Args:
        target_url (str): complete URL of the desired security/CIK.

    Returns:
        string: the complete URL of the most recent 13F-HR filing page for
                the given CIK.
    """
    try:
        page = requests.get(target_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(page.text, 'html.parser')

    # handling invalid CIK
    if (soup.find('h1') and
            soup.select('h1')[0].text.startswith("No matching")):
        print("Invalid CIK")
        sys.exit(1)

    links = soup.find_all('a', href=True)
    urls = [link['href'] for link in links
            if link['href'].startswith("/Archives")]

    # select most recent 13F, change urls[0] to get previous reports
    most_recent_13f = "https://www.sec.gov" + urls[0]
    return most_recent_13f

def generate_xml_url(target_13f_url):
    """Returns the URL of the XML file from a given 13F-HR filing page.

    Args:
        target_13f_url (str): complete URL of a 13F-HR filing page from
                              sec.gov.

    Returns:
        string: the complete URL of the 13F-HR XML file on sec.gov.
    """
    try:
        page = requests.get(target_13f_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', href=True)
    urls = [link['href'] for link in links if link.text.endswith(".xml")]
    xml_url = "https://www.sec.gov" + urls[1]
    return xml_url

def write_xml_to_tsv(xml_url, filename):
    """Creates a new TSV file from a given XML file.

    Parses a given XML file from a given URL and creates a new text file
    in the current directory with the header and the rows from the XML file.

    Args:
        xml_url (str): complete URL of a 13F-HR XML file.
        filename (str): filename of the new text file.

    Returns:
        None.
    """
    try:
        page = requests.get(xml_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    root = ET.fromstring(page.text)

    # find holding (child) with largest number of headers to use for TSV
    max_number_of_headers = 0
    model_child = None
    for child in root:
        number_of_headers = 0
        for subchild in child.iter():
            if not list(subchild):
                number_of_headers += 1
        if max_number_of_headers < number_of_headers:
            max_number_of_headers = number_of_headers
            model_child = child

    with open(filename, 'w') as f:

        # get the headers and write to TSV
        headers = []
        for child in model_child.iter():
            if not list(child):
                headers.append(child.tag)
        f.write('\t'.join([header.split('}',1)[1] for header in headers]))
        f.write('\n')

        # parse holdings, handle missing data, and write to TSV
        for child in root:
            newline = ""
            for header in headers:
                has_element = False
                for subchild in child.iter():
                    if subchild.tag == header:
                        newline += (subchild.text + '\t')
                        has_element = True
                # holding doesn't have header, so fill with N/A instead
                if not has_element:
                    newline += ("N/A \t")
            f.write(newline)
            f.write('\n')

    print("Writing to", filename, "...")
    return None

def convert_xml_to_tsv():
    """Main driver function."""
    # select target fund, define output filename
    fund = sys.argv[1]
    filename = sys.argv[2] + ".txt" if len(sys.argv) > 2 else fund + ".txt"

    # get 13F-HR list URL for target fund
    target_url = generate_cik_url(fund)

    # get most recent 13F-HR URL for target fund
    most_recent_13f_url = generate_most_recent_13f(target_url)

    # get 13F-HR XML file URL
    xml_url = generate_xml_url(most_recent_13f_url)

    write_xml_to_tsv(xml_url, filename)


if __name__ == "__main__":
    convert_xml_to_tsv()
    print("Done")
