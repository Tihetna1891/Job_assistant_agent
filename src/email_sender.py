# import smtplib
# import os
# import time
# import logging
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from dotenv import load_dotenv

# # Load the .env file using a relative path
# load_dotenv(os.path.join(os.path.dirname(__file__), "..", "env", "email.env"))

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def send_job_application_email(to_email, job_title, company, applicant_name, cv_path, cover_letter_path=None):
#     try:
#         # Check if the CV file exists
#         if not os.path.exists(cv_path):
#             logging.error(f"CV file not found at {cv_path}")
#             return False
        
#         # Check if the cover letter file exists (if provided)
#         if cover_letter_path and not os.path.exists(cover_letter_path):
#             logging.error(f"Cover letter file not found at {cover_letter_path}")
#             return False

#         # Get email credentials from environment variables
#         email_user = os.getenv('EMAIL_USER')
#         email_password = os.getenv('EMAIL_PASSWORD')
#         email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
#         email_port = int(os.getenv('EMAIL_PORT', 587))

#         if not email_user or not email_password:
#             logging.error("Email credentials are not set properly in environment variables.")
#             return False

#         # Define the email subject and body
#         subject = f"Application for {job_title} Position at {company}"
#         body = f"""
#         Dear Hiring Manager,

#         I hope this email finds you well. I am excited to apply for the {job_title} position at {company}. 
#         With my experience and skills, I am confident in my ability to contribute effectively to your team.

#         Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
#         to discuss how my background aligns with the role. I look forward to your response.

#         Best regards,  
#         {applicant_name}
#         """

#         # Log the start of the email sending process
#         logging.info(f"Preparing to send email to {to_email}...")

#         # Create message object
#         msg = MIMEMultipart()
#         msg['From'] = email_user
#         msg['To'] = ", ".join(to_email) if isinstance(to_email, list) else to_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         # Attach CV
#         logging.info(f"Attaching CV from {cv_path}")
#         with open(cv_path, 'rb') as cv_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(cv_file.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cv_path)}')
#             msg.attach(part)

#         # Attach cover letter if it exists
#         if cover_letter_path:
#             logging.info(f"Attaching cover letter from {cover_letter_path}")
#             with open(cover_letter_path, 'rb') as cover_letter_file:
#                 part = MIMEBase('application', 'octet-stream')
#                 part.set_payload(cover_letter_file.read())
#                 encoders.encode_base64(part)
#                 part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cover_letter_path)}')
#                 msg.attach(part)

#         retries = 3  # Number of retry attempts
#         for attempt in range(retries):
#             try:
#                 logging.info(f"Attempting to send email to {to_email}...")

#                 with smtplib.SMTP(email_host, email_port) as server:
#                     server.set_debuglevel(1)  # Enable debug mode
#                     server.starttls()
#                     logging.info("Starting TLS encryption...")

#                     # Attempt to log in
#                     server.login(email_user, email_password)
#                     logging.info("Logged in successfully...")

#                     # Send the email
#                     server.sendmail(email_user, msg['To'].split(", "), msg.as_string())
#                     logging.info(f"Application email sent successfully to {to_email}")
#                     return True  # Return True on success
#             except Exception as e:
#                 logging.error(f"Error sending email to {to_email}: {str(e)}", exc_info=True)
#                 if attempt < retries - 1:
#                     logging.info(f"Retrying... (Attempt {attempt + 2} of {retries})")
#                     time.sleep(5)  # Wait 5 seconds before retrying
#                 else:
#                     logging.error("All retry attempts failed.")
#                     return False

#     except Exception as e:
#         logging.error(f"An error occurred while preparing to send the email: {str(e)}", exc_info=True)
#         return False

# # Example usage for sending an application email
# if __name__ == "__main__":
#     logging.info("Sending email...")
#     success = send_job_application_email(
#         to_email=os.getenv('EMAIL_USER'),
#         job_title="Data Scientist",
#         company="TechCorp",
#         applicant_name="John Doe",
#         cv_path="path_to_uploaded_cv.pdf"
#     )
#     if success:
#         logging.info("Email sent successfully.")
#     else:
#         logging.info("Email sending failed.")

