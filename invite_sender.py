import re
import os
import json
import yagmail
import logging


from collections import defaultdict
from itertools import groupby


class Utilities:
    @staticmethod
    def get_email_addresses(s):
        """Returns an iterator of matched emails found in string s."""
        # Removing lines that start with '//' because the regular expression
        # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
        regex = re.compile(
            (
                "([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"
            )
        )
        return list((email[0] for email in re.findall(regex, s.lower()) if not email[0].startswith("//")))

    @staticmethod
    def kwargs_defaultdict(**kwargs):
        return defaultdict(None, kwargs)

    @staticmethod
    def yes_or_no(prompt_text):
        '''asks yes or no question to user and returns 'True' for a yes answer and 'False' for a no answer'''
        yes_and_no_list = ['yes', 'y', 'no', 'n']
        response = ''
        while response.lower() not in yes_and_no_list:
            response = input(prompt_text)
        if response in yes_and_no_list[2:]:
            return False
        else:
            return True

    @staticmethod
    def split_path(path):
        '''splits a path into each piece that corresponds to a mount point, directory name, or file'''
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    @staticmethod
    def parse_session_id(text):

        def all_equal(iterable):
            g = groupby(iterable)
            return next(g, True) and not next(g, False)

        greedy_regex = r"\D\d{3}-\d{3}-\d{3}[$|\D]?"
        picky_regex = r"\d{3}-\d{3}-\d{3}"
        ids_in_text = re.findall(greedy_regex, text)
        ids_in_text = [re.search(picky_regex, id).group() for id in ids_in_text]

        if not ids_in_text:
            logging.warning("WARNING: No Blubeam Session id found. Enter valid session id text")

        if not all_equal(ids_in_text):
            logging.warning(
                f"WARNING: {len(set(ids_in_text))} BLuebeam Session id matches found and some are not the same. \n Using the first match.")

        return ids_in_text[0] if ids_in_text else None


class DocumentReview:

    def __init__(self, review_files_dir=None):
        self.project_number = None
        self.project_name = None
        self.pm = None
        self.review_type = None
        self.files_url = None
        self.files_dir = review_files_dir
        self.reviewer_emails = None
        self.recharge_number = None
        self.review_end = None
        self.reviewer_notes = None
        self.session_id = None
        self.download_url = None
        self.datetime_format = "%m-%d-%Y"

    def __str__(self):
        """
        :return: human readable string of the review attributes
        """
        summary_str = f"Project Number: {self.project_number}\nProject Name: {self.project_name}\n"
        if self.pm:
            summary_str += f"PM: {self.pm}\n"
        summary_str += f"Recharge: {self.recharge_number}\n"
        if self.review_type:
            summary_str += f"Review Type: {self.review_type}\n"
        if self.files_url:
            summary_str += f"File download URL: {self.files_url}\n"
        summary_str += f"Review End: {self.review_end.strftime(self.datetime_format)}\n"

        # if there are reviewer emails we will format them into a list
        if self.reviewer_emails:
            reviewer_str = ''
            for idx, email in enumerate(self.reviewer_emails):
                reviewer_str += email
                if (idx % 4 == 0) and (idx != 0):
                    reviewer_str += '\n'
                else:
                    reviewer_str += ", "
            summary_str += f"Distribution Emails: {reviewer_str}\n"
        if self.reviewer_notes:
            summary_str += f"Reviewer Notes: {self.reviewer_notes}\n"

        # see if there are files for review and add their filenas to the summary
        file_paths = self.file_list_for_reviewing()
        if file_paths:
            summary_str += "Files under review: "
            for f_path in file_paths:
                filename = Utilities.split_path(f_path)[-1]
                summary_str += f"{filename}\n"

        return summary_str

    def invite_html(self) -> str:
        invite_html = r"""
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Plan_review_invite</title>
            </head>
            <body>
            <h2>PPDO Document Review</h2>
            <p>Please accept this email as a request for review for <i>Project {project_number}""".format(
            project_number=self.project_number)

        if self.project_name:
            invite_html += r""", {project_name} """.format(project_name=self.project_name)

        invite_html += """</i>on behalf of the University"""
        if self.pm:
            invite_html += """ project manager, {pm}""".format(pm=self.pm)

        invite_html += """. If possible, please leave your comments in the below Bluebeam Studio Session. If you do not have Bluebeam, please complete your review in either FileMaker or on the attached reviewer_comments spreadsheet.</p>
            <h3>&#160;</h3>
            <h3>Review Completion Date</h3>
            <p>Please have your comments available by the end of the day on {review_end}</p>
            <p>&#160;</p>
            <h3>Bluebeam Session</h3>""".format(review_end=self.review_end.strftime(self.datetime_format))

        invite_html += r"""Session URL: <a href="https://studio.bluebeam.com/hyperlink.html?link=studio.bluebeam.com/sessions/{session_id}">https://studio.bluebeam.com/hyperlink.html?link=studio.bluebeam.com/sessions/{session_id}</a></p>
            <p>&#160;</p>""".format(session_id=self.session_id)

        # if a download link is provided add it in the relevant html
        if self.download_url:
            file_dl_str = """<h3>Download Link</h3>
            <p>Download files here: <a href="{download_url}">{download_url}</a></p>
            <p>&#160;</p>""".format(download_url=self.download_url)
            invite_html += file_dl_str

        if self.reviewer_notes:
            invite_html += """
              <h3>&#160;</h3>
              <h3>Notes for Reviewers</h3>
              <p>{notes}</p>
              """.format(notes=self.reviewer_notes)

        invite_html += r"""<h3>Recharge</h3>
            <p>Time can be recharged to {recharge_number}</p>
            <p>&#160;</p>
            <p>Thank you,<br /><em>UCSC Construction Documents</em><br /><em> 1156 High Street, Barn G</em><br /><em> Physical Planning Development &amp; Operations</em><br /><em> University of California, Santa Cruz</em><br /><em> constdoc@ucsc.edu</em><br /><em> (831) 459-5326</em></p>
            </body>
            </html>
        """.format(recharge_number=self.recharge_number)
        #invite_html.format(**self.__dict__)
        return invite_html

    def check_necessary_data(self):
        """
        Checks if all necessary attributes are populated.
        """
        necessary_attr_list = ["project_number", "recharge_number", "reviewer_emails", "review_end"]
        attr_dict = defaultdict(None, self.__dict__)
        populated_attr = [x for x in list(attr_dict.keys()) if attr_dict[x]]
        if not all(x in populated_attr for x in necessary_attr_list):
            missing_fields_str = "Missing necessary info from the following fields: "
            for x in necessary_attr_list:
                if x not in populated_attr:
                    missing_fields_str += x
                    missing_fields_str += ", "
            logging.exception(missing_fields_str, exc_info=True)
            return False

        return True

    def session_name(self):
        name_str = str(self.project_number)
        name_str += f" {self.review_type} "
        name_str += " for completion "
        name_str += self.review_end.strftime(self.datetime_format)
        if len(name_str) > 60:
            print(
                f"Bluebeam only allows session names under 60 chars long. THe session name generated for this review is {len(name_str)} chars long",
                exc_info=True)
        return name_str

    def invite_email_subject(self):
        name_str = "Project " + str(self.project_number)
        if self.project_name:
            name_str += ", "
            name_str += self.project_name
        name_str += " -- "
        if self.review_type:
            name_str += self.review_type
        name_str += " Completion "
        name_str += self.review_end.strftime(self.datetime_format)
        return name_str

    def file_list_for_reviewing(self):
        """
        :return: list of paths to pdfs that need to be included in the review
        """
        if not self.files_dir:
            logging.exception("DocumentReview object is missing directory path ( files_dir) for submittal files",
                             exc_info=True)
            return []

        file_list = [os.path.join(self.files_dir, file) for file in os.listdir(self.files_dir) if
                     file.lower().endswith(".pdf")]
        return file_list



