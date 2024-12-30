import os
import re
import sys
import requests
import feedparser
from urllib.parse import quote_plus

# Configure stdout to handle UTF-8 encoding to prevent UnicodeEncodeError
if sys.version_info >= (3, 7):
    # Python 3.7+ supports reconfigure
    sys.stdout.reconfigure(encoding='utf-8')
else:
    # For older versions, use a workaround
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

def sanitize_filename(filename: str) -> str:
    """
    Remove or replace characters that are not suitable for filenames.
    Replaces invalid characters with underscores and trims trailing periods/spaces.
    """
    # Replace invalid characters with underscores
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Replace any remaining whitespace (including newlines) with underscores
    filename = re.sub(r'\s+', '_', filename)
    # Remove trailing periods or underscores
    filename = filename.strip('_').rstrip('.')
    return filename

def split_name(researcher_name: str):
    """
    Splits the researcher's full name into (first_name, last_name).
    - If only one name is provided, it's treated as the last name.
    - If the name is empty, both first_name and last_name are empty.
    """
    if not researcher_name.strip():
        return "", ""
    
    parts = researcher_name.strip().split()
    if len(parts) == 1:
        # Only one name provided
        return "", parts[0].lower()
    else:
        # Multiple parts: first and last
        first_name = parts[0].lower()
        last_name = parts[-1].lower()
        return first_name, last_name

def build_filename(first_name: str, last_name: str, title: str) -> str:
    """
    Constructs the filename based on available name parts and title.
    - If both first and last names are provided: first_last_title.pdf
    - If only last name is provided: last_title.pdf
    - If no name is provided: title.pdf
    """
    if first_name and last_name:
        return f"{first_name}_{last_name}_{title}.pdf"
    elif last_name:
        return f"{last_name}_{title}.pdf"
    else:
        return f"{title}.pdf"

def search_arxiv(researcher_name: str, max_papers: int = 5, title_filter: str = ""):
    """
    Searches arXiv for papers based on author and/or title filter.
    
    Parameters:
    - researcher_name: Author's full name (optional)
    - max_papers: Maximum number of PDFs to download
    - title_filter: Substring that must appear in the title (optional)
    
    Returns:
    - List of tuples: (title, pdf_url)
    """
    # Build the search query
    queries = []
    if researcher_name.strip():
        # Author-based search (exact or partial match)
        author_query = f'au:"{researcher_name}"'
        queries.append(author_query)
    if title_filter.strip():
        # Title-based search
        title_query = f'ti:"{title_filter}"'
        queries.append(title_query)
    
    if not queries:
        # If no filters provided, perform a broad search (not recommended)
        search_query = 'all:"all"'
    else:
        # Combine queries with AND
        search_query = ' AND '.join(queries)
    
    # URL encode the search query
    encoded_query = quote_plus(search_query)
    
    # Construct the API query URL
    query_url = (
        f'http://export.arxiv.org/api/query?search_query={encoded_query}'
        f'&start=0&max_results={max_papers}&sortBy=lastUpdatedDate&sortOrder=descending'
    )
    
    print(f"Searching arXiv with query: {search_query}\n")
    
    # Parse the feed
    feed = feedparser.parse(query_url)
    results = []
    
    # Normalize the title filter for case-insensitive comparison
    title_filter_lower = title_filter.lower()
    
    # Split the input name for substring matching
    if researcher_name.strip():
        target_name_lower = researcher_name.lower()
    
    for entry in feed.entries:
        title = entry.title.strip()
        
        # Title filter check (redundant if title_filter is used in the query, but kept for safety)
        if title_filter and (title_filter_lower not in title.lower()):
            continue
        
        # If author filter is provided, verify the authors contain the substring
        if researcher_name.strip():
            authors = [a.get('name', '').lower() for a in entry.authors]
            # Check if any author's name contains the target substring
            if not any(target_name_lower in author for author in authors):
                continue
        
        # Retrieve the PDF link
        pdf_link = None
        for link in entry.links:
            if link.rel == 'related' and link.type == 'application/pdf':
                pdf_link = link.href
                break
            elif link.type == 'application/pdf':
                pdf_link = link.href
                break
        
        if pdf_link:
            results.append((title, pdf_link))
    
    return results

