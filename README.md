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
