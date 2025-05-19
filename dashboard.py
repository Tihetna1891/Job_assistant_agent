# import streamlit as st
# import pandas as pd
# import os
# import time
# from datetime import datetime
# from dotenv import load_dotenv
# import logging
# import shutil

# # Import functions from your existing files
# from src.google_sheets_integration import authenticate_gsheet, update_job_status_in_sheet, get_job_status_from_sheet, update_row_in_sheet, delete_row_from_sheet
# from src.cover_letter_generator import generate_cover_letter, extract_experience_from_cv, extract_name_and_contact_from_cv, save_to_files
# from src.email_sender import send_job_application_email
# from src.job_scraper import JobScraper
# from src.nlp_processing import extract_skills_from_description

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Load environment variables using a relative path
# load_dotenv(os.path.join(os.path.dirname(__file__), "env", "app.env"))

# # Create a temp directory for storing uploaded files and generated cover letters
# TEMP_DIR = "temp"
# if not os.path.exists(TEMP_DIR):
#     os.makedirs(TEMP_DIR)

# # --- Custom CSS for Styling ---
# def load_css():
#     st.markdown("""
#     <style>
#         .main {
#             background-color: #f8f9fa;
#         }
#         .stButton>button {
#             background-color: #4a90e2;
#             color: white;
#             border-radius: 8px;
#             padding: 8px 16px;
#             border: none;
#             font-weight: 500;
#         }
#         .stButton>button:hover {
#             background-color: #357abd;
#             color: white;
#         }
#         .stTextInput>div>div>input, .stTextArea>div>div>textarea {
#             border-radius: 8px;
#             padding: 8px;
#         }
#         .stSelectbox>div>div>div {
#             border-radius: 8px;
#             padding: 4px;
#         }
#         .stDateInput>div>div>input {
#             border-radius: 8px;
#             padding: 8px;
#         }
#         .stNumberInput>div>div>input {
#             border-radius: 8px;
#             padding: 8px;
#         }
#         .header {
#             color: #2c3e50;
#             font-weight: 700;
#         }
#         .sidebar .sidebar-content {
#             background-color: #2c3e50;
#             color: white;
#         }
#         .sidebar .sidebar-content .stRadio>div {
#             color: white;
#         }
#         .success-box {
#             background-color: #d4edda;
#             color: #155724;
#             padding: 16px;
#             border-radius: 8px;
#             margin: 16px 0;
#         }
#         .warning-box {
#             background-color: #fff3cd;
#             color: #856404;
#             padding: 16px;
#             border-radius: 8px;
#             margin: 16px 0;
#         }
#         .error-box {
#             background-color: #f8d7da;
#             color: #721c24;
#             padding: 16px;
#             border-radius: 8px;
#             margin: 16px 0;
#         }
#         .job-card {
#             background-color: white;
#             border-radius: 8px;
#             padding: 16px;
#             margin-bottom: 16px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         }
#         .job-card h3 {
#             color: #2c3e50;
#             margin-top: 0;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize session state variables
# if 'cover_letter_path' not in st.session_state:
#     st.session_state.cover_letter_path = None
# if 'cv_path' not in st.session_state:
#     st.session_state.cv_path = None
# if 'selected_job' not in st.session_state:
#     st.session_state.selected_job = {}
# if 'applicant_name' not in st.session_state:
#     st.session_state.applicant_name = "Applicant"
# if 'job_results' not in st.session_state:
#     st.session_state.job_results = None
# if 'applications' not in st.session_state:
#     st.session_state.applications = None

# # Function to clean up temporary files
# def cleanup_temp_files():
#     if os.path.exists(TEMP_DIR):
#         for filename in os.listdir(TEMP_DIR):
#             file_path = os.path.join(TEMP_DIR, filename)
#             try:
#                 if os.path.isfile(file_path):
#                     os.unlink(file_path)
#             except Exception as e:
#                 logging.error(f"Error cleaning up temp file {file_path}: {e}")

# # --- Streamlit UI Components ---
# def main():
#     st.set_page_config(
#         page_title="AI Job Assistant",
#         layout="wide",
#         page_icon="💼"
#     )
#     load_css()
    
#     # Sidebar navigation
#     st.sidebar.title("💼 AI Job Assistant")
#     st.sidebar.markdown("---")
#     page = st.sidebar.radio(
#         "Navigation",
#         ["🏠 Dashboard", "🔍 Job Search", "📝 Cover Letter", "✉️ Email Application", "📊 Application Tracker"],
#         label_visibility="collapsed"
#     )
    
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### Settings")
#     json_credentials_file = st.sidebar.text_input(
#         "Google Sheets Credentials Path",
#         "credentials.json",
#         help="Path to your Google Sheets service account JSON file"
#     )
#     spreadsheet_id = st.sidebar.text_input(
#         "Google Sheet ID",
#         help="ID of your Google Sheet for tracking applications"
#     )
    
#     if page == "🏠 Dashboard":
#         render_dashboard()
#     elif page == "🔍 Job Search":
#         render_job_search()
#     elif page == "📝 Cover Letter":
#         render_cover_letter_generator()
#     elif page == "✉️ Email Application":
#         render_email_application()
#     elif page == "📊 Application Tracker":
#         render_application_tracker(json_credentials_file, spreadsheet_id)

# def render_dashboard():
#     st.title("AI Job Assistant Dashboard")
#     st.markdown("""
#     Welcome to your AI-powered job application assistant! This tool helps you:
    
#     - 🔍 Search for relevant job opportunities
#     - 📝 Generate personalized cover letters
#     - ✉️ Send professional application emails
#     - 📊 Track your application progress
    
#     Get started by selecting a page from the sidebar.
#     """)
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Jobs Found", "25", "+5 from last week")
#     with col2:
#         st.metric("Applications Sent", "8", "3 pending")
#     with col3:
#         st.metric("Interview Rate", "25%", "2 of 8")
    
#     st.markdown("---")
#     st.subheader("Recent Activity")
#     st.write("Your recent job application activity will appear here.")

# def render_job_search():
#     st.title("Job Search")
#     st.markdown("Find your next career opportunity using our AI-powered job search.")
    
#     with st.expander("🔍 Search Filters", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             job_titles = st.text_input(
#                 "Job Titles (comma separated)",
#                 "Data Scientist, Machine Learning Engineer",
#                 help="Enter multiple job titles separated by commas"
#             )
#         with col2:
#             location = st.text_input("Location", "London")
    
#     if st.button("Search Jobs", key="search_jobs"):
#         with st.spinner("🔍 Searching for jobs..."):
#             job_list = [title.strip() for title in job_titles.split(",")]
            
#             try:
#                 scraper = JobScraper(job_titles=job_list, location=location)
#                 scraper.scrape_jobs()
#                 jobs = scraper.get_saved_jobs()
                
#                 if not jobs.empty:
#                     st.session_state.job_results = jobs
#                     st.success(f"🎉 Found {len(jobs)} jobs!")
                    