def download_papers(
    researcher_name: str, 
    n: int = 5, 
    title_filter: str = ""
):
    """
    Orchestrates the search on arXiv and downloads the PDFs.
    
    Parameters:
    - researcher_name: Author's full name (optional)
    - n: Maximum number of PDFs to download
    - title_filter: Substring that must appear in the title (optional)
    """
    first_name, last_name = split_name(researcher_name)
    
    # Search arXiv
    arxiv_results = search_arxiv(
        researcher_name=researcher_name,
        max_papers=n,
        title_filter=title_filter
    )
    
    # Limit the results to n
    arxiv_results = arxiv_results[:n]
    
    if not arxiv_results:
        print("No papers found matching the criteria.\n")
        return
    
    print(f"Found {len(arxiv_results)} paper(s). Starting download...\n")
    
    for i, (title, pdf_url) in enumerate(arxiv_results, start=1):
        # Process the title for filename
        sanitized_title = sanitize_filename(title.lower())
        filename = build_filename(first_name, last_name, sanitized_title)
        
        print(f"[{i}] Downloading: {title}")
        print(f"    from: {pdf_url}")
        
        try:
            response = requests.get(pdf_url, stream=True, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"    Error downloading PDF: {e}\n")
            continue
        
        # Save the PDF to disk
        try:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"    Saved as: {filename}\n")
        except OSError as e:
            print(f"    Error saving file '{filename}': {e}\n")
            continue

def print_usage():
    """
    Prints the usage instructions.
    """
    usage_text = """
Usage:
    python xdownload_papers_arxiv.py "<RESEARCHER_NAME>" <N> "<TITLE_FILTER>"

Parameters:
    <RESEARCHER_NAME> : Author's full name (e.g., "Marvin Lettau"). 
                        Use empty quotes "" to skip author filtering.
    <N>               : Maximum number of PDFs to download (integer).
    <TITLE_FILTER>    : Substring to filter titles (e.g., "machine learning").
                        Use empty quotes "" to skip title filtering.

Examples:
    1. Search by author only:
       python xdownload_papers_arxiv.py "Richardson" 5 ""

    2. Search by title only:
       python xdownload_papers_arxiv.py "" 5 "fortran"

    3. Search by both author and title:
       python xdownload_papers_arxiv.py "Richardson" 5 "fortran"
"""
    print(usage_text)

if __name__ == "__main__":
    """
    Entry point of the script. Parses command-line arguments and initiates the download.
    """
    # Ensure at least N is provided
    if len(sys.argv) < 3:
        print("Error: Not enough arguments provided.\n")
        print_usage()
        sys.exit(1)
    
    # Parse command-line arguments
    name_input = sys.argv[1]
    
    try:
        n_pdfs = int(sys.argv[2])
        if n_pdfs <= 0:
            raise ValueError
    except ValueError:
        print("Error: <N> must be a positive integer.\n")
        print_usage()
        sys.exit(1)
    
    # Title filter is optional
    if len(sys.argv) >= 4:
        title_filter = sys.argv[3]
    else:
        title_filter = ""
    
    # Display the search criteria
    print("=== arXiv PDF Downloader ===\n")
    print(f"Author Filter    : {'None' if not name_input.strip() else name_input}")
    print(f"Title Filter     : {'None' if not title_filter.strip() else title_filter}")
    print(f"Number of PDFs   : {n_pdfs}\n")
    
    # Start downloading
    download_papers(
        researcher_name=name_input,
        n=n_pdfs,
        title_filter=title_filter
    )
    
    print("Download process completed.")
