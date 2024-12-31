"""
Searches arXiv for papers based on author(s), title filter, and year
range. It retrieves paper details such as title, authors, year, PDF
link, and optionally abstracts.

Usage:
    python xarxiv.py "<AUTHORS_QUERY>" <N> "<TITLE_FILTER>" [--start_year YEAR] [--end_year YEAR] [--list] [--abstract]

Parameters:
    <AUTHORS_QUERY>   : Author query prefixed with a logical operator ("AND" or "OR") followed by comma-separated author names.
                        Examples:
                            "AND John Doe, Jim Smith"
                            "OR Alice Johnson, Bob Lee"
    <N>               : Maximum number of PDFs to download (integer).
    <TITLE_FILTER>    : Substring that must appear in the title (e.g., "machine learning"). Use empty quotes "" to skip title filtering.
    [--start_year YEAR] : Start year for publication (inclusive, optional).
    [--end_year YEAR]   : End year for publication (inclusive, optional).
    [--list]            : Optional flag. If specified, the script will only list matching papers without downloading.
    [--abstract]        : Optional flag. If specified, the script will include the abstract of each paper in the listing.

Examples:
    1. Search for papers co-authored by "John Doe" and "Jim Smith" and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" 

    2. Search for papers authored by either "John Doe" or "Jim Smith" and download PDFs:
       python xarxiv.py "OR John Doe, Jim Smith" 10 ""

    3. Search by title only and download PDFs:
       python xarxiv.py "OR" 5 "fortran"

    4. Search by both authors and title substring and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 5 "fortran"

    5. Search by authors within a year range and list papers without downloading:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" --start_year 2015 --end_year 2020 --list

    6. Search by authors, list papers without downloading, and include abstracts:
       python xarxiv.py "OR John Doe, Jim Smith" 10 "" --list --abstract
"""

import os
import re
import sys
import requests
import feedparser
import argparse
import textwrap
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
    # Remove trailing underscores or periods
    filename = filename.strip('_').rstrip('.')
    return filename