#                     # Display jobs in cards
#                     for idx, job in jobs.iterrows():
#                         with st.container():
#                             st.markdown(f"""
#                             <div class="job-card">
#                                 <h3>{job['job_title']}</h3>
#                                 <p><strong>Company:</strong> {job['company']}</p>
#                                 <p><strong>Location:</strong> {job['location']}</p>
#                                 <p><strong>Salary:</strong> £{job['salary_min']} - £{job['salary_max']}</p>
#                                 <a href="{job['apply_link']}" target="_blank">View Job</a>
#                             </div>
#                             """, unsafe_allow_html=True)
#                 else:
#                     st.warning("No jobs found. Try different search terms.")
#             except Exception as e:
#                 st.error(f"Error searching for jobs: {str(e)}")

# def render_cover_letter_generator():
#     st.title("Cover Letter Generator")
#     st.markdown("Create a personalized cover letter for your job application.")
    
#     if 'job_results' in st.session_state and not st.session_state.job_results.empty:
#         job_list = st.session_state.job_results[['job_title', 'company']].to_dict('records')
#         job_options = {f"{job['job_title']} at {job['company']}": idx for idx, job in enumerate(job_list)}
#         selected_job_key = st.selectbox(
#             "Select a job to apply for",
#             options=list(job_options.keys()),
#             help="Select a job from your previous search results"
#         )
#         selected_job_idx = job_options[selected_job_key]
#         selected_job = st.session_state.job_results.iloc[selected_job_idx]
#         st.session_state.selected_job = selected_job
        
#         with st.expander("📄 Job Details", expanded=True):
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown(f"**Job Title:** {selected_job['job_title']}")
#                 st.markdown(f"**Company:** {selected_job['company']}")
#                 st.markdown(f"**Location:** {selected_job['location']}")
#             with col2:
#                 st.markdown(f"**Salary Range:** £{selected_job['salary_min']} - £{selected_job['salary_max']}")
#                 st.markdown(f"**Posted:** {selected_job['created']}")
#                 st.markdown(f"[Apply Here]({selected_job['apply_link']})")
            
#             st.markdown("**Description:**")
#             st.write(selected_job['description'][:500] + "...")
#     else:
#         st.warning("⚠️ No job results available. Please search for jobs first.")
#         selected_job = None
    
#     if selected_job is not None:
#         st.subheader("Upload Your CV")
#         cv_file = st.file_uploader(
#             "Choose your CV file (PDF or DOCX)",
#             type=['pdf', 'docx'],
#             help="Upload your CV to personalize the cover letter",
#             key="cv_uploader"
#         )
        
#         if cv_file:
#             # Save the uploaded file to the temp directory
#             cv_filename = f"cv_{int(time.time())}.{cv_file.name.split('.')[-1]}"
#             temp_cv_path = os.path.join(TEMP_DIR, cv_filename)
#             with open(temp_cv_path, "wb") as f:
#                 f.write(cv_file.getbuffer())
            
#             st.session_state.cv_path = temp_cv_path
#             st.success("✅ CV uploaded successfully!")
            
#             if st.button("Generate Cover Letter", key="generate_cover_letter"):
#                 with st.spinner("✨ Generating your personalized cover letter..."):
#                     try:
#                         # Generate cover letter
#                         cover_letter = generate_cover_letter(
#                             selected_job['job_title'],
#                             selected_job['company'],
#                             selected_job['description'],
#                             temp_cv_path
#                         )
                        
#                         # Extract name from CV for saving files
#                         name, _ = extract_name_and_contact_from_cv(temp_cv_path)
#                         st.session_state.applicant_name = name
                        
#                         # Save cover letter to a temporary file
#                         cover_letter_filename = f"cover_letter_{int(time.time())}.txt"
#                         cover_letter_path = os.path.join(TEMP_DIR, cover_letter_filename)
#                         with open(cover_letter_path, "w") as f:
#                             f.write(cover_letter)
                        
#                         st.session_state.cover_letter_path = cover_letter_path
                        
#                         st.subheader("Your Custom Cover Letter")
#                         st.text_area(
#                             "Cover Letter Content",
#                             cover_letter,
#                             height=400,
#                             label_visibility="collapsed"
#                         )
#                         st.success("📄 Cover letter generated and saved successfully!")
#                     except Exception as e:
#                         st.error(f"Error generating cover letter: {str(e)}")

# def render_email_application():
#     st.title("Email Application")
#     st.markdown("Send your job application with cover letter and CV attached.")
    
#     required_keys = ['cover_letter_path', 'cv_path', 'selected_job']
#     if not all(key in st.session_state for key in required_keys):
#         st.warning("""
#         ⚠️ Please complete these steps first:
#         1. Search for jobs on the Job Search page
#         2. Generate a cover letter on the Cover Letter page
#         """)
#         return
    
#     with st.expander("✉️ Email Details", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             recipient_email = st.text_input(
#                 "Recipient Email",
#                 help="The hiring manager's email address"
#             )
#         with col2:
#             email_subject = st.text_input(
#                 "Subject",
#                 f"Application for {st.session_state.selected_job['job_title']} Position",
#                 help="Email subject line"
#             )
    
#     email_body = f"""
# Dear Hiring Manager,

# I hope this email finds you well. I am excited to apply for the {st.session_state.selected_job['job_title']} position at {st.session_state.selected_job['company']}. 
# With my experience and skills, I am confident in my ability to contribute effectively to your team.

# Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
# to discuss how my background aligns with the role. I look forward to your response.

# Best regards,  
# {st.session_state.applicant_name}
# """
    
#     st.text_area(
#         "Email Body",
#         email_body,
#         height=200,
#         key="email_body"
#     )
    
#     if st.button("Send Application", key="send_application"):
#         with st.spinner("📤 Sending your application..."):
#             try:
#                 send_job_application_email(
#                     to_email=recipient_email,
#                     job_title=st.session_state.selected_job['job_title'],
#                     company=st.session_state.selected_job['company'],
#                     applicant_name=st.session_state.applicant_name,
#                     cv_path=st.session_state.cv_path,
#                     cover_letter_path=st.session_state.cover_letter_path
#                 )
#                 st.success("🎉 Application sent successfully!")
                
#                 # Update Google Sheets if configured
#                 if 'spreadsheet_id' in st.session_state and st.session_state.spreadsheet_id:
#                     job_data = {
#                         "job_title": st.session_state.selected_job['job_title'],
#                         "company": st.session_state.selected_job['company'],
#                         "location": st.session_state.selected_job['location'],
#                         "created": datetime.now().strftime("%Y-%m-%d"),
#                         "salary_min": st.session_state.selected_job.get('salary_min', ''),
#                         "salary_max": st.session_state.selected_job.get('salary_max', ''),
#                         "apply_link": st.session_state.selected_job.get('apply_link', ''),
#                         "status": "Applied",
#                         "application_date": datetime.now().strftime("%Y-%m-%d"),
#                         "interview_date": "",
#                         "notes": "Application sent via AI Job Assistant"
#                     }
                    
