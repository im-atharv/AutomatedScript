# === Import Libraries ===
import pandas as pd
import argparse
import smtplib
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from email.message import EmailMessage


# === Functions ===
def get_data(query, db_params):
    """Fetch data from Postgres and return as DataFrame"""
    try:
        print("[INFO] Connecting to database...")
        engine = create_engine(
            f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        )
        df = pd.read_sql(query, engine)
        print(f"[SUCCESS] Data fetched successfully, Rows retrieved: {len(df)}")
        return df
    except SQLAlchemyError as e:
        print(f"[ERROR] Database connection or query failed: {e}")
        return pd.DataFrame()  # return empty df on failure


def send_email(sender, receiver, subject, body, file_path, smtp_params):
    """Send email with attachment (simplified using EmailMessage)"""
    try:
        print("[INFO] Preparing email...")
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = sender, receiver, subject
        msg.add_alternative(body, subtype="html")

        # Attach file
        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file_path)
            )

        print("[INFO] Connecting to SMTP server...")
        with smtplib.SMTP(smtp_params["host"], smtp_params["port"]) as server:
            server.starttls()
            print("[INFO] Logging in to SMTP server...")
            server.login(smtp_params["user"], smtp_params["password"])
            server.send_message(msg)
            print("[SUCCESS] Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("[ERROR] SMTP authentication failed. Please check your email/password.")
    except smtplib.SMTPConnectError:
        print("[ERROR] Failed to connect to the SMTP server.")
    except FileNotFoundError:
        print(f"[ERROR] Attachment file not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


def build_html_body(business_date, row_count):
    """Return a styled HTML body for the email"""
    return f"""
    <html>
    <body style="font-family:Arial, sans-serif; background:#f9f9f9; padding:20px; color:#333;">
        <div style="background:#fff; border-radius:8px; padding:20px; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            <h2 style="color:#2c3e50;">📊 Sales Report - {business_date}</h2>
            <p>Hello Team,</p>
            <p>Please find attached the sales report for <b>{business_date}</b>.</p>
            <p>The report contains <b>{row_count} records</b>.</p>
            <p>Regards,<br>Automated Reporting System</p>
            <hr>
            <p style="font-size:12px; color:#777;">This is an auto-generated email. Please do not reply.</p>
        </div>
    </body>
    </html>
    """


# === Main ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--business_date", required=True)
    parser.add_argument("-s", "--sender_email", required=True)
    parser.add_argument("-r", "--receiver_email", required=True)
    parser.add_argument("-sub", "--subject", required=True)
    args = parser.parse_args()

    print("[INFO] Starting report generation...")

    # Load environment variables
    load_dotenv()

    # Database + SMTP configs
    db_params = {
        "dbname": os.getenv("DB_NAME"), "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"), "host": os.getenv("DB_HOST"), "port": os.getenv("DB_PORT")
    }

    smtp_params = {
        "host": os.getenv("SMTP_HOST"), "port": int(os.getenv("SMTP_PORT")),
        "user": os.getenv("SMTP_USER"), "password": os.getenv("SMTP_PASSWORD")
    }

    # Query + fetch
    query = f"SELECT * FROM sales_data WHERE transaction_date = '{args.business_date}'"
    df = get_data(query, db_params)
    if df.empty:
        print("[WARNING] No data found for given business_date!")
        return

    # Save to Excel
    file = f"sales_report_{args.business_date}.xlsx"
    try:
        df.to_excel(file, index=False)
        print(f"[SUCCESS] Report saved to {file}")
    except Exception as e:
        print(f"[ERROR] Failed to save Excel report: {e}")
        return

    # Build the HTML body
    html = build_html_body(args.business_date, len(df))

    # Send email
    send_email(args.sender_email, args.receiver_email, args.subject, html, file, smtp_params)

    print("[INFO] Script completed.")


if __name__ == "__main__":
    main()
