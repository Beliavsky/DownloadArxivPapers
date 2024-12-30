import os
import re
import sys
import requests
import feedparser
import argparse
from urllib.parse import quote_plus
from datetime import datetime

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


def search_arxiv(researcher_name: str, max_papers: int = 5, title_filter: str = "",
                start_year: int = None, end_year: int = None):
    """
    Searches arXiv for papers based on author, title filter, and year range.
    
    Parameters:
    - researcher_name: Author's full name (optional)
    - max_papers: Maximum number of PDFs to retrieve
    - title_filter: Substring that must appear in the title (optional)
    - start_year: Start year for publication (inclusive, optional)
    - end_year: End year for publication (inclusive, optional)
    
    Returns:
    - List of tuples: (title, authors, year, pdf_url)
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
    
    # Prepare year range
    if start_year:
        start_date = datetime(start_year, 1, 1)
    if end_year:
        end_date = datetime(end_year, 12, 31)
    
    # Split the input name for substring matching
    if researcher_name.strip():
        target_name_lower = researcher_name.lower()
    
    for entry in feed.entries:
        title = entry.title.strip()
        
        # Title filter check (redundant if title_filter is used in the query, but kept for safety)
        if title_filter and (title_filter_lower not in title.lower()):
            continue
        
        # Year range filter
        published_str = entry.published
        try:
            published_date = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
            published_year = published_date.year
        except ValueError:
            # If date parsing fails, skip this entry
            continue
        
        if start_year and published_year < start_year:
            continue
        if end_year and published_year > end_year:
            continue
        
        # If author filter is provided, verify the authors contain the substring
        if researcher_name.strip():
            authors = [a.get('name', '').lower() for a in entry.authors]
            # Check if any author's name contains the target substring
            if not any(target_name_lower in author for author in authors):
                continue
        else:
            # If no author filter, retrieve authors for listing purposes
            authors = [a.get('name', '') for a in entry.authors]
        
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
            # Join authors into a single string
            authors_str = ', '.join(authors)
            results.append((title, authors_str, published_year, pdf_link))
    
    return results


def download_papers(
    researcher_name: str, 
    n: int = 5, 
    title_filter: str = "",
    start_year: int = None,
    end_year: int = None,
    list_only: bool = False
):
    """
    Orchestrates the search on arXiv and optionally downloads the PDFs.
    
    Parameters:
    - researcher_name: Author's full name (optional)
    - n: Maximum number of PDFs to download
    - title_filter: Substring that must appear in the title (optional)
    - start_year: Start year for publication (inclusive, optional)
    - end_year: End year for publication (inclusive, optional)
    - list_only: If True, only prints matching papers without downloading
    """
    first_name, last_name = split_name(researcher_name)
    
    # Search arXiv
    arxiv_results = search_arxiv(
        researcher_name=researcher_name,
        max_papers=n,
        title_filter=title_filter,
        start_year=start_year,
        end_year=end_year
    )
    
    # Limit the results to n
    arxiv_results = arxiv_results[:n]
    
    if not arxiv_results:
        print("No papers found matching the criteria.\n")
        return
    
    if list_only:
        print(f"Found {len(arxiv_results)} paper(s) matching the criteria:\n")
        for i, (title, authors, year, pdf_url) in enumerate(arxiv_results, start=1):
            print(f"[{i}] Title       : {title}")
            print(f"    Authors     : {authors}")
            print(f"    Year        : {year}")
            print(f"    PDF Link    : {pdf_url}\n")
    else:
        print(f"Found {len(arxiv_results)} paper(s). Starting download...\n")
        for i, (title, authors, year, pdf_url) in enumerate(arxiv_results, start=1):
            # Process the title for filename
            sanitized_title = sanitize_filename(title.lower())
            filename = build_filename(first_name, last_name, sanitized_title)
            
            print(f"[{i}] Downloading: {title}")
            print(f"    Authors     : {authors}")
            print(f"    Year        : {year}")
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
    python xdownload_papers_arxiv.py "<RESEARCHER_NAME>" <N> "<TITLE_FILTER>" [--start_year YEAR] [--end_year YEAR] [--list]
    
Parameters:
    <RESEARCHER_NAME> : Author's full name (e.g., "Marvin Lettau"). 
                        Use empty quotes "" to skip author filtering.
    <N>               : Maximum number of PDFs to download (integer).
    <TITLE_FILTER>    : Substring to filter titles (e.g., "machine learning").
                        Use empty quotes "" to skip title filtering.
    [--start_year YEAR] : Start year for publication (inclusive, optional).
    [--end_year YEAR]   : End year for publication (inclusive, optional).
    [--list]            : Optional flag. If specified, the script will only list matching papers without downloading.
    
Examples:
    1. Search by author only and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 ""
    
    2. Search by title only and download PDFs:
       python xdownload_papers_arxiv.py "" 5 "fortran"
    
    3. Search by both author and title substring and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 "fortran"
    
    4. Search by author and title substring within a year range and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 "fortran" --start_year 2015 --end_year 2020
    
    5. Search by title only within a year range and list papers without downloading:
       python xdownload_papers_arxiv.py "" 5 "fortran" --start_year 2010 --end_year 2020 --list
    """
    print(usage_text)