#                     if update_job_status_in_sheet(
#                         st.session_state.json_credentials_file,
#                         st.session_state.spreadsheet_id,
#                         "Sheet1",
#                         job_data
#                     ):
#                         st.success("📊 Application status updated in tracker!")
#                     else:
#                         st.warning("Could not update application tracker.")
                
#                 # Clean up temporary files after sending
#                 cleanup_temp_files()
#                 st.session_state.cover_letter_path = None
#                 st.session_state.cv_path = None
#             except Exception as e:
#                 st.error(f"Error sending application: {str(e)}")
# @st.cache_data(ttl=300)  # Cache for 5 minutes
# def load_applications(json_credentials_file, spreadsheet_id, _timestamp):
#     return get_job_status_from_sheet(json_credentials_file, spreadsheet_id)

# def render_application_tracker(json_credentials_file, spreadsheet_id):
#     st.title("Application Tracker")
#     st.markdown("""
#     Track your job applications and their status. Your applications are synced with Google Sheets for persistent storage.
    
#     **Setup Instructions:**
#     - Ensure your Google Sheet has the following columns: `job_title`, `company`, `location`, `created`, `salary_min`, `salary_max`, `apply_link`, `status`, `application_date`, `interview_date`, `notes`.
#     - Provide the path to your Google Sheets service account JSON file and the Spreadsheet ID in the sidebar settings.
#     """)

#     # Validate inputs
#     if not os.path.exists(json_credentials_file):
#         st.warning(f"⚠️ Google Sheets credentials file not found at {json_credentials_file}")
#         return
    
#     if not spreadsheet_id:
#         st.warning("Please enter a Google Sheet ID in the sidebar settings")
#         return
    
#     st.session_state.json_credentials_file = json_credentials_file
#     st.session_state.spreadsheet_id = spreadsheet_id

#     # Initialize last_refresh if it doesn't exist
#     if 'last_refresh' not in st.session_state:
#         st.session_state.last_refresh = 0

#     # Auto-refresh every 30 seconds
#     current_time = time.time()
#     if current_time - st.session_state.last_refresh > 30:
#         st.session_state.applications = load_applications(json_credentials_file, spreadsheet_id, current_time)
#         st.session_state.last_refresh = current_time

#     tab1, tab2 = st.tabs(["View Applications", "Add Application"])
    
#     with tab1:
#         st.subheader("Your Job Applications")
#         if st.button("Refresh Applications", key="refresh_apps"):
#             # Clear cache and reload
#             load_applications.clear()  # Clear the cache
#             st.session_state.applications = load_applications(json_credentials_file, spreadsheet_id, time.time())
#             st.session_state.last_refresh = time.time()
        
#         applications = st.session_state.applications
#         if applications is None:
#             st.warning("Failed to load applications. Check the error messages above for details.")
#         elif not applications:  # Empty list
#             st.warning("No applications found in the Google Sheet.")
#         else:
#             df = pd.DataFrame(applications)
#             st.session_state.applications_df = df  # Store for edit/delete operations
            
#             # Status counts
#             status_counts = df['status'].value_counts().reset_index()
#             status_counts.columns = ['Status', 'Count']
            
#             col1, col2, col3 = st.columns([2, 3, 1])
#             with col1:
#                 st.dataframe(status_counts, hide_index=True)
#             with col2:
#                 st.bar_chart(status_counts.set_index('Status'))
            
#             # Pagination
#             page_size = 10
#             total_rows = len(df)
#             total_pages = (total_rows + page_size - 1) // page_size
#             page = st.number_input("Page", min_value=1, max_value=max(1, total_pages), value=1, key="tracker_page")
#             start_idx = (page - 1) * page_size
#             end_idx = min(start_idx + page_size, total_rows)
            
#             st.write(f"Showing rows {start_idx + 1} to {end_idx} of {total_rows}")
            
#             # Display applications with edit/delete buttons
#             for idx in range(start_idx, end_idx):
#                 row = df.iloc[idx]
#                 with st.expander(f"{row['job_title']} at {row['company']} (Status: {row['status']})"):
#                     st.write(f"**Location:** {row['location']}")
#                     st.write(f"**Posted:** {row['created']}")
#                     st.write(f"**Salary Range:** {row['salary_min']} - {row['salary_max']}")
#                     st.write(f"**Application Date:** {row['application_date']}")
#                     st.write(f"**Interview Date:** {row['interview_date']}")
#                     st.write(f"**Notes:** {row['notes']}")
#                     st.write(f"**Apply Link:** {row['apply_link']}")
                    
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if st.button("Edit", key=f"edit_{idx}"):
#                             st.session_state[f"edit_mode_{idx}"] = True
#                     with col2:
#                         if st.button("Delete", key=f"delete_{idx}"):
#                             if st.session_state.get(f"confirm_delete_{idx}", False):
#                                 # Delete the row (row index in Google Sheets is idx + 2 because of header row and 1-based indexing)
#                                 if delete_row_from_sheet(json_credentials_file, spreadsheet_id, idx + 2):
#                                     st.success(f"Deleted application for {row['job_title']} at {row['company']}.")
#                                     st.session_state.applications = load_applications(json_credentials_file, spreadsheet_id, time.time())
#                                     st.session_state.last_refresh = time.time()
#                                 else:
#                                     st.error("Failed to delete application.")
#                                 st.session_state[f"confirm_delete_{idx}"] = False
#                             else:
#                                 st.session_state[f"confirm_delete_{idx}"] = True
#                                 st.warning("Are you sure? Click again to confirm.")
                    
#                     # Edit form
#                     if st.session_state.get(f"edit_mode_{idx}", False):
#                         with st.form(key=f"edit_form_{idx}"):
#                             col1, col2 = st.columns(2)
#                             with col1:
#                                 job_title = st.text_input("Job Title*", value=row['job_title'])
#                                 company = st.text_input("Company*", value=row['company'])
#                                 location = st.text_input("Location", value=row['location'])
#                                 created = st.date_input("Date Posted", value=datetime.strptime(row['created'], "%Y-%m-%d") if row['created'] else datetime.now())
#                                 salary_min = st.number_input("Min Salary", min_value=0.0, value=float(row['salary_min']) if row['salary_min'] else 0.0)
#                             with col2:
#                                 salary_max = st.number_input("Max Salary", min_value=0.0, value=float(row['salary_max']) if row['salary_max'] else 0.0)
#                                 apply_link = st.text_input("Application Link", value=row['apply_link'])
#                                 status = st.selectbox("Status*", ["Interested", "Applied", "Interview", "Offer", "Rejected"], index=["Interested", "Applied", "Interview", "Offer", "Rejected"].index(row['status']))
#                                 application_date = st.date_input("Application Date", value=datetime.strptime(row['application_date'], "%Y-%m-%d") if row['application_date'] else datetime.now())
#                                 interview_date = st.date_input("Interview Date", value=datetime.strptime(row['interview_date'], "%Y-%m-%d") if row['interview_date'] else None)
                            
#                             notes = st.text_area("Notes", value=row['notes'])
                            
