# Bluebeam Document Review Invitation Sender

This project is designed for distributing PDF files for review using Bluebeam Revu Studio Sessions. The workflow automates email invitations with links to the Bluebeam session and the required files, making it easier for users to manage document reviews efficiently. This project is hosted in a Google Colab environment and integrates with Google Drive for file storage.

## Table of Contents
1. [Overview](#overview)
2. [Folder Structure](#folder-structure)
3. [Setup and Dependencies](#setup-and-dependencies)
4. [Google Drive Integration](#google-drive-integration)
5. [Project Files](#project-files)
6. [Usage](#usage)
7. [Email Sending Process](#email-sending-process)
8. [Troubleshooting](#troubleshooting)

## Overview

This project automates the process of creating and sending out Bluebeam Revu Studio Session invitations. The typical use case involves:
1. Uploading project files (mostly PDFs) for review to Bluebeam Revu Studio session.
2. Retrieving the session ID.
3. Using a Google Colab notebook to generate email content with the session details and file links.
4. Sending out the email invitations with the generated content.

## Folder Structure

The project relies on a specific folder structure within Google Drive. Ensure your Google Drive is set up as follows:

```
/content/drive/Shareddrives/PPDO_data_systems/document_review_invite_sender
└── invite_sender.py

/content/drive/Shareddrives/PPDO_data_systems/plan_review_sender/
└── rev_dist_files
      ├── gmail_creds.json
      └── reviewer_comments.xls
```

### Explanation of Files
- **invite_sender.py**: This script processes email content and file paths. It handles:
  - Reading the email template from the `Templates/` directory.
  - Formatting the email subject and body.
  - Saving the generated email text to the `Output/` directory.
  - Sending the email using `yagmail` with OAuth2 credentials.

- **document_review_invite_sender.ipynb**: The main notebook that guides the user through the process of generating email content for Bluebeam session invitations. It includes sections for inputting project details, mounting Google Drive, and creating email content based on the file information.

- **reviewer_comments.xls** Spreadsheet for docuement reviewers to fill out en lieu of marking up the docuemnts in Revu

## Setup and Dependencies

To use the Colab notebook effectively, you need the following:
- A Google Account with access to Google Drive and PPDO_data_systems shared drive.
- A Google Colab environment to run the notebook.
- Access to Bluebeam Revu with permissions to create Studio Sessions.

### Required Python Packages
The necessary Python packages are automatically handled by the Colab environment, but if you run this locally, you will need:
- `google-colab`
- `google-auth`
- `pandas`
- `os` (standard library)

## Google Drive Integration

The notebook mounts your Google Drive to access and store files. Ensure that your Google Drive directory structure matches the expected format mentioned above.

### How to Mount Google Drive
The Google Colab notebook includes the following command to mount your Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
```
Make sure to grant the necessary permissions when prompted

## Project Files

### 1. `document_review_invite_sender.ipynb`
The main notebook that guides the user through the process of generating email content for Bluebeam session invitations. It includes sections for inputting project details, mounting Google Drive, and creating email content based on the file information.

### 2. `invite_sender.py`
A helper script that processes email content and file paths. This script handles:
- Reading the email template from the `Templates/` directory.
- Formatting the email subject and body.
- Saving the generated email text to the `Output/` directory.

### 3. Documentation (`Documentation_ Bluebeam Document Review.pdf`)
This PDF file provides detailed instructions on the Bluebeam document review process and usage guidelines for the project files.

## Hard-Coded Paths in the Notebook
The following paths are defined in the notebook and must align with your Google Drive structure:

- **`/content/drive/MyDrive/Bluebeam_Review/Session_Files/`**: Location where session files are stored.
- **`/content/drive/MyDrive/Bluebeam_Review/Shared_Links/`**: Directory for files shared via links.
- **`/content/drive/MyDrive/Templates/email_template.txt`**: Email template file used for generating content.
- **`/content/drive/MyDrive/Output/email_content.txt`**: Output file where the generated email text is saved.

Ensure these directories exist and are correctly set up in your Google Drive.

## Usage

1. **Create a New Bluebeam Session**:
   - Open Bluebeam Revu and create a new session.
   - Name the session using the format: `<Project_Number>_<Review_Type>_Completion_<Date>`.
   - Retrieve the session ID (found in the session settings or invite window).

2. **Prepare the Google Colab Notebook**:
   - Open the `document_review_invite_sender.ipynb` notebook in Google Colab.
   - Mount your Google Drive by running the cell with the command:
     ```python
     from google.colab import drive
     drive.mount('/content/drive')
     ```
   - Ensure the necessary files are in the correct directories in your Google Drive.

3. **Input Project Details**:
   - Fill in the required project details in the notebook cells, such as `project_manager`, `project_number`, `project_name`, `recharge_number`, `review_type`, `download_url`, `review_end_date`, and `notes_for_reviewers`.

4. **Generate Email Content**:
   - Run the notebook cells to generate the email content. The notebook will format the email subject and body based on the provided project details and template.

5. **Send Email Invitations**:
   - Use the `yagmail` library to send the generated email content to the list of reviewer emails. Ensure your OAuth2 credentials are correctly set up as described in the troubleshooting section.

6. **Verify Email Sent**:
   - Check the Colab output logs to confirm that the email invitations were sent successfully.

## Troubleshooting

1. **Google Drive Mounting Issues**:
   - Ensure you grant the necessary permissions when prompted.
   - Verify the folder paths in the notebook match your Google Drive structure.

2. **File Not Found Errors**:
   - Check that the files are uploaded to the correct directory in Google Drive.
   - Ensure the file paths in the notebook are updated correctly.


### 4. **OAuth2 Gmail Credentials for `yagmail`**

This project uses `yagmail` to send email invitations via Gmail. For enhanced security, OAuth2 authentication is used instead of storing plaintext passwords. Follow the steps below to set up and use OAuth2 credentials.

#### **OAuth2 Credential Setup**

1. **Obtain OAuth2 Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the "Gmail API".
   - Configure the OAuth consent screen and create OAuth2 client credentials.
   - Download the `credentials.json` file. This file contains your `client_id` and `client_secret`.

2. **Generate `gmail_creds.json` File**:
   - Use the `yagmail` setup process to create an OAuth2 credentials file:
     ```bash
     python -m yagmail.register --oauth2
     ```
   - Follow the prompts to upload the `credentials.json` file and authenticate. The resulting `oauth2_creds.json` file will be saved locally.
   - Can be created manually too. JSON keys in the file are email_address, google_client_id, google_client_secret, and google_refresh_token 



#### **Common Issues and Fixes**

- **OAuth2 File Not Found**: Ensure the `gmail_creds.json` file is in the correct path.
- **Invalid Credentials Error**: If you receive an "Invalid Credentials" error, try regenerating the OAuth2 file using the `yagmail.register` command.
- **Permission Denied**: Make sure the Gmail account has enabled access to "Less Secure Apps" or set up the Gmail API with the correct scopes during the OAuth2 setup.
