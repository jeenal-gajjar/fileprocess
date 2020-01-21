# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This module send Email after File Processing.

from sales.email_content import CONTENT
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase


class EmailManager:

    """
    EmailManager to send log file as attachment
    """

    def __init__(self, config, log):
        self._log = log
        self.config = config
        self.email_content = CONTENT
        self.filepath = self.config.get_log_file()


    def _get_attachment(self):
        file_name = self.filepath.split('/')[-1]
        with open(self.filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )
        return part


    def send_mail(self):
        try:
            """With this function we send out our html email"""

            # Create message container - the correct MIME type is multipart/alternative here!
            message = MIMEMultipart('alternative')
            message['subject'] = self.config.get_email_subject()
            message['To'] = self.config.get_receiver_email()
            message['From'] = self.config.get_sender_email()

            # Credentials (if needed) for sending the mail
            password = self.config.get_password()
            html_body = MIMEText(self.email_content, "plain")
            message.attach(html_body)
            message.attach(self._get_attachment())

            server = smtplib.SMTP(self.config.get_smtp_server() + ":" + str(self.config.get_port()))
            #server.set_debuglevel(1)

            server.starttls()
            server.login(self.config.get_sender_email(), password)
            server.sendmail(self.config.get_sender_email(), self.config.get_receiver_email(), message.as_string())
            server.quit()
        except Exception as e:
            self._log.error("[ Email Manager -> send_maiil ] "+ e)





