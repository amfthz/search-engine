seyed amin fattahzadeh 
# HTML File Parser and Database Search Tool

## Overview

This project is a Python tool to:
1. Parse HTML files and extract their text content.
2. Store the content in a MySQL database.
3. Allow users to search the database for files by their name or content.

## Setup:

### Requirements

- Python 3.6 or higher
- MySQL Server
- Python packages: `mysql-connector-python`, `lxml`, `rich`

### Installation

1. **Install Python Packages**
   ```bash
   pip install mysql-connector-python lxml rich
   ```

2. **Set Up MySQL Database**
   - Create a new database named `amin_db_with_index`.
   - Create a table named `wiki`:
     ```sql
     CREATE TABLE wiki (
         id INT AUTO_INCREMENT PRIMARY KEY,
         filename VARCHAR(255),
         file_size BIGINT,
         full_path TEXT,
         last_modified DATETIME,
         content LONGTEXT
     );
     ```

3. **Update Database Configuration**
   Update the database connection details in the script if needed:
   ```python
   connection = mysql.connector.connect(
       host="127.0.0.1",
       user="root",
       password="my password",
       database="amin_db_with_index"
   )
   ```

## Usage

### Insert Data into Database

To parse HTML files from a directory and insert them into the database:
```python
directory_path = r'D:\DCRB with index'
parse_and_insert_data(directory_path)
```

### Run the Search Tool

Start the search tool by running the script:
```bash
python.py
```

### Search Interface

- Enter a search term to find files by their name or content.
- Type `exit` to quit the tool.

## Functions

- **parse_html_file(file_path)**: Extracts text from an HTML file.
- **create_indexes(connection)**: Creates indexes in the database for faster search.
- **parse_directory(directory_path, connection)**: Parses HTML files in a directory and inserts them into the database.
- **parse_and_insert_data(directory_path)**: Combines parsing and insertion process.
- **search_files_in_database(search_query, connection)**: Searches the database for files matching the search query.
- **display_search_results(search_query, filename_results, content_results)**: Shows search results in a table.
- **highlight_search_query(text, query)**: Highlights search terms in the text.


## Contact

For any questions or issues, contact [seyedamin.fattahzadeh01@universitadipavia.it].
or you cna ask me on my linkedin : amin-fattahzadeh