import smtplib
import os
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def send_job_application_email(recipient_email, subject, body, cv_path, cover_letter_path):
#     try:
#         # Check if the CV file exists
#         if not os.path.exists(cv_path):
#             logging.error(f"CV file not found at {cv_path}")
#             return False
        
#         if hasattr(st, "secrets") and "general" in st.secrets:
#             email_user = st.secrets["general"]["EMAIL_ADDRESS"]
#             email_password = st.secrets["general"]["EMAIL_PASSWORD"]
#             email_host = st.secrets["general"]["EMAIL_HOST"]
#             email_port = st.secrets["general"]["EMAIL_PORT"]
#         else:
#             raise ValueError("Email credentials not found in secrets.")

#         if not email_user or not email_password:
#             logging.error("Email credentials are not set properly in secrets.")
#             return False

#         # Create message object
#         msg = MIMEMultipart()
#         msg['From'] = email_user
#         msg['To'] = ", ".join(recipient_email) if isinstance(recipient_email, list) else recipient_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         # Attach CV
#         logging.info(f"Attaching CV from {cv_path}")
#         with open(cv_path, 'rb') as cv_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(cv_file.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cv_path)}')
#             msg.attach(part)

#         # Attach cover letter
#         logging.info(f"Attaching cover letter from {cover_letter_path}")
#         with open(cover_letter_path, 'rb') as cover_letter_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(cover_letter_file.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cover_letter_path)}')
#             msg.attach(part)

#         retries = 3
#         for attempt in range(retries):
#             try:
#                 logging.info(f"Attempting to send email to {recipient_email}...")
#                 with smtplib.SMTP(email_host, email_port) as server:
#                     server.set_debuglevel(1)
#                     server.starttls()
#                     logging.info("Starting TLS encryption...")
#                     server.login(email_user, email_password)
#                     logging.info("Logged in successfully...")
#                     server.sendmail(email_user, msg['To'].split(", "), msg.as_string())
#                     logging.info(f"Application email sent successfully to {recipient_email}")
#                     return True
#             except Exception as e:
#                 logging.error(f"Error sending email to {recipient_email}: {str(e)}", exc_info=True)
#                 if attempt < retries - 1:
#                     logging.info(f"Retrying... (Attempt {attempt + 2} of {retries})")
#                     time.sleep(5)
#                 else:
#                     logging.error("All retry attempts failed.")
#                     return False

#     except Exception as e:
#         logging.error(f"An error occurred while preparing to send the email: {str(e)}", exc_info=True)
#         return False


logging.basicConfig(level=logging.INFO)

