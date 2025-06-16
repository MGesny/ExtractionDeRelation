from lxml import html
from urllib.parse import urljoin
import os

def get_all_hrefs_from_file(file_path, xpath, base_url=None):
    """
    Extract all hrefs from nodes matching XPath in a local HTML file
    
    Args:
        file_path: Path to the HTML file
        xpath: XPath expression to find nodes
        base_url: Optional base URL for resolving relative URLs
        
    Returns:
        List of absolute hrefs
    """
    try:
        # Verify file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Read HTML content
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML
        tree = html.fromstring(html_content)
        
        # Find all matching parent nodes
        parent_nodes = tree.xpath(xpath)
        
        # Collect all unique hrefs
        all_hrefs = set()
        
        for parent in parent_nodes:
            # Get href from parent node itself if it exists
            parent_href = parent.get('href')
            if parent_href:
                all_hrefs.add(urljoin(base_url, parent_href)) if base_url else parent_href
            
            # Get hrefs from all descendant nodes
            child_hrefs = parent.xpath(".//@href")
            for href in child_hrefs:
                all_hrefs.add(urljoin(base_url, href) if base_url else href)
        
        return sorted(all_hrefs)  # Return as sorted list for consistency
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

import requests
from lxml import html

def get_elements_by_class_part(url):
    try:
        # Fetch the webpage
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        tree = html.fromstring(response.content)
        
        # Construct the XPath
        xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "Paragraph__content", " " ))]'
        
        # Find all elements matching the XPath
        elements = tree.xpath(xpath)
        
        print(f"Found {len(elements)} elements")
        texte=[]
        # Print information about found elements
        for i, element in enumerate(elements, 1):
            texte.append(element.text_content())
        texte=" ".join(texte)
        return texte.replace("Ã¹","ù").replace("Ã§","ç").replace("Ã¨","è").replace("Ã©","é").replace("Ã®","î").replace("Ã«","ë").replace("Ã ","à").replace("Ãª","ê")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_text_to_file(text, filename, mode='w', encoding='utf-8'):
    """
    Save text to a .txt file.
    
    Parameters:
        text (str): The text content to save
        filename (str): Name/path of the file to create (include .txt extension)
        mode (str): File mode - 'w' for write (default), 'a' for append
        encoding (str): Text encoding (default: 'utf-8')
    
    Returns:
        bool: True if successful, False if error occurs
    """
    try:
        with open(filename, mode, encoding=encoding) as file:
            file.write(text)
        print(f"Text successfully saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False
# Example usage
if __name__ == "__main__":
    # Configure these values
    listehref={}
    for namehandballeur in ["elohimprandi","nikolakarabatic","lucabalo","valentinporte","dikamem","yannislenne"]:
        html_file_path = "C:/Users/mathu/Downloads/"+namehandballeur+"lequipe.html"  # Path to your HTML file
        xpath_expression = '//*[contains(concat( " ", @class, " " ), concat( " ", "SearchResult__item", " " ))]'
        website_base_url = ""  # Optional - for making relative URLs absolute
        
        # Get the hrefs
        hrefs = get_all_hrefs_from_file(
            file_path=html_file_path,
            xpath=xpath_expression,
            base_url=website_base_url
        )
        
        # Print results
        print(f"\nFound {len(hrefs)} unique hrefs for {namehandballeur}")
        listehref[namehandballeur]=hrefs
        
    
    print(listehref)
    for namehandballeur in ["elohimprandi","nikolakarabatic","lucabalo","valentinporte","dikamem","yannislenne"]:
        for i,fin_url in enumerate(listehref[namehandballeur]):
            url = "https://lequipe.fr"+fin_url

            print(url)

            save_text_to_file(get_elements_by_class_part(url), f"C:/Users/mathu/Documents/2024-2025/Stage/Texte/{namehandballeur}-text{i}.txt")