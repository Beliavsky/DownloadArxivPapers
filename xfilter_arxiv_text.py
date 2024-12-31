#!/usr/bin/env python3
"""
xfilter_arxiv_text.py

A script to filter arXiv search results saved in a human-readable text file using a query string similar to arXiv's search syntax.

Usage:
    python xfilter_arxiv_text.py <input_text_file> "<QUERY_STRING>" [--save_as OUTPUT_TEXT]

Parameters:
    <input_text_file> : Path to the text file containing arXiv search results.
    <QUERY_STRING>    : Query string to filter the results (e.g., 'ti:"machine learning" AND au:"John Doe"').

Optional Arguments:
    --save_as OUTPUT_TEXT : If specified, saves the filtered results to the given text file.

Examples:
    1. Filter by title only:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"realized volatility"' --save_as filtered_results.txt

    2. Filter by title and author:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"machine learning" AND au:"Jane Smith"' --save_as ml_jane.txt

    3. Filter with OR operator:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'au:"John Doe" OR au:"Jane Smith"'

    4. Complex query with parentheses:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"machine learning" AND (au:"Jane Smith" OR year:2022)' --save_as complex_filter.txt
"""

import argparse
import re
import sys
from typing import List, Dict, Any, Callable, Optional
import io
import textwrap

# Configure stdout to handle UTF-8 encoding to prevent UnicodeEncodeError
try:
    # Python 3.7+
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # For older versions
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter arXiv search results saved in a text file using a query string similar to arXiv's search syntax.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
    1. Filter by title only:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"realized volatility"' --save_as filtered_results.txt

    2. Filter by title and author:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"machine learning" AND au:"Jane Smith"' --save_as ml_jane.txt

    3. Filter with OR operator:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'au:"John Doe" OR au:"Jane Smith"'

    4. Complex query with parentheses:
        python xfilter_arxiv_text.py arxiv_search_output.txt 'ti:"machine learning" AND (au:"Jane Smith" OR year:2022)' --save_as complex_filter.txt