#                             if st.form_submit_button("Save Changes"):
#                                 if not all([job_title, company, status]):
#                                     st.error("Please fill in all required fields (*)")
#                                 elif salary_min > salary_max:
#                                     st.error("Minimum salary cannot be greater than maximum salary.")
#                                 else:
#                                     updated_job_data = {
#                                         "job_title": job_title,
#                                         "company": company,
#                                         "location": location,
#                                         "created": created.strftime("%Y-%m-%d"),
#                                         "salary_min": str(salary_min),
#                                         "salary_max": str(salary_max),
#                                         "apply_link": apply_link,
#                                         "status": status,
#                                         "application_date": application_date.strftime("%Y-%m-%d"),
#                                         "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
#                                         "notes": notes
#                                     }
#                                     if update_row_in_sheet(json_credentials_file, spreadsheet_id, idx + 2, updated_job_data):
#                                         st.success(f"Updated application for {job_title} at {company}.")
#                                         st.session_state.applications = load_applications(json_credentials_file, spreadsheet_id, time.time())
#                                         st.session_state.last_refresh = time.time()
#                                         st.session_state[f"edit_mode_{idx}"] = False
#                                     else:
#                                         st.error("Failed to update application.")
    
#     with tab2:
#         st.subheader("Add New Application")
#         with st.form("new_application_form"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 job_title = st.text_input("Job Title*")
#                 company = st.text_input("Company*")
#                 location = st.text_input("Location")
#                 created = st.date_input("Date Posted", datetime.now())
#                 salary_min = st.number_input("Min Salary", min_value=0.0, value=0.0)
#             with col2:
#                 salary_max = st.number_input("Max Salary", min_value=0.0, value=0.0)
#                 apply_link = st.text_input("Application Link")
#                 status = st.selectbox(
#                     "Status*",
#                     ["Interested", "Applied", "Interview", "Offer", "Rejected"]
#                 )
#                 application_date = st.date_input("Application Date", datetime.now())
#                 interview_date = st.date_input("Interview Date", value=None)
            
#             notes = st.text_area("Notes")
            
#             submitted = st.form_submit_button("Add Application")
#             if submitted:
#                 if not all([job_title, company, status]):
#                     st.error("Please fill in all required fields (*)")
#                 elif salary_min > salary_max:
#                     st.error("Minimum salary cannot be greater than maximum salary.")
#                 else:
#                     job_data = {
#                         "job_title": job_title,
#                         "company": company,
#                         "location": location,
#                         "created": created.strftime("%Y-%m-%d"),
#                         "salary_min": str(salary_min),
#                         "salary_max": str(salary_max),
#                         "apply_link": apply_link,
#                         "status": status,
#                         "application_date": application_date.strftime("%Y-%m-%d"),
#                         "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
#                         "notes": notes
#                     }
                    
#                     if update_job_status_in_sheet(
#                         json_credentials_file,
#                         spreadsheet_id,
#                         "Sheet1",
#                         job_data
#                     ):
#                         st.success(f"Application for {job_title} at {company} added successfully!")
#                         st.session_state.applications = load_applications(json_credentials_file, spreadsheet_id, time.time())
#                         st.session_state.last_refresh = time.time()
#                         st.rerun()
#                     else:
#                         st.error("Failed to add application. Check your internet connection or credentials.")
# # def render_application_tracker(json_credentials_file, spreadsheet_id):
# #     st.title("Application Tracker")
# #     st.markdown("Track your job applications and their status.")
    
# #     if not os.path.exists(json_credentials_file):
# #         st.warning(f"⚠️ Google Sheets credentials file not found at {json_credentials_file}")
# #         return
    
# #     if not spreadsheet_id:
# #         st.warning("Please enter a Google Sheet ID in the sidebar settings")
# #         return
    
# #     st.session_state.json_credentials_file = json_credentials_file
# #     st.session_state.spreadsheet_id = spreadsheet_id
    
# #     tab1, tab2 = st.tabs(["View Applications", "Add Application"])
    
# #     with tab1:
# #         st.subheader("Your Job Applications")
# #         if st.button("Refresh Applications", key="refresh_apps"):
# #             st.rerun()
        
# #         applications = get_job_status_from_sheet(json_credentials_file, spreadsheet_id)
# #         if applications:
# #             df = pd.DataFrame(applications)
# #             st.session_state.applications = df
            
# #             # Status counts
# #             status_counts = df['status'].value_counts().reset_index()
# #             status_counts.columns = ['Status', 'Count']
            
# #             col1, col2, col3 = st.columns([2, 3, 1])
# #             with col1:
# #                 st.dataframe(status_counts, hide_index=True)
# #             with col2:
# #                 st.bar_chart(status_counts.set_index('Status'))
            
# #             st.dataframe(df)
# #         else:
# #             st.warning("No applications found or couldn't load data.")
    
# #     with tab2:
# #         st.subheader("Add New Application")
# #         with st.form("new_application_form"):
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 job_title = st.text_input("Job Title*")
# #                 company = st.text_input("Company*")
# #                 location = st.text_input("Location")
# #                 created = st.date_input("Date Posted", datetime.now())
# #                 salary_min = st.number_input("Min Salary", min_value=0)
# #             with col2:
# #                 salary_max = st.number_input("Max Salary", min_value=0)
# #                 apply_link = st.text_input("Application Link")
# #                 status = st.selectbox(
# #                     "Status*",
# #                     ["Interested", "Applied", "Interview", "Offer", "Rejected"]
# #                 )
# #                 application_date = st.date_input("Application Date", datetime.now())
# #                 interview_date = st.date_input("Interview Date", value=None)
            
# #             notes = st.text_area("Notes")
            
# #             submitted = st.form_submit_button("Add Application")
# #             if submitted:
# #                 if not job_title or not company or not status:
# #                     st.error("Please fill in required fields (*)")
# #                 else:
# #                     job_data = {
# #                         "job_title": job_title,
# #                         "company": company,
# #                         "location": location,
# #                         "created": created.strftime("%Y-%m-%d"),
# #                         "salary_min": salary_min,
# #                         "salary_max": salary_max,
# #                         "apply_link": apply_link,
# #                         "status": status,
# #                         "application_date": application_date.strftime("%Y-%m-%d"),
# #                         "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
# #                         "notes": notes
# #                     }
                    
# #                     if update_job_status_in_sheet(
# #                         json_credentials_file,
# #                         spreadsheet_id,
# #                         "Sheet1",
# #                         job_data
# #                     ):
# #                         st.success("Application added successfully!")
# #                         time.sleep(1)
# #                         st.rerun()
# #                     else:
# #                         st.error("Failed to add application.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import logging
import tempfile
import json

