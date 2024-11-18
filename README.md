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
1. Uploading project files (mostly PDFs) for review.
2. Creating a Bluebeam session and retrieving the session ID.
3. Using a Google Colab notebook to generate email content with the session details and file links.
4. Sending out the email invitations with the generated content.

## Folder Structure

The project relies on a specific folder structure within Google Drive. Ensure your Google Drive is set up as follows:

```
/content/drive/MyDrive/ProjectReviews/
├── PDFs/
│   ├── Drawing1.pdf
│   ├── Drawing2.pdf
│   └── ...
├── ReviewerComments.xlsx
└── EmailTemplates/
    ├── SubjectLineTemplate.txt
    └── EmailBodyTemplate.txt
```

### Explanation of Folders
- **Bluebeam_Review/Session_Files/**: Stores all project-specific review files (e.g., drawings, specifications).
- **Bluebeam_Review/Shared_Links/**: Contains shareable links for files too large to be sent as email attachments.
- **Templates/**: Holds templates for the email content.
- **Output/**: Stores generated email content for review.

## Setup and Dependencies

To use the Colab notebook effectively, you need the following:
- A Google Account with access to Google Drive.
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

2. **Upload Files to Google Drive**:
   - Place the PDF files for review in the appropriate folder under `Session_Files/`.

3. **Generate Email Content Using Colab Notebook**:
   - Open the Colab notebook (`document_review_invite_sender.ipynb`).
   - Mount Google Drive when prompted.
   - Follow the instructions in the notebook to fill out the form with session details and file paths.
   - Run the form cell to generate the email content.

4. **Copy and Paste Email Content**:
   - Copy the generated subject line and email body from the output.
   - Paste it into your email client (Thunderbird recommended).
   - Attach the Excel sheet with reviewer comments and any original attachments.

## Troubleshooting

1. **Google Drive Mounting Issues**:
   - Ensure you grant the necessary permissions when prompted.
   - Verify the folder paths in the notebook match your Google Drive structure.

2. **File Not Found Errors**:
   - Check that the files are uploaded to the correct directory in Google Drive.
   - Ensure the file paths in the notebook are updated correctly.

3. **Email Content Not Generating**:
   - Verify the email template file exists in the `Templates/` directory.
   - Check the logs in the Colab output for error messages.

### 4. **OAuth2 Gmail Credentials for `yagmail`**

This project uses `yagmail` to send email invitations via Gmail. For enhanced security, OAuth2 authentication is used instead of storing plaintext passwords. Follow the steps below to set up and use OAuth2 credentials.

#### **OAuth2 Credential Setup**

1. **Obtain OAuth2 Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the "Gmail API".
   - Configure the OAuth consent screen and create OAuth2 client credentials.
   - Download the `credentials.json` file. This file contains your `client_id` and `client_secret`.

2. **Generate `oauth2_creds.json` File**:
   - Use the `yagmail` setup process to create an OAuth2 credentials file:
     ```bash
     python -m yagmail.register --oauth2
     ```
   - Follow the prompts to upload the `credentials.json` file and authenticate. The resulting `oauth2_creds.json` file will be saved locally.



#### **Common Issues and Fixes**

- **OAuth2 File Not Found**: Ensure the `oauth2_creds.json` file is in the correct path (e.g., `/content/drive/MyDrive/oauth2_creds.json`).
- **Invalid Credentials Error**: If you receive an "Invalid Credentials" error, try regenerating the OAuth2 file using the `yagmail.register` command.
- **Permission Denied**: Make sure the Gmail account has enabled access to "Less Secure Apps" or set up the Gmail API with the correct scopes during the OAuth2 setup.

By using OAuth2, your Gmail credentials are securely handled, reducing the risk of exposing sensitive information.