"""
    )
    parser.add_argument('input_text_file', type=str, help='Path to the text file containing arXiv search results.')
    parser.add_argument('query_string', type=str, help='Query string to filter the results (e.g., \'ti:"machine learning" AND au:"John Doe"\').')
    parser.add_argument('--save_as', type=str, help='Path to save the filtered results as a text file.', default=None)
    return parser.parse_args()

def load_papers(file_path: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)
    
    # Split content into lines
    lines = content.splitlines()
    
    papers = []
    current_paper = {}
    in_papers_section = False
    
    # Define patterns for fields
    title_pattern = re.compile(r'\[(\d+)\]\s+Title\s*:\s*(.+)', re.IGNORECASE)
    authors_pattern = re.compile(r'\s+Authors\s*:\s*(.+)', re.IGNORECASE)
    year_pattern = re.compile(r'\s+Year\s*:\s*(\d{4})', re.IGNORECASE)
    category_pattern = re.compile(r'\s+Category\s*:\s*([\w\.\-]+)', re.IGNORECASE)
    pdf_link_pattern = re.compile(r'\s+PDF Link\s*:\s*(http[s]?://\S+)', re.IGNORECASE)
    
    i = 0
    while i < len(lines):
        line = lines[i]
        # Identify the start of the papers section
        if line.strip().startswith("Found"):
            in_papers_section = True
            i +=1
            continue
        if not in_papers_section:
            i +=1
            continue
        # Identify each paper entry starting with [number]
        title_match = title_pattern.match(line)
        if title_match:
            if current_paper:
                papers.append(current_paper)
                current_paper = {}
            current_paper['title'] = title_match.group(2).strip()
            i +=1
            # Check for continuation lines
            while i < len(lines):
                next_line = lines[i]
                # If next_line matches any field, break
                if (authors_pattern.match(next_line) or
                    year_pattern.match(next_line) or
                    category_pattern.match(next_line) or
                    pdf_link_pattern.match(next_line) or
                    title_pattern.match(next_line)):
                    break
                # If next_line is not empty and indented, assume it's a continuation of the title
                if next_line.strip() != "" and (next_line.startswith(' ') or next_line.startswith('\t')):
                    current_paper['title'] += ' ' + next_line.strip()
                    i +=1
                else:
                    break
            continue
        # Extract other fields
        authors_match = authors_pattern.match(line)
        if authors_match:
            authors_str = authors_match.group(1).strip()
            # Split authors by comma and strip whitespace
            authors = [author.strip() for author in authors_str.split(',')]
            current_paper['authors'] = authors
            i +=1
            continue
        year_match = year_pattern.match(line)
        if year_match:
            current_paper['year'] = int(year_match.group(1))
            i +=1
            continue
        category_match = category_pattern.match(line)
        if category_match:
            current_paper['category'] = category_match.group(1).strip()
            i +=1
            continue
        pdf_link_match = pdf_link_pattern.match(line)
        if pdf_link_match:
            current_paper['pdf_link'] = pdf_link_match.group(1).strip()
            i +=1
            continue
        # If line doesn't match any pattern, skip
        i +=1
    # Add the last paper if exists
    if current_paper:
        papers.append(current_paper)
    
    return papers

def tokenize_query(query: str) -> List[str]:
    """
    Tokenizes the query string into a list of tokens.
    Supports:
    - Field-specific searches: ti:"machine learning" or ti:machine
    - Logical operators: AND, OR
    - Parentheses: (, )
    """
    # Updated regex to allow for quoted and unquoted values
    token_pattern = re.compile(
        r'\s*(AND|OR|\(|\)|ti:"[^"]+"|ti:[^\s()]+|au:"[^"]+"|au:[^\s()]+|year:\d{4}|cat:"[^"]+"|cat:[^\s()]+)\s*',
        re.IGNORECASE
    )
    tokens = token_pattern.findall(query)
    tokens = [token.strip() for token in tokens if token.strip()]
    return tokens

def build_filter_function(tokens: List[str]) -> Callable[[Dict[str, Any]], bool]:
    """
    Builds a filter function based on the list of tokens.
    Returns a function that takes a paper dictionary and returns True if it matches the query.
    """
    def parse_expression(index):
        funcs = []
        operators = []
        while index < len(tokens):
            token = tokens[index]
            if token.upper() in ('AND', 'OR'):
                operators.append(token.upper())
                index += 1
            elif token == '(':
                sub_func, index = parse_expression(index + 1)
                funcs.append(sub_func)
            elif token == ')':
                index += 1
                break
            else:
                # Field-specific search
                field_match = re.match(r'(ti|au|year|cat):"([^"]+)"', token, re.IGNORECASE)
                if field_match:
                    field, value = field_match.groups()
                else:
                    # Handle unquoted values
                    field_match = re.match(r'(ti|au|cat):([^\s()]+)', token, re.IGNORECASE)
                    if field_match:
                        field, value = field_match.groups()
                    else:
                        # Handle year without quotes
                        field_match = re.match(r'(year):(\d{4})', token, re.IGNORECASE)
                        if field_match:
                            field, value = field_match.groups()
                        else:
                            print(f"Error: Invalid token '{token}' in query.")
                            sys.exit(1)
                
                # Define the matching function based on field
                if field.lower() == 'ti':
                    func = lambda paper, v=value.lower(): v in paper.get('title', '').lower()
                elif field.lower() == 'au':
                    func = lambda paper, v=value.lower(): any(v == author.lower() for author in paper.get('authors', []))
                elif field.lower() == 'year':
                    func = lambda paper, v=int(value): paper.get('year') == v
                elif field.lower() == 'cat':
                    func = lambda paper, v=value.lower(): v == paper.get('category', '').lower()
                else:
                    print(f"Error: Unsupported field '{field}' in query.")
                    sys.exit(1)
                
                funcs.append(func)
                index += 1
        
        # Combine the functions based on operators
        if not operators:
            return (funcs[0], index)
        
        combined_func = funcs[0]
        for op, func in zip(operators, funcs[1:]):
            if op == 'AND':
                combined_func = (lambda f1=combined_func, f2=func: lambda paper: f1(paper) and f2(paper))()
            elif op == 'OR':
                combined_func = (lambda f1=combined_func, f2=func: lambda paper: f1(paper) or f2(paper))()
        
        return (combined_func, index)
    
    filter_func, _ = parse_expression(0)
    return filter_func

def filter_papers(papers: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    tokens = tokenize_query(query)
    if not tokens:
        print("Error: Empty or invalid query string.")
        sys.exit(1)
    filter_func = build_filter_function(tokens)
    filtered = [paper for paper in papers if filter_func(paper)]
    return filtered

def display_papers(papers: List[Dict[str, Any]]):
    if not papers:
        print("No papers found matching the criteria.\n")
        return
    
    wrap_width = 80
    for i, paper in enumerate(papers, start=1):
        title = paper.get('title', 'No Title')
        authors = ', '.join(paper.get('authors', []))
        year = paper.get('year', 'N/A')
        category = paper.get('category', 'N/A')
        pdf_link = paper.get('pdf_link', 'No PDF Link')
        
        # Define initial and subsequent indents
        initial_indent = f"[{i}]  Title    : "
        subsequent_indent = "                "
        
        # Wrap the title
        wrapped_title = textwrap.fill(title, width=wrap_width - len(initial_indent),
                                      initial_indent=initial_indent,
                                      subsequent_indent=subsequent_indent)
        
        print(wrapped_title)
        print(f"    Authors   : {authors}")
        print(f"    Year      : {year}")
        print(f"    Category  : {category}")
        print(f"    PDF Link  : {pdf_link}\n")
        print("-" * 80)

def save_filtered_papers(papers: List[Dict[str, Any]], output_path: str):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== Filtered arXiv Search Results ===\n\n")
            for i, paper in enumerate(papers, start=1):
                title = paper.get('title', 'No Title')
                authors = ', '.join(paper.get('authors', []))
                year = paper.get('year', 'N/A')
                category = paper.get('category', 'N/A')
                pdf_link = paper.get('pdf_link', 'No PDF Link')
                
                # Define initial and subsequent indents
                initial_indent = f"[{i}]  Title    : "
                subsequent_indent = "                "
                
                # Wrap the title
                wrapped_title = textwrap.fill(title, width=80 - len(initial_indent),
                                              initial_indent=initial_indent,
                                              subsequent_indent=subsequent_indent)
                
                f.write(f"{wrapped_title}\n")
                f.write(f"    Authors   : {authors}\n")
                f.write(f"    Year      : {year}\n")
                f.write(f"    Category  : {category}\n")
                f.write(f"    PDF Link  : {pdf_link}\n\n")
                f.write("-" * 80 + "\n")
        print(f"Filtered results saved to {output_path}\n")
    except OSError as e:
        print(f"Error saving file '{output_path}': {e}\n")

def main():
    args = parse_arguments()
    input_file = args.input_text_file
    query_string = args.query_string
    output_file = args.save_as
    
    # Strip surrounding quotes if present
    query_string = query_string.strip('"').strip("'")
    
    print("=== arXiv Search Results Filter ===\n")
    print(f"Input File     : {input_file}")
    print(f"Query String   : {query_string}")
    if output_file:
        print(f"Output File    : {output_file}")
    print()
    
    papers = load_papers(input_file)
    filtered_papers = filter_papers(papers, query_string)
    
    if output_file:
        save_filtered_papers(filtered_papers, output_file)
    
    display_papers(filtered_papers)

    print("Filtering process completed.")

if __name__ == "__main__":
    main()
