# Automated Database Reporting and Emailing Script

A Python script that connects to a PostgreSQL database, executes a SQL query based on a given business date, saves the results to an Excel file, and emails the file as an attachment with a styled HTML body.

---

## Features

-   **Database Connection**: Securely connects to a PostgreSQL database using credentials from environment variables.
-   **Dynamic Queries**: Fetches data for a specific business date provided as a command-line argument.
-   **Excel Export**: Saves the retrieved data into a neatly formatted Excel file using `pandas`.
-   **HTML Email**: Sends an email with a styled HTML body summarizing the report.
-   **Secure Credential Management**: Uses a `.env` file to manage sensitive information like database and email credentials.
-   **Command-Line Interface**: Utilizes `argparse` to accept parameters like business date, sender/receiver emails, and subject line, making it easy to automate and schedule.
-   **Error Handling**: Includes robust error handling for database connections, file operations, and email sending.

---

## Prerequisites

Before you begin, ensure you have the following installed:
-   Python 3.7+
-   `pip` (Python package installer)

---

## Setup & Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/im-atharv/AutomatedScript.git
    cd AutomatedScript
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    In the same directory as the script, create a file named `.env` and add your database and SMTP credentials. This file keeps your sensitive information separate from the code.

    ```env
    # Database Credentials
    DB_HOST="your_db_host"
    DB_PORT="5432"
    DB_NAME="your_db_name"
    DB_USER="your_db_user"
    DB_PASSWORD="your_db_password"

    # SMTP Server Credentials
    SMTP_HOST="smtp.example.com"
    SMTP_PORT="587"
    SMTP_USER="your_email@example.com"
    SMTP_PASSWORD="your_email_password"
    ```
    **Note:** For Gmail, you might need to use an "App Password" instead of your regular password if you have 2-Factor Authentication enabled.

---

## Usage

Run the script from your terminal and provide the required arguments.

**Syntax:**
```bash
python script.py -d BUSINESS_DATE -s SENDER_EMAIL -r RECEIVER_EMAIL -sub "SUBJECT"
```
**Example**
```bash
python main.py -d "2023-10-26" -s "sender@example.com" -r "receiver@example.com" -sub "Daily Sales Report for 2023-10-26"
```