# Import functions from your existing files
from src.google_sheets_integration import authenticate_gsheet, update_job_status_in_sheet, get_job_status_from_sheet
from src.cover_letter_generator import generate_cover_letter, extract_experience_from_cv, extract_name_and_contact_from_cv, save_to_files
from src.email_sender import send_job_application_email
from src.job_scraper import JobScraper
from src.nlp_processing import extract_skills_from_description

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Custom CSS for Styling ---
def load_css():
    st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stButton>button { background-color: #4a90e2; color: white; border-radius: 8px; padding: 8px 16px; border: none; font-weight: 500; }
        .stButton>button:hover { background-color: #357abd; color: white; }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-radius: 8px; padding: 8px; }
        .stSelectbox>div>div>div { border-radius: 8px; padding: 4px; }
        .stDateInput>div>div>input { border-radius: 8px; padding: 8px; }
        .stNumberInput>div>div>input { border-radius: 8px; padding: 8px; }
        .header { color: #2c3e50; font-weight: 700; }
        .sidebar .sidebar-content { background-color: #2c3e50; color: white; }
        .sidebar .sidebar-content .stRadio>div { color: white; }
        .success-box { background-color: #d4edda; color: #155724; padding: 16px; border-radius: 8px; margin: 16px 0; }
        .warning-box { background-color: #fff3cd; color: #856404; padding: 16px; border-radius: 8px; margin: 16px 0; }
        .error-box { background-color: #f8d7da; color: #721c24; padding: 16px; border-radius: 8px; margin: 16px 0; }
        .job-card { background-color: white; border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .job-card h3 { color: #2c3e50; margin-top: 0; }
    </style>
    """, unsafe_allow_html=True)

# At the beginning of your main() function or before using session state
if 'cover_letter' not in st.session_state:
    st.session_state.cover_letter = ""
if 'cv_file' not in st.session_state:
    st.session_state.cv_file = None
if 'cover_letter_path' not in st.session_state:
    st.session_state.cover_letter_path = None
if 'cv_saved_path' not in st.session_state:
    st.session_state.cv_saved_path = None
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = {}
if 'applicant_name' not in st.session_state:
    st.session_state.applicant_name = "Applicant"

# --- Streamlit UI Components ---
def main():
    st.set_page_config(
        page_title="AI Job Assistant",
        layout="wide",
        page_icon="💼"
    )
    load_css()
    
    # Sidebar navigation
    st.sidebar.title("💼 AI Job Assistant")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Job Search", "📝 Cover Letter", "✉️ Email Application", "📊 Application Tracker"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Settings")
    json_credentials_file = None
    if hasattr(st, "secrets"):
        if "google_sheets" in st.secrets and "credentials_json" in st.secrets["google_sheets"]:
            try:
                credentials_json = st.secrets["google_sheets"]["credentials_json"]
                credentials_dict = json.loads(credentials_json)
            except json.JSONDecodeError as e:
                st.error(f"Invalid credentials_json in secrets.toml: {e}")
                return
            except Exception as e:
                st.error(f"Error loading credentials_json from secrets: {e}")
                return
            
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp_file:
                    json.dump(credentials_dict, tmp_file)
                    json_credentials_file = tmp_file.name
                st.session_state.spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
            except Exception as e:
                st.error(f"Error writing credentials to temporary file: {e}")
                return
    
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "🔍 Job Search":
        render_job_search()
    elif page == "📝 Cover Letter":
        render_cover_letter_generator()
    elif page == "✉️ Email Application":
        render_email_application()
    elif page == "📊 Application Tracker":
        render_application_tracker(json_credentials_file, st.session_state.spreadsheet_id if 'spreadsheet_id' in st.session_state else None)

    # Cleanup temporary file if it exists
    if json_credentials_file and os.path.exists(json_credentials_file):
        os.unlink(json_credentials_file)

def render_dashboard():
    st.title("AI Job Assistant Dashboard")
    st.markdown("""
    Welcome to your AI-powered job application assistant! This tool helps you:
    
    - 🔍 Search for relevant job opportunities
    - 📝 Generate personalized cover letters
    - ✉️ Send professional application emails
    - 📊 Track your application progress
    
    Get started by selecting a page from the sidebar.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Found", "25", "+5 from last week")
    with col2:
        st.metric("Applications Sent", "8", "3 pending")
    with col3:
        st.metric("Interview Rate", "25%", "2 of 8")
    
    st.markdown("---")
    st.subheader("Recent Activity")
    st.write("Your recent job application activity will appear here.")

def render_job_search():
    st.title("Job Search")
    st.markdown("Find your next career opportunity using our AI-powered job search.")
    
    with st.expander("🔍 Search Filters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            job_titles = st.text_input(
                "Job Titles (comma separated)",
                "Data Scientist, Machine Learning Engineer",
                help="Enter multiple job titles separated by commas"
            )
        with col2:
            location = st.text_input("Location", "London")
    
    if st.button("Search Jobs", key="search_jobs"):
        with st.spinner("🔍 Searching for jobs..."):
            job_list = [title.strip() for title in job_titles.split(",")]
            
            try:
                scraper = JobScraper(job_list, location=location)
                scraper.scrape_jobs()
                jobs = scraper.get_saved_jobs()
                
                if not jobs.empty:
                    st.session_state.job_results = jobs
                    st.success(f"🎉 Found {len(jobs)} jobs!")
                    
                    # Display jobs in cards
                    for idx, job in jobs.iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div class="job-card">
                                <h3>{job['job_title']}</h3>
                                <p><strong>Company:</strong> {job['company']}</p>
                                <p><strong>Location:</strong> {job['location']}</p>
                                <p><strong>Salary:</strong> £{job['salary_min']} - £{job['salary_max']}</p>
                                <a href="{job['apply_link']}" target="_blank">View Job</a>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found. Try different search terms.")
            except Exception as e:
                st.error(f"Error searching for jobs: {str(e)}")

# def render_cover_letter_generator():
#     st.title("Cover Letter Generator")
#     st.markdown("Create a personalized cover letter for your job application.")
    
#     if 'job_results' in st.session_state and not st.session_state.job_results.empty:
#         job_list = st.session_state.job_results[['job_title', 'company']].to_dict('records')
#         job_options = {f"{job['job_title']} at {job['company']}": idx for idx, job in enumerate(job_list)}
#         selected_job_key = st.selectbox(
#             "Select a job to apply for",
#             options=list(job_options.keys()),
#             help="Select a job from your previous search results"
#         )
#         selected_job_idx = job_options[selected_job_key]
#         selected_job = st.session_state.job_results.iloc[selected_job_idx]
#         st.session_state.selected_job = selected_job
        
#         with st.expander("📄 Job Details", expanded=True):
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown(f"**Job Title:** {selected_job['job_title']}")
#                 st.markdown(f"**Company:** {selected_job['company']}")
#                 st.markdown(f"**Location:** {selected_job['location']}")
#             with col2:
#                 st.markdown(f"**Salary Range:** £{selected_job['salary_min']} - £{selected_job['salary_max']}")
#                 st.markdown(f"**Posted:** {selected_job['created']}")
#                 st.markdown(f"[Apply Here]({selected_job['apply_link']})")
            
#             st.markdown("**Description:**")
#             st.write(selected_job['description'][:500] + "...")
#     else:
#         st.warning("⚠️ No job results available. Please search for jobs first.")
#         selected_job = None
    
#     if selected_job is not None:
#         st.subheader("Upload Your CV")
#         cv_file = st.file_uploader(
#             "Choose your CV file (PDF or DOCX)",
#             type=['pdf', 'docx'],
#             help="Upload your CV to personalize the cover letter"
#         )
        
#         if cv_file:
#             # Save the uploaded file temporarily
#             temp_cv_path = f"temp_cv.{cv_file.name.split('.')[-1]}"
#             with open(temp_cv_path, "wb") as f:
#                 f.write(cv_file.getbuffer())
            
#             st.session_state.cv_path = temp_cv_path
#             st.success("✅ CV uploaded successfully!")
            
#             if st.button("Generate Cover Letter", key="generate_cover_letter"):
#                 with st.spinner("✨ Generating your personalized cover letter..."):
#                     try:
#                         cover_letter = generate_cover_letter(
#                             selected_job['job_title'],
#                             selected_job['company'],
#                             selected_job['description'],
#                             temp_cv_path
#                         )
#                         st.session_state.cover_letter = cover_letter
                        
#                         # Extract name from CV for saving files
#                         name, _ = extract_name_and_contact_from_cv(temp_cv_path)
#                         st.session_state.applicant_name = name
                        
#                         st.subheader("Your Custom Cover Letter")
#                         st.text_area(
#                             "Cover Letter Content",
#                             cover_letter,
#                             height=400,
#                             label_visibility="collapsed"
#                         )
                        
#                         # Save to files
#                         if 'cover_letter_path' not in st.session_state:
#                             cover_letter_path, _ = save_to_files(temp_cv_path, cover_letter, name)
#                             st.session_state.cover_letter_path = cover_letter_path
#                             st.session_state.cv_saved_path = temp_cv_path
#                             st.success("📄 Cover letter saved successfully!")
#                     except Exception as e:
#                         st.error(f"Error generating cover letter: {str(e)}")
import tempfile
def render_cover_letter_generator():
    st.title("Cover Letter Generator")
    st.markdown("Create a personalized cover letter for your job application.")
    
    if 'job_results' not in st.session_state or st.session_state.job_results.empty:
        st.warning("⚠️ No job results available. Please search for jobs first.")
        return
    
    job_list = st.session_state.job_results[['job_title', 'company']].to_dict('records')
    job_options = {f"{job['job_title']} at {job['company']}": idx for idx, job in enumerate(job_list)}
    selected_job_key = st.selectbox(
        "Select a job to apply for",
        options=list(job_options.keys()),
        help="Select a job from your previous search results"
    )
    selected_job_idx = job_options[selected_job_key]
    selected_job = st.session_state.job_results.iloc[selected_job_idx]
    st.session_state.selected_job = selected_job
    
    with st.expander("📄 Job Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Job Title:** {selected_job['job_title']}")
            st.markdown(f"**Company:** {selected_job['company']}")
            st.markdown(f"**Location:** {selected_job['location']}")
        with col2:
            st.markdown(f"**Salary Range:** £{selected_job['salary_min']} - £{selected_job['salary_max']}")
            st.markdown(f"**Posted:** {selected_job['created']}")
            st.markdown(f"[Apply Here]({selected_job['apply_link']})")
        
        st.markdown("**Description:**")
        st.write(selected_job['description'][:500] + "...")
    
    st.subheader("Upload Your CV")
    cv_file = st.file_uploader(
        "Choose your CV file (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your CV to personalize the cover letter",
        key="cv_uploader_cover_letter"
    )
    
    if cv_file:
        # Store CV content and extension in session state
        st.session_state.cv_content = cv_file.getbuffer()
        st.session_state.cv_extension = cv_file.name.split('.')[-1]
        st.session_state.cv_filename = cv_file.name  # Store original filename for later use
        
        # Create a temporary file for cover letter generation using tempfile
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{st.session_state.cv_extension}") as temp_cv:
                temp_cv.write(st.session_state.cv_content)
                temp_cv_path = temp_cv.name
            logging.info(f"Saved temporary CV for generation: {temp_cv_path}")
        except Exception as e:
            logging.error(f"Failed to save temporary CV for generation: {str(e)}", exc_info=True)
            st.error(f"Error processing CV: {str(e)}")
            return
        
        st.success("✅ CV uploaded successfully!")
        
        if st.button("Generate Cover Letter", key="generate_cover_letter"):
            with st.spinner("✨ Generating your personalized cover letter..."):
                try:
                    cover_letter = generate_cover_letter(
                        selected_job['job_title'],
                        selected_job['company'],
                        selected_job['description'],
                        temp_cv_path
                    )
                    st.session_state.cover_letter = cover_letter
                    st.session_state.cover_letter_content = cover_letter
                    
                    # Extract name from CV
                    name, _ = extract_name_and_contact_from_cv(temp_cv_path)
                    st.session_state.applicant_name = name
                    
                    st.subheader("Your Custom Cover Letter")
                    st.text_area(
                        "Cover Letter Content",
                        cover_letter,
                        height=400,
                        label_visibility="collapsed"
                    )
                    st.success("📄 Cover letter generated successfully!")
                except Exception as e:
                    logging.error(f"Error generating cover letter: {str(e)}", exc_info=True)
                    st.error(f"Error generating cover letter: {str(e)}")
                finally:
                    # Clean up the temporary CV file
                    if os.path.exists(temp_cv_path):
                        try:
                            os.unlink(temp_cv_path)
                            logging.info(f"Deleted temporary CV file: {temp_cv_path}")
                        except Exception as e:
                            logging.warning(f"Failed to delete temporary CV file: {str(e)}")


import tempfile
import re
def render_email_application():
    st.title("Email Application")
    st.markdown("Send your job application with cover letter and CV attached.")
    required_keys = ['cover_letter', 'selected_job']
    if not all(key in st.session_state for key in required_keys):
    # if 'cover_letter' not in st.session_state or 'cv_path' not in st.session_state:
        st.warning("""
        ⚠️ Please complete these steps first:
        1. Search for jobs on the Job Search page
        2. Generate a cover letter on the Cover Letter page
        """)
        return
    # Safe access to cv_saved_path with default None
    cv_path = st.session_state.get('cv_saved_path')
    
    # File uploader as fallback if cv_saved_path doesn't exist
    cv_file = st.file_uploader(
        "Upload CV (PDF or DOCX)", 
        type=['pdf', 'docx'],
        key='cv_uploader'
    )
     # Use either the saved path or newly uploaded file
    current_cv = cv_path if cv_path else cv_file
    with st.expander("✉️ Email Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            recipient_email = st.text_input(
                "Recipient Email",
                help="The hiring manager's email address"
            )
        with col2:
            email_subject = st.text_input(
                "Subject",
                f"Application for {st.session_state.selected_job['job_title']} Position",
                help="Email subject line"
            )
    
    email_body = f"""
Dear Hiring Manager,

I hope this email finds you well. I am excited to apply for the {st.session_state.selected_job['job_title']} position at {st.session_state.selected_job['company']}. 
With my experience and skills, I am confident in my ability to contribute effectively to your team.

Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
to discuss how my background aligns with the role. I look forward to your response.

Best regards,  
{st.session_state.applicant_name}
"""
    
    st.text_area(
        "Email Body",
        email_body,
        height=200,
        key="email_body"
    )
    
    if st.button("Send Application", key="send_application"):
        with st.spinner("📤 Sending your application..."):
            try:
                success = send_job_application_email(
                    recipient_email,
                    email_subject,
                    email_body,
                    current_cv, 
                    # st.session_state.cv_saved_path,
                    st.session_state.cover_letter_path
                )
                
                if success:
                    st.success("🎉 Application sent successfully!")
                    
                    # Update Google Sheets if configured
                    if 'spreadsheet_id' in st.session_state and st.session_state.spreadsheet_id:
                        job_data = {
                            "job_title": st.session_state.selected_job['job_title'],
                            "company": st.session_state.selected_job['company'],
                            "location": st.session_state.selected_job['location'],
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "salary_min": st.session_state.selected_job.get('salary_min', ''),
                            "salary_max": st.session_state.selected_job.get('salary_max', ''),
                            "apply_link": st.session_state.selected_job.get('apply_link', ''),
                            "status": "Applied",
                            "application_date": datetime.now().strftime("%Y-%m-%d"),
                            "interview_date": "",
                            "notes": "Application sent via AI Job Assistant"
                        }
                        
                        if update_job_status_in_sheet(
                            st.session_state.json_credentials_file,
                            st.session_state.spreadsheet_id,
                            "Sheet1",
                            job_data
                        ):
                            st.success("📊 Application status updated in tracker!")
                        else:
                            st.warning("Could not update application tracker.")
                else:
                    st.error("Failed to send email. Please check your email settings.")
            except Exception as e:
                st.error(f"Error sending application: {str(e)}")


# def render_email_application():
#     st.title("Email Application")
#     st.markdown("Send your job application with cover letter and CV attached.")
#     required_keys = ['cover_letter', 'selected_job']
#     if not all(key in st.session_state for key in required_keys):
#         st.warning("""
#         ⚠️ Please complete these steps first:
#         1. Search for jobs on the Job Search page
#         2. Generate a cover letter on the Cover Letter page
#         """)
#         return

#     # Check for CV content in session state
#     if 'cv_content' not in st.session_state or 'cv_extension' not in st.session_state:
#         st.warning("CV not found in session. Please upload your CV.")
#         cv_file = st.file_uploader(
#             "Upload CV (PDF or DOCX)", 
#             type=['pdf', 'docx'],
#             key="cv_uploader_email"
#         )
#         if cv_file:
#             st.session_state.cv_content = cv_file.getbuffer()
#             st.session_state.cv_extension = cv_file.name.split('.')[-1]
#             st.session_state.cv_filename = cv_file.name
#             st.success("✅ CV uploaded successfully!")
#         else:
#             return

#     cv_content = st.session_state.cv_content
#     cv_extension = st.session_state.cv_extension
#     cv_filename = st.session_state.cv_filename

#     # Check for cover letter content in session state
#     if 'cover_letter_content' not in st.session_state:
#         st.error("Cover letter content not found. Please generate a cover letter first.")
#         return
#     cover_letter_content = st.session_state.cover_letter_content

#     with st.expander("✉️ Email Details", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             sender_email = st.text_input(
#                 "Your Email Address",
#                 help="The email address to send from (e.g., your Gmail address)"
#             )
#             sender_password = st.text_input(
#                 "Your Email Password",
#                 type="password",
#                 help="For Gmail, use an App Password (not your regular password). See Google's App Password setup."
#             )
#             recipient_email = st.text_input(
#                 "Recipient Email",
#                 help="The hiring manager's email address"
#             )
#         with col2:
#             email_subject = st.text_input(
#                 "Subject",
#                 f"Application for {st.session_state.selected_job['job_title']} Position",
#                 help="Email subject line"
#             )
    
#     email_body = f"""
# Dear Hiring Manager,

# I hope this email finds you well. I am excited to apply for the {st.session_state.selected_job['job_title']} position at {st.session_state.selected_job['company']}. 
# With my experience and skills, I am confident in my ability to contribute effectively to your team.

# Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
# to discuss how my background aligns with the role. I look forward to your response.

# Best regards,  
# {st.session_state.applicant_name}
# """
    
#     st.text_area(
#         "Email Body",
#         email_body,
#         height=200,
#         key="email_body"
#     )
    
#     if st.button("Send Application", key="send_application"):
#         if not recipient_email:
#             st.error("Please provide a recipient email address.")
#             return
#         if not sender_email:
#             st.error("Please provide your email address.")
#             return
#         if not sender_password:
#             st.error("Please provide your email password (e.g., Gmail App Password).")
#             return

#         # Create a temporary CV file using tempfile
#         applicant_name = st.session_state.get('applicant_name', 'Applicant')
#         # Sanitize applicant name to avoid invalid filename characters
#         safe_applicant_name = re.sub(r'[<>:"/\\|?*]', '_', applicant_name)
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=f".{cv_extension}") as temp_cv:
#                 temp_cv.write(cv_content)
#                 temp_cv_path = temp_cv.name
#             logging.info(f"Saved temporary CV for email: {temp_cv_path}")
#             if not os.path.exists(temp_cv_path):
#                 raise Exception(f"Temporary CV file not found after creation: {temp_cv_path}")
#         except Exception as e:
#             logging.error(f"Failed to save temporary CV for email: {str(e)}", exc_info=True)
#             st.error(f"Error preparing CV for email: {str(e)}")
#             return

#         # Create a temporary cover letter file using tempfile
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_cover:
#                 temp_cover.write(cover_letter_content.encode('utf-8'))
#                 cover_letter_path = temp_cover.name
#             logging.info(f"Saved temporary cover letter for email: {cover_letter_path}")
#             if not os.path.exists(cover_letter_path):
#                 raise Exception(f"Temporary cover letter file not found after creation: {cover_letter_path}")
#         except Exception as e:
#             logging.error(f"Failed to write temporary cover letter file: {str(e)}", exc_info=True)
#             st.error(f"Error preparing cover letter for email: {str(e)}")
#             return

#         with st.spinner("📤 Sending your application..."):
#             try:
#                 success = send_job_application_email(
#                     recipient_email,
#                     email_subject,
#                     email_body,
#                     temp_cv_path,
#                     cover_letter_path,
#                     sender_email=sender_email,
#                     sender_password=sender_password
#                 )
                
#                 if success:
#                     st.success("🎉 Application sent successfully!")
                    
#                     # Update Google Sheets if configured
#                     if 'spreadsheet_id' in st.session_state and st.session_state.spreadsheet_id:
#                         job_data = {
#                             "job_title": st.session_state.selected_job['job_title'],
#                             "company": st.session_state.selected_job['company'],
#                             "location": st.session_state.selected_job['location'],
#                             "created": datetime.now().strftime("%Y-%m-%d"),
#                             "salary_min": st.session_state.selected_job.get('salary_min', ''),
#                             "salary_max": st.session_state.selected_job.get('salary_max', ''),
#                             "apply_link": st.session_state.selected_job.get('apply_link', ''),
#                             "status": "Applied",
#                             "application_date": datetime.now().strftime("%Y-%m-%d"),
#                             "interview_date": "",
#                             "notes": "Application sent via AI Job Assistant"
#                         }
                        
#                         if update_job_status_in_sheet(
#                             st.session_state.json_credentials_file,
#                             st.session_state.spreadsheet_id,
#                             "Sheet1",
#                             job_data
#                         ):
#                             st.success("📊 Application status updated in tracker!")
#                         else:
#                             st.warning("Could not update application tracker.")
#                 else:
#                     st.error("Failed to send email. Please check your email settings.")
#             except Exception as e:
#                 st.error(f"Error sending application: {str(e)}")
#             finally:
#                 # Clean up the temporary files
#                 for temp_file in [temp_cv_path, cover_letter_path]:
#                     if os.path.exists(temp_file):
#                         try:
#                             os.unlink(temp_file)
#                             logging.info(f"Deleted temporary file: {temp_file}")
#                         except Exception as e:
#                             logging.warning(f"Failed to delete temporary file {temp_file}: {str(e)}")
# def render_email_application():
#     st.title("Email Application")
#     st.markdown("Send your job application with cover letter and CV attached.")
#     required_keys = ['cover_letter', 'selected_job']
#     if not all(key in st.session_state for key in required_keys):
#         st.warning("""
#         ⚠️ Please complete these steps first:
#         1. Search for jobs on the Job Search page
#         2. Generate a cover letter on the Cover Letter page
#         """)
#         return
#     # Safe access to cv_saved_path with default None
#     cv_path = st.session_state.get('cv_saved_path')
    
#     # File uploader as fallback if cv_saved_path doesn't exist
#     cv_file = st.file_uploader(
#         "Upload CV (PDF or DOCX)", 
#         type=['pdf', 'docx'],
#         key='cv_uploader'
#     )
#      # Use either the saved path or newly uploaded file
#     current_cv = cv_path if cv_path else cv_file
#     with st.expander("✉️ Email Details", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             recipient_email = st.text_input(
#                 "Recipient Email",
#                 help="The hiring manager's email address"
#             )
#         with col2:
#             email_subject = st.text_input(
#                 "Subject",
#                 f"Application for {st.session_state.selected_job['job_title']} Position",
#                 help="Email subject line"
#             )
    
#     email_body = f"""
# Dear Hiring Manager,

# I hope this email finds you well. I am excited to apply for the {st.session_state.selected_job['job_title']} position at {st.session_state.selected_job['company']}. 
# With my experience and skills, I am confident in my ability to contribute effectively to your team.

# Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
# to discuss how my background aligns with the role. I look forward to your response.

# Best regards,  
# {st.session_state.applicant_name}
# """
    
#     st.text_area(
#         "Email Body",
#         email_body,
#         height=200,
#         key="email_body"
#     )
    
#     if st.button("Send Application", key="send_application"):
#         with st.spinner("📤 Sending your application..."):
#             try:
#                 success = send_job_application_email(
#                     recipient_email,
#                     email_subject,
#                     email_body,
#                     current_cv,
#                     st.session_state.cover_letter_path
#                 )
                
#                 if success:
#                     st.success("🎉 Application sent successfully!")
                    
#                     # Update Google Sheets if configured
#                     if spreadsheet_id:
#                         job_data = {
#                             "job_title": st.session_state.selected_job['job_title'],
#                             "company": st.session_state.selected_job['company'],
#                             "location": st.session_state.selected_job['location'],
#                             "created": datetime.now().strftime("%Y-%m-%d"),
#                             "salary_min": st.session_state.selected_job.get('salary_min', ''),
#                             "salary_max": st.session_state.selected_job.get('salary_max', ''),
#                             "apply_link": st.session_state.selected_job.get('apply_link', ''),
#                             "status": "Applied",
#                             "application_date": datetime.now().strftime("%Y-%m-%d"),
#                             "interview_date": "",
#                             "notes": "Application sent via AI Job Assistant"
#                         }
                        
#                         if update_job_status_in_sheet(
#                             st.secrets["google_sheets"]["credentials_json"],
#                             st.secrets["google_sheets"]["spreadsheet_id"],
#                             "Sheet1",
#                             job_data
#                         ):
#                             st.success("📊 Application status updated in tracker!")
#                         else:
#                             st.warning("Could not update application tracker.")
#                 else:
#                     st.error("Failed to send email. Please check your email settings.")
#             except Exception as e:
#                 st.error(f"Error sending application: {str(e)}")

def render_application_tracker(json_credentials_file, spreadsheet_id):
    st.title("Application Tracker")
    st.markdown("Track your job applications and their status.")
    
    if not json_credentials_file:
        st.warning("⚠️ Google Sheets credentials not configured. Check secrets.")
        return
    
    if not spreadsheet_id:
        st.warning("Please configure a Google Sheet ID in secrets.")
        return
    
    st.session_state.json_credentials_file = json_credentials_file
    st.session_state.spreadsheet_id = spreadsheet_id
    
    tab1, tab2 = st.tabs(["View Applications", "Add Application"])
    
    with tab1:
        st.subheader("Your Job Applications")
        if st.button("Refresh Applications", key="refresh_apps"):
            st.experimental_rerun()
        
        applications = get_job_status_from_sheet(json_credentials_file, spreadsheet_id)
        if applications:
            df = pd.DataFrame(applications)
            st.session_state.applications = df
            
            # Status counts
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.dataframe(status_counts, hide_index=True)
            with col2:
                st.bar_chart(status_counts.set_index('Status'))
            
            st.dataframe(df)
        else:
            st.warning("No applications found or couldn't load data.")
    
    with tab2:
        st.subheader("Add New Application")
        with st.form("new_application_form"):
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Job Title*")
                company = st.text_input("Company*")
                location = st.text_input("Location")
                created = st.date_input("Date Posted", datetime.now())
                salary_min = st.number_input("Min Salary", min_value=0)
            with col2:
                salary_max = st.number_input("Max Salary", min_value=0)
                apply_link = st.text_input("Application Link")
                status = st.selectbox(
                    "Status*",
                    ["Interested", "Applied", "Interview", "Offer", "Rejected"]
                )
                application_date = st.date_input("Application Date", datetime.now())
                interview_date = st.date_input("Interview Date", value=None)
            
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Application")
            if submitted:
                if not job_title or not company or not status:
                    st.error("Please fill in required fields (*)")
                else:
                    job_data = {
                        "job_title": job_title,
                        "company": company,
                        "location": location,
                        "created": created.strftime("%Y-%m-%d"),
                        "salary_min": salary_min,
                        "salary_max": salary_max,
                        "apply_link": apply_link,
                        "status": status,
                        "application_date": application_date.strftime("%Y-%m-%d"),
                        "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
                        "notes": notes
                    }
                    
                    if update_job_status_in_sheet(
                        json_credentials_file,
                        spreadsheet_id,
                        "Sheet1",
                        job_data
                    ):
                        st.success("Application added successfully!")
                        time.sleep(1)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to add application.")

if __name__ == "__main__":
    main()