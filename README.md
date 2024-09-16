# **Site Parser**

This is a test parser for extracting newses and saving them to a CSV file using the library **Selectolax**.

## **Features**
- **Choosing which page to which page**:  
  You can choose which page to which data will be collected in the `.env` file.

- **Asynchronous translation into Russian**:  
  The parser is also capable of synchronously translating all incoming text with <p> and <li> tags.

- **Further improvements**:  
  In the future, parsing options for other sites will be added, as well as the ability to parse from many sites at the same time.

## **Setup**

### **Requirements**
- `httpx`
- `selectolax`
- `deep-translator`

### **Installation**

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Site_parser.git
    cd telegram-parser
    ```

2. **Install Poetry**:
    ```bash
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    poetry --version
    ```

3. **Install Project Dependencies**:
    ```bash
    poetry install
    ```

4. **Set Up Environment Variables**:
    The project uses environment variables to store information like start/end page. You need to create a `.env` file at the root of the project directory.

    - **4.1. Create a `.env` file**:
        ```bash
        touch .env
        ```

    - **4.2. Add the page numbers you want to parse, as well as the information you need (example below)**:
        ```plaintext
        START_PAGE=1
        END_PAGE=3
        NEWS_CATEGORY=economy-trade
        ```

5. **Running the Code**:

    - **5.1. Activate the virtual environment created by Poetry**:
        ```bash
        poetry shell
        ```

    - **5.2. Run the script to start fetching messages from Telegram**:
        ```bash
        poetry run python src/main.py
        ```

6. **Output**:
    - **6.1 Example output**:
        ```bash
        The data from the page 1 is collected
        The data from the page 2 is collected
        ```
    After running the script, the extracted messages will be saved in a CSV file located at `data/data/results.csv`. The file will include details like title, news date, news href, news short text, news main text, country and category.