def split_authors(authors_query: str):
    """
    Splits the authors query into operator and list of authors.

    Parameters:
        authors_query (str): A string starting with a logical operator followed by comma-separated author names.

    Returns:
        tuple: (operator, list_of_authors)
    """
    # Regex to capture operator and authors
    match = re.match(r'^(AND|OR)\s+(.*)$', authors_query.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Invalid AUTHORS_QUERY format. It should start with 'AND' or 'OR' followed by author names.")
    
    operator = match.group(1).upper()
    authors_str = match.group(2)
    # Split authors by comma and strip whitespace
    authors = [author.strip() for author in authors_str.split(',') if author.strip()]
    
    if not authors:
        raise ValueError("No authors specified in AUTHORS_QUERY.")
    
    return operator, authors


def build_arxiv_query(operator: str, authors: list) -> str:
    """
    Constructs the arXiv API query string based on the logical operator and list of authors.

    Parameters:
        operator (str): Logical operator ("AND" or "OR").
        authors (list): List of author names.

    Returns:
        str: Formatted arXiv query string.
    """
    if operator not in {"AND", "OR"}:
        raise ValueError("Logical operator must be 'AND' or 'OR'.")
    
    # Construct individual author queries
    author_queries = [f'au:"{author}"' for author in authors]
    
    # Join with the specified operator
    combined_query = f' {operator} '.join(author_queries)
    
    return combined_query


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


def capitalize_author_names(authors_str):
    """
    Capitalize the authors' names appropriately, handling special characters.

    Parameters:
        authors_str (str): A string containing authors' names separated by commas.

    Returns:
        str: A string with each author's name capitalized.
    """
    authors = authors_str.split(',')
    capitalized_authors = []
    for author in authors:
        author = author.strip()
        # Handle hyphens and apostrophes
        # Split by space to handle first and last names
        parts = author.split(' ')
        capitalized_parts = []
        for part in parts:
            # Further split by hyphen and apostrophe
            sub_parts = re.split("([-'])", part)  # Keep the delimiter
            capitalized_sub_parts = [
                sub_part.capitalize() if sub_part not in ["-", "'"] else sub_part
                for sub_part in sub_parts
            ]
            capitalized_part = ''.join(capitalized_sub_parts)
            capitalized_parts.append(capitalized_part)
        capitalized_author = ' '.join(capitalized_parts)
        capitalized_authors.append(capitalized_author)
    return ', '.join(capitalized_authors)


def search_arxiv(authors_query: str, max_papers: int = 5, title_filter: str = "",
                start_year: int = None, end_year: int = None):
    """
    Searches arXiv for papers based on authors, title filter, and year range.

    Parameters:
    - authors_query: Author query string starting with a logical operator followed by author names.
    - max_papers: Maximum number of PDFs to retrieve
    - title_filter: Substring that must appear in the title (optional)
    - start_year: Start year for publication (inclusive, optional)
    - end_year: End year for publication (inclusive, optional)

    Returns:
    - List of tuples: (title, authors, year, pdf_url, abstract)
    """
    # Parse authors query
    operator, authors = split_authors(authors_query)
    
    # Build arXiv query
    combined_query = build_arxiv_query(operator, authors)
    
    # URL encode the search query
    encoded_query = quote_plus(combined_query)
    
    # Define a reasonable width for wrapping
    wrap_width = 80  # You can adjust this as needed
    
    # Construct the API query URL
    query_url = (
        f'http://export.arxiv.org/api/query?search_query={encoded_query}'
        f'&start=0&max_results={max_papers}&sortBy=lastUpdatedDate&sortOrder=descending'
    )
    
    # Include title filter if provided
    if title_filter.strip():
        title_encoded = quote_plus(f'ti:"{title_filter}"')
        query_url += f'&title_filter={title_encoded}'
    
    print(f"Searching arXiv with query: {combined_query}")
    if title_filter.strip():
        print(f"Title Filter: {title_filter}")
    print()
    
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
    
    for entry in feed.entries:
        title = ' '.join(entry.title.strip().split())  # Normalize spaces
        abstract = ' '.join(entry.summary.strip().split())  # Normalize spaces
        
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
        
        # Authors extraction
        authors = [a.get('name', '') for a in entry.authors]
        authors_str = ', '.join(authors)
        
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
            results.append((title, authors_str, published_year, pdf_link, abstract))
    
    return results


def download_papers(
    authors_query: str, 
    n: int = 5, 
    title_filter: str = "",
    start_year: int = None,
    end_year: int = None,
    list_only: bool = False,
    include_abstract: bool = False
):
    """
    Orchestrates the search on arXiv and optionally downloads the PDFs.

    Parameters:
    - authors_query: Author query string starting with a logical operator followed by author names.
    - n: Maximum number of PDFs to download
    - title_filter: Substring that must appear in the title (optional)
    - start_year: Start year for publication (inclusive, optional)
    - end_year: End year for publication (inclusive, optional)
    - list_only: If True, only prints matching papers without downloading
    - include_abstract: If True, includes the abstract in the listing
    """
    # Search arXiv
    try:
        arxiv_results = search_arxiv(
            authors_query=authors_query,
            max_papers=n,
            title_filter=title_filter,
            start_year=start_year,
            end_year=end_year
        )
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    
    if not arxiv_results:
        print("No papers found matching the criteria.\n")
        return
    
    if list_only:
        print(f"Found {len(arxiv_results)} paper(s) matching the criteria:\n")
        for i, (title, authors, year, pdf_url, abstract) in enumerate(arxiv_results, start=1):
            # Capitalize authors' names
            authors_capitalized = capitalize_author_names(authors)
            # Prepare prefix and padding for alignment
            prefix = f"[{i}]  Title"  # Added two spaces after the index
            padding = ' ' * (14 - len(prefix)) if len(prefix) < 14 else ' '
            # Wrap the title using textwrap with adjusted indentation
            wrapped_title = textwrap.fill(
                title,
                width=80,
                initial_indent=f"{prefix}{padding}: ",
                subsequent_indent=' ' * 16  # 14 spaces for alignment + 2 spaces
            )
            print(wrapped_title)
            # Format Authors
            authors_prefix = "    Authors"
            padding_authors = ' ' * (14 - len(authors_prefix)) if len(authors_prefix) < 14 else ' '
            print(f"{authors_prefix}{padding_authors}: {authors_capitalized}")
            # Format Year
            year_prefix = "    Year"
            padding_year = ' ' * (14 - len(year_prefix)) if len(year_prefix) < 14 else ' '
            print(f"{year_prefix}{padding_year}: {year}")
            # Format PDF Link
            pdf_prefix = "    PDF Link"
            padding_pdf = ' ' * (14 - len(pdf_prefix)) if len(pdf_prefix) < 14 else ' '
            print(f"{pdf_prefix}{padding_pdf}: {pdf_url}")
            # Format Abstract if flag is set
            if include_abstract:
                abstract_prefix = "    Abstract"
                padding_abstract = ' ' * (14 - len(abstract_prefix)) if len(abstract_prefix) < 14 else ' '
                wrapped_abstract = textwrap.fill(
                    abstract,
                    width=80,
                    initial_indent=f"{abstract_prefix}{padding_abstract}: ",
                    subsequent_indent=' ' * 16  # 14 spaces for alignment + 2 spaces
                )
                print(f"{wrapped_abstract}\n")
            else:
                print()  # Add an empty line for spacing
    else:
        print(f"Found {len(arxiv_results)} paper(s). Starting download...\n")
        for i, (title, authors, year, pdf_url, abstract) in enumerate(arxiv_results, start=1):
            # Process the title for filename
            sanitized_title = sanitize_filename(title.lower())
            # Split authors to extract first and last names for filename
            authors_list = [author.strip() for author in authors.split(',') if author.strip()]
            if authors_list:
                # Take the first author's first and last name
                first_author = authors_list[0].split()
                if len(first_author) >= 2:
                    first_name = first_author[0].lower()
                    last_name = first_author[-1].lower()
                else:
                    first_name = ""
                    last_name = first_author[0].lower()
            else:
                first_name = ""
                last_name = ""
            filename = build_filename(first_name, last_name, sanitized_title)
            
            print(f"[{i}] Downloading: {title}")
            # Capitalize authors' names
            authors_capitalized = capitalize_author_names(authors)
            print(f"    Authors     : {authors_capitalized}")
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
        
        print("Process completed.")


def print_usage():
    """
    Prints the usage instructions.
    """
    usage_text = """
Usage:
    python xarxiv.py "<AUTHORS_QUERY>" <N> "<TITLE_FILTER>" [--start_year YEAR] [--end_year YEAR] [--list] [--abstract]

Parameters:
    <AUTHORS_QUERY>   : Author query prefixed with a logical operator ("AND" or "OR") followed by comma-separated author names.
                        Examples:
                            "AND John Doe, Jim Smith"
                            "OR Alice Johnson, Bob Lee"
    <N>               : Maximum number of PDFs to download (integer).
    <TITLE_FILTER>    : Substring that must appear in the title (e.g., "machine learning"). Use empty quotes "" to skip title filtering.
    [--start_year YEAR] : Start year for publication (inclusive, optional).
    [--end_year YEAR]   : End year for publication (inclusive, optional).
    [--list]            : Optional flag. If specified, the script will only list matching papers without downloading.
    [--abstract]        : Optional flag. If specified, the script will include the abstract of each paper in the listing.

Examples:
    1. Search for papers co-authored by "John Doe" and "Jim Smith" and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" 

    2. Search for papers authored by either "John Doe" or "Jim Smith" and download PDFs:
       python xarxiv.py "OR John Doe, Jim Smith" 10 ""

    3. Search by title only and download PDFs:
       python xarxiv.py "OR" 5 "fortran"

    4. Search by both authors and title substring and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 5 "fortran"

    5. Search by authors within a year range and list papers without downloading:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" --start_year 2015 --end_year 2020 --list

    6. Search by authors, list papers without downloading, and include abstracts:
       python xarxiv.py "OR John Doe, Jim Smith" 10 "" --list --abstract
    """
    print(usage_text)


def main():
    """
    Main function to parse arguments and initiate the download or listing process.
    """
    parser = argparse.ArgumentParser(
        description="Search and download papers from arXiv based on authors, title, and year range filters.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
    1. Search for papers co-authored by "John Doe" and "Jim Smith" and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" 

    2. Search for papers authored by either "John Doe" or "Jim Smith" and download PDFs:
       python xarxiv.py "OR John Doe, Jim Smith" 10 ""

    3. Search by title only and download PDFs:
       python xarxiv.py "OR" 5 "fortran"

    4. Search by both authors and title substring and download PDFs:
       python xarxiv.py "AND John Doe, Jim Smith" 5 "fortran"

    5. Search by authors within a year range and list papers without downloading:
       python xarxiv.py "AND John Doe, Jim Smith" 10 "" --start_year 2015 --end_year 2020 --list

    6. Search by authors, list papers without downloading, and include abstracts:
       python xarxiv.py "OR John Doe, Jim Smith" 10 "" --list --abstract
"""
    )

    # Positional arguments
    parser.add_argument('authors_query', type=str, help='Author query with logical operator (e.g., "AND John Doe, Jim Smith")')
    parser.add_argument('n', type=int, help='Maximum number of PDFs to download')
    parser.add_argument('title_filter', type=str, help='Substring to filter titles (use "" to skip)')

    # Optional arguments
    parser.add_argument('--start_year', type=int, help='Start year for publication (inclusive)', default=None)
    parser.add_argument('--end_year', type=int, help='End year for publication (inclusive)', default=None)
    parser.add_argument('--list', action='store_true', help='List matching papers without downloading')
    parser.add_argument('--abstract', action='store_true', help='Include abstracts in the listing')

    args = parser.parse_args()

    # Extract arguments
    authors_query = args.authors_query
    n_pdfs = args.n
    title_filter = args.title_filter
    start_year = args.start_year
    end_year = args.end_year
    list_only = args.list
    include_abstract = args.abstract

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
    print("=== arXiv PDF Downloader and Formatter ===\n")
    print(f"Author Query     : {authors_query}")
    print(f"Title Filter     : {'None' if not title_filter.strip() else title_filter}")
    print(f"Year Range       : {'None' if not (start_year or end_year) else f'{start_year if start_year else "-∞"} to {end_year if end_year else "∞"}'}")
    print(f"Number of PDFs   : {n_pdfs}")
    action = 'List only' if list_only else 'Download PDFs and List'
    if include_abstract:
        action += ' with Abstracts'
    print(f"Action           : {action}\n")

    # Start the process
    download_papers(
        authors_query=authors_query,
        n=n_pdfs,
        title_filter=title_filter,
        start_year=start_year,
        end_year=end_year,
        list_only=list_only,
        include_abstract=include_abstract
    )

    print("Process completed.")


if __name__ == "__main__":
    main()