class InviteEmailer:
    def __init__(self, oauth_filepath: str):
        self.oauth_filepath = oauth_filepath
        self.sender_email = "constdoc@ucsc.edu"
        self.max_attachment_size = 22020096
        remove_oauth_file = False
        if os.path.exists(oauth_filepath):
            with open(oauth_filepath) as creds_json:
                creds_json_contents = json.load(creds_json)
                expected_cred_keys = [
                    "email_address",
                    "google_client_id",
                    "google_client_secret",
                    "google_refresh_token",
                ]
                # if not all of the expected keys from credential file exist, delete the file to initiate a
                # new authentication process
                if not all(
                        [x in expected_cred_keys for x in list(creds_json_contents.keys())]
                ):
                    remove_oauth_file = True

        # this needed to be removed from within the with
        if remove_oauth_file:
            os.remove(oauth_filepath)

        self.yag_client = yagmail.SMTP(self.sender_email, oauth2_file=self.oauth_filepath)

    @staticmethod
    def valid_attachments(file_list, max_attachment_size):
        """
        returns a sublist of files from self.files which are small enough to be a submittal attachment
        :return: None
        """
        # Exclude individual files tht are too big to be attached
        atx_size_good = lambda fp: (os.path.getsize(fp) <= max_attachment_size)
        valid_attachments = [
            some_atx for some_atx in file_list if atx_size_good(some_atx)
        ]

        # If all submittal files are collectively too big to be attached.
        while sum([os.path.getsize(atx) for atx in valid_attachments]) >= max_attachment_size:
            print(f"The file, {valid_attachments[-1]} is not being sent to reduce attachments size.")
            valid_attachments = valid_attachments[:-1]
        return valid_attachments

    def distribute_invite(self, doc_review: DocumentReview, review_spreadsheet_path: str, attempts=3):
        files_for_invitation = doc_review.file_list_for_reviewing()
        files_for_invitation.append(review_spreadsheet_path)
        html = doc_review.invite_html()
        attempt_num = 0
        send_attempt = {}
        while attempt_num < attempts:
            attempt_num += 1
            try:
                send_attempt = self.yag_client.send(
                    to=doc_review.reviewer_emails,
                    subject=doc_review.invite_email_subject(),
                    attachments=self.valid_attachments(files_for_invitation, self.max_attachment_size),
                    contents=[html],
                )
                return True
            except Exception as e:
                try:
                    if str(e.file.status) == '400':
                            print(f"Attempt to send invitation emails failed: \n {str(e)}\n Potentially an issue with gmail credentials")
                except:
                    print(f"Attempt to send invitation emails failed: \n {str(e)}")
        return False


