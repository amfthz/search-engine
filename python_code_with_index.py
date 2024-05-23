import mysql.connector
import os
import time
from lxml import etree
from rich.console import Console
from rich.table import Table
from rich.text import Text

# first of all i have to parse the html files.
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        tree = etree.HTML(html_content)
        text_content = '\n'.join(tree.xpath('//text()'))
        return text_content

# creating indexes in my data base amin_db_wit_index 
def create_indexes(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_filename ON wiki(filename);")
    cursor.execute("CREATE FULLTEXT INDEX IF NOT EXISTS idx_content ON wiki(content);")
    connection.commit()

# inserting the parse contents into my database. (amin_db_with_index)
def parse_directory(directory_path, connection):
    cursor = connection.cursor()
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.html', '.htm')):  # Adjusted file filtering condition(amin_db_with_index)
                file_path = os.path.join(root, file)
                filename = os.path.basename(file_path)
                
                # Check if the file has already been inserted (stoping inserting existing files, and add new html and htm files)
                cursor.execute("SELECT COUNT(*) FROM wiki WHERE filename = %s", (filename,))
                result = cursor.fetchone()
                if result[0] > 0:
                    print(f"File '{filename}' already exists in the database. Skipping insertion.")
                    continue
                
                file_size = os.path.getsize(file_path)
                full_path = file_path
                last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
                
                # extract content from HTML file
                content = parse_html_file(file_path)
                
                # insert metadata and content into database
                print(f"Inserting file: {filename}")
                cursor.execute("""
                    INSERT INTO wiki (filename, file_size, full_path, last_modified, content)
                    VALUES (%s, %s, %s, %s, %s)
                """, (filename, file_size, full_path, last_modified, content))
                print(f"File '{filename}' inserted successfully.")
    connection.commit()

# function to parse directory and insert data into the database
def parse_and_insert_data(directory_path):
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Aminfatah12345678@",
        database="amin_db_with_index"
    )

    # Create indexes
    create_indexes(connection)

    # Parse directory and insert data into database
    parse_directory(directory_path, connection)

    # Close the database connection
    connection.close()

# search files in the database
def search_files_in_database(search_query, connection):
    cursor = connection.cursor()
    
    # search for filenames (remember to bold the names next week)
    cursor.execute("SELECT * FROM wiki WHERE filename LIKE %s", (f"%{search_query}%",))
    filename_results = cursor.fetchall()
    
    # search for content using FULLTEXT search (wiki table)
    cursor.execute("SELECT * FROM wiki WHERE MATCH(content) AGAINST (%s IN NATURAL LANGUAGE MODE)", (search_query,))
    content_results = cursor.fetchall()
    
    return filename_results, content_results

#display search results ( watch viedo on youtube to how manage this table and its function and i can insert colors too )
def display_search_results(search_query, filename_results, content_results):
    console = Console()

    #  filename results
    if filename_results:
        console.print(f"\n[bold underline]Search Results for Filenames matching '{search_query}':[/bold underline]")
        filename_table = Table()
        filename_table.add_column("ID", justify="center")
        filename_table.add_column("Filename", justify="left")
        filename_table.add_column("Full Path", justify="left")
        filename_table.add_column("File Size", justify="right")
        filename_table.add_column("Last Modified", justify="center")
        
        for result in filename_results:
            filename_text = highlight_search_query(result[1], search_query)
            filename_table.add_row(
                str(result[0]),
                filename_text,
                result[2],
                f"{result[3]:,}",
                result[4].strftime("%Y-%m-%d %H:%M:%S")
            )

        console.print(filename_table)
    else:
        console.print(f"\nNo filenames matching '{search_query}' found.")

    #  content results
    if content_results:
        console.print(f"\n[bold underline]Search Results for Content matching '{search_query}':[/bold underline]")
        content_table = Table()
        content_table.add_column("ID", justify="center")
        content_table.add_column("Filename", justify="left")
        content_table.add_column("Full Path", justify="left")
        content_table.add_column("File Size", justify="right")
        content_table.add_column("Last Modified", justify="center")
        content_table.add_column("Occurrences in Content", justify="right")
        content_table.add_column("Content Excerpt", justify="left")

        for result in content_results:
            occurrences = result[5].lower().count(search_query.lower())
            content_table.add_row(
                str(result[0]),
                result[1],
                result[2],
                f"{result[3]:,}",
                result[4].strftime("%Y-%m-%d %H:%M:%S"),
                str(occurrences),
                (result[5][:100] + '...') if result[5] else "N/A"
            )

        console.print(content_table)
    else:
        console.print(f"\nNo content matching '{search_query}' found.")

#  highlight search query in text (bolding )
def highlight_search_query(text, query):
    highlighted_text = Text()
    start = 0
    lower_text = text.lower()
    lower_query = query.lower()
    
    while start < len(text):
        idx = lower_text.find(lower_query, start)
        if idx == -1:
            highlighted_text.append(text[start:])
            break
        highlighted_text.append(text[start:idx])
        highlighted_text.append(text[idx:idx + len(query)], style="bold")
        start = idx + len(query)
    
    return highlighted_text

# Main function
def main():
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Aminfatah12345678@",
        database="amin_db_with_index"
    )

    # Search for files by name and content
    while True:
        search_query = input("Enter the search string (or 'exit' to quit): ")
        if search_query.lower() == 'exit':
            break

        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Perform the search
        filename_results, content_results = search_files_in_database(search_query, connection)
        
        # Display results
        display_search_results(search_query, filename_results, content_results)

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()

# Example usage to insert data
directory_path = r'E:\University\DC Project'
parse_and_insert_data(directory_path)
