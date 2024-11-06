import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

build_status = os.getenv('BUILD_STATUS', 'Unknown')
build_definition = os.getenv('BUILD_DEFINITION', 'Unknown')
build_id = os.getenv('BUILD_ID', 'Unknown')
build_branch = os.getenv('BUILD_BRANCH', 'Unknown')

sender_email = "goofygitlab@gmail.com"
receiver_email = "goofygitlab@gmail.com"
app_password = os.getenv('GMAIL_PASSWORD')

subject = f"Azure DevOps Pipeline Status: {build_definition} - {build_id}"
body = f"""
The build pipeline has completed with status: {build_status}

Pipeline Name: {build_definition}
Build ID: {build_id}
Branch: {build_branch}
"""

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")

""" for azure devops
- script: |
    SUBJECT="Azure DevOps Pipeline Status: $(Build.DefinitionName) - $(Build.BuildId)"
    BODY="The build pipeline has completed with status: $(Build.Status)\n\n"
    BODY="${BODY}Pipeline Name: $(Build.DefinitionName)\n"
    BODY="${BODY}Build ID: $(Build.BuildId)\n"
    BODY="${BODY}Branch: $(Build.SourceBranchName)\n"
    BODY="${BODY}Build Status: $(Build.Status)\n"
    MAIL="goofygitlab@gmail.com"  
    echo -e "Subject: $SUBJECT\n\n$BODY" | \
    curl --url 'smtp://smtp.gmail.com:587' --ssl-reqd \
     --mail-from "$MAIL" --mail-rcpt "$MAIL" \
     --user "$MAIL:${GMAIL_PASSWORD}"
  displayName: 'Send Pipeline Status Email'
"""
