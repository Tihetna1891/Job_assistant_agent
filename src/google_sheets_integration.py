import os
import time
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import logging
import traceback
import streamlit as st
from dotenv import load_dotenv

# Load the .env file using a relative path
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "env", "google_sheets.env"))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Google Sheets authentication function
def authenticate_gsheet(json_credentials_file):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(json_credentials_file, scopes=scopes)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return gspread.authorize(creds)
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return None

# Function to update job application status in Google Sheets
def update_job_status_in_sheet(json_credentials_file, spreadsheet_id, sheet_name="Sheet1", job_data={}):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            return False

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        required_fields = ["job_title", "company", "status"]
        if not all(field in job_data for field in required_fields):
            logging.error("Missing required fields in job_data.")
            return False

        job_row = [
            job_data.get("job_title", ""), job_data.get("company", ""), job_data.get("location", ""),
            job_data.get("created", ""), job_data.get("salary_min", ""), job_data.get("salary_max", ""),
            job_data.get("apply_link", ""), job_data.get("status", ""), job_data.get("application_date", ""),
            job_data.get("interview_date", ""), job_data.get("notes", "")
        ]

        retries = 3
        for attempt in range(retries):
            try:
                sheet.append_row(job_row)
                logging.info(f"Job data for {job_data['job_title']} added to Google Sheets.")
                return True
            except gspread.exceptions.APIError as api_err:
                logging.error(f"API Error (attempt {attempt+1}/{retries}): {api_err}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logging.error(f"Unexpected error updating Google Sheets: {e}")
                print(traceback.format_exc())
                return False

    except Exception as e:
        logging.error(f"Error in update_job_status_in_sheet: {e}")
        print(traceback.format_exc())

    return False

# Function to update a specific row in Google Sheets
def update_row_in_sheet(json_credentials_file, spreadsheet_id, row_index, job_data, sheet_name="Sheet1"):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            return False

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        required_fields = ["job_title", "company", "status"]
        if not all(field in job_data for field in required_fields):
            logging.error("Missing required fields in job_data for update.")
            return False

        job_row = [
            job_data.get("job_title", ""), job_data.get("company", ""), job_data.get("location", ""),
            job_data.get("created", ""), job_data.get("salary_min", ""), job_data.get("salary_max", ""),
            job_data.get("apply_link", ""), job_data.get("status", ""), job_data.get("application_date", ""),
            job_data.get("interview_date", ""), job_data.get("notes", "")
        ]

        retries = 3
        for attempt in range(retries):
            try:
                # Update the specific row (row_index is 1-based in gspread)
                sheet.update(f"A{row_index}:{chr(ord('A') + len(job_row) - 1)}{row_index}", [job_row])
                logging.info(f"Updated row {row_index} for {job_data['job_title']} in Google Sheets.")
                return True
            except gspread.exceptions.APIError as api_err:
                logging.error(f"API Error (attempt {attempt+1}/{retries}): {api_err}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logging.error(f"Unexpected error updating row in Google Sheets: {e}")
                print(traceback.format_exc())
                return False

    except Exception as e:
        logging.error(f"Error in update_row_in_sheet: {e}")
        print(traceback.format_exc())

    return False

# Function to delete a specific row in Google Sheets
def delete_row_from_sheet(json_credentials_file, spreadsheet_id, row_index, sheet_name="Sheet1"):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            return False

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        retries = 3
        for attempt in range(retries):
            try:
                sheet.delete_rows(row_index)
                logging.info(f"Deleted row {row_index} from Google Sheets.")
                return True
            except gspread.exceptions.APIError as api_err:
                logging.error(f"API Error (attempt {attempt+1}/{retries}): {api_err}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logging.error(f"Unexpected error deleting row from Google Sheets: {e}")
                print(traceback.format_exc())
                return False

    except Exception as e:
        logging.error(f"Error in delete_row_from_sheet: {e}")
        print(traceback.format_exc())

    return False

# Function to retrieve job application statuses from Google Sheets
def get_job_status_from_sheet(json_credentials_file, spreadsheet_id, sheet_name="Sheet1"):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            logging.error("Failed to authenticate with Google Sheets API. Check credentials file.")
            st.error("Failed to authenticate with Google Sheets API. Check credentials file.")
            return None

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        # Define expected headers in the correct order and names
        expected_headers = [
            "job_title", "company", "location", "created", "salary_min", "salary_max",
            "apply_link", "status", "application_date", "interview_date", "notes"
        ]

        # Check if the sheet has data
        all_values = sheet.get_all_values()
        if not all_values or len(all_values) < 2:  # At least header row + 1 data row
            logging.warning("Google Sheet is empty or has no data rows.")
            return []

        # Check if headers match
        actual_headers = all_values[0]
        if actual_headers != expected_headers:
            logging.error(f"Header mismatch. Expected: {expected_headers}, Got: {actual_headers}")
            st.error(f"Header mismatch in Google Sheet. Expected: {expected_headers}, Got: {actual_headers}")
            return None

        job_records = sheet.get_all_records(expected_headers=expected_headers)

        logging.info(f"Retrieved {len(job_records)} job application records.")
        return job_records

    except gspread.exceptions.WorksheetNotFound:
        logging.error(f"Worksheet '{sheet_name}' not found in Google Sheet with ID {spreadsheet_id}.")
        st.error(f"Worksheet '{sheet_name}' not found in Google Sheet. Please ensure the sheet name is correct (e.g., 'Sheet1').")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Google Sheet with ID {spreadsheet_id} not found or inaccessible.")
        st.error(f"Google Sheet with ID {spreadsheet_id} not found or inaccessible. Check the spreadsheet ID and permissions.")
        return None
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Google Sheets API Error: {api_err}")
        st.error(f"Google Sheets API Error: {api_err}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error retrieving job status: {e}")
        st.error(f"Unexpected error retrieving job status: {e}")
        return None