def send_job_application_email(to_email, subject, body, cv_file=None, cover_letter_text=None):
    """
    Send job application email with attachments (handles both file paths and file objects)
    
    Args:
        to_email (str/list): Recipient email(s)
        subject (str): Email subject
        body (str): Email body content
        cv_file (file object/str): Either file object or path to CV
        cover_letter_text (str): Content of cover letter
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = to_email if isinstance(to_email, str) else ", ".join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach CV
        if cv_file:
            if hasattr(cv_file, 'read'):  # File object
                cv_data = cv_file.read()
                filename = getattr(cv_file, 'name', 'CV.pdf')
            else:  # Assume it's a file path
                with open(cv_file, 'rb') as f:
                    cv_data = f.read()
                filename = os.path.basename(cv_file)
            
            part = MIMEApplication(cv_data, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

        # Attach cover letter
        if cover_letter_text:
            part = MIMEText(cover_letter_text, 'plain')
            part['Content-Disposition'] = 'attachment; filename="Cover_Letter.txt"'
            msg.attach(part)

        # Send email
        with smtplib.SMTP(os.getenv('EMAIL_HOST', 'smtp.gmail.com'), 
                         int(os.getenv('EMAIL_PORT', 587))) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
            logging.info(f"Email sent successfully to {to_email}")
            return True

    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False
# def send_job_application_email(recipient_email, subject, body, cv_path, cover_letter_path, sender_email=None, sender_password=None):
#     try:
#         # Check if the CV file exists
#         if not os.path.exists(cv_path):
#             logging.error(f"CV file not found at {cv_path}")
#             return False
        
#         # Check if the cover letter file exists
#         if not os.path.exists(cover_letter_path):
#             logging.error(f"Cover letter file not found at {cover_letter_path}")
#             return False

#         # Load email host and port from secrets (as defaults)
#         if hasattr(st, "secrets") and "general" in st.secrets:
#             email_host = st.secrets["general"]["EMAIL_HOST"]
#             email_port = st.secrets["general"]["EMAIL_PORT"]
#         else:
#             logging.error("Email host/port not found in secrets.")
#             raise ValueError("Email host/port not found in secrets.")

#         # Validate sender email and password
#         if not sender_email or not sender_password:
#             logging.error("Sender email or password not provided.")
#             return False

#         email_user = sender_email
#         email_password = sender_password

#         logging.info(f"Email settings: user={email_user}, host={email_host}, port={email_port}")
        
#         # Create message object
#         msg = MIMEMultipart()
#         msg['From'] = email_user
#         msg['To'] = ", ".join(recipient_email) if isinstance(recipient_email, list) else recipient_email
#         logging.info(f"Sending email from {msg['From']} to {msg['To']}")
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         # Attach CV
#         logging.info(f"Attaching CV from {cv_path}")
#         with open(cv_path, 'rb') as cv_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(cv_file.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cv_path)}')
#             msg.attach(part)

#         # Attach cover letter
#         logging.info(f"Attaching cover letter from {cover_letter_path}")
#         with open(cover_letter_path, 'rb') as cover_letter_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(cover_letter_file.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cover_letter_path)}')
#             msg.attach(part)

#         retries = 3
#         for attempt in range(retries):
#             try:
#                 logging.info(f"Attempting to send email to {recipient_email}...")
#                 with smtplib.SMTP(email_host, email_port) as server:
#                     server.set_debuglevel(1)
#                     server.starttls()
#                     logging.info("Starting TLS encryption...")
#                     server.login(email_user, email_password)
#                     logging.info("Logged in successfully...")
#                     server.sendmail(email_user, msg['To'].split(", "), msg.as_string())
#                     logging.info(f"Application email sent successfully to {recipient_email}")
#                     return True
#             except smtplib.SMTPAuthenticationError as e:
#                 logging.error(f"SMTP Authentication failed: {str(e)}")
#                 return False
#             except smtplib.SMTPException as e:
#                 logging.error(f"SMTP error: {str(e)}")
#                 if attempt < retries - 1:
#                     logging.info(f"Retrying... (Attempt {attempt + 2} of {retries})")
#                     time.sleep(5)
#                 else:
#                     logging.error("All retry attempts failed.")
#                     return False
#             except Exception as e:
#                 logging.error(f"Unexpected error sending email: {str(e)}", exc_info=True)
#                 if attempt < retries - 1:
#                     logging.info(f"Retrying... (Attempt {attempt + 2} of {retries})")
#                     time.sleep(5)
#                 else:
#                     logging.error("All retry attempts failed.")
#                     return False

#     except Exception as e:
#         logging.error(f"An error occurred while preparing to send the email: {str(e)}", exc_info=True)
#         return False

if __name__ == "__main__":
    logging.info("Sending email...")
    send_job_application_email(
        to_email=st.secrets["general"]["EMAIL_ADDRESS"],
        subject="Test Application",
        body="This is a test email.",
        cv_path="path_to_cv.pdf",
        cover_letter_path="path_to_cover_letter.txt"
    )
    logging.info("Email function executed.")