def main():
    """
    Main function to parse arguments and initiate the download or listing process.
    """
    parser = argparse.ArgumentParser(
        description="Search and download papers from arXiv based on author, title, and year range filters.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
    1. Search by author only and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 ""
    
    2. Search by title only and download PDFs:
       python xdownload_papers_arxiv.py "" 5 "fortran"
    
    3. Search by both author and title substring and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 "fortran"
    
    4. Search by author and title substring within a year range and download PDFs:
       python xdownload_papers_arxiv.py "Richardson" 5 "fortran" --start_year 2015 --end_year 2020
    
    5. Search by title only within a year range and list papers without downloading:
       python xdownload_papers_arxiv.py "" 5 "fortran" --start_year 2010 --end_year 2020 --list
"""
    )
    
    # Positional arguments
    parser.add_argument('researcher_name', type=str, help='Author\'s full name (use "" to skip)')
    parser.add_argument('n', type=int, help='Maximum number of PDFs to download')
    parser.add_argument('title_filter', type=str, help='Substring to filter titles (use "" to skip)')
    
    # Optional arguments
    parser.add_argument('--start_year', type=int, help='Start year for publication (inclusive)', default=None)
    parser.add_argument('--end_year', type=int, help='End year for publication (inclusive)', default=None)
    parser.add_argument('--list', action='store_true', help='List matching papers without downloading')
    
    args = parser.parse_args()
    
    # Extract arguments
    name_input = args.researcher_name
    n_pdfs = args.n
    title_filter = args.title_filter
    start_year = args.start_year
    end_year = args.end_year
    list_only = args.list
    
    # Validate 'n_pdfs'
    if n_pdfs <= 0:
        print("Error: <N> must be a positive integer.\n")
        print_usage()
        sys.exit(1)
    
    # Validate year range
    if start_year and end_year and start_year > end_year:
        print("Error: --start_year cannot be greater than --end_year.\n")
        print_usage()
        sys.exit(1)
    
    # Display the search criteria
    print("=== arXiv PDF Downloader ===\n")
    print(f"Author Filter    : {'None' if not name_input.strip() else name_input}")
    print(f"Title Filter     : {'None' if not title_filter.strip() else title_filter}")
    print(f"Year Range       : {'None' if not (start_year or end_year) else f'{start_year if start_year else "-∞"} to {end_year if end_year else "∞"}'}")
    print(f"Number of PDFs   : {n_pdfs}")
    print(f"Action           : {'List only' if list_only else 'Download PDFs'}\n")
    
    # Start the process
    download_papers(
        researcher_name=name_input,
        n=n_pdfs,
        title_filter=title_filter,
        start_year=start_year,
        end_year=end_year,
        list_only=list_only
    )
    
    print("Process completed.")


if __name__ == "__main__":
    main()
