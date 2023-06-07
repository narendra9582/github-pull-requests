import requests
import smtplib
import ssl
from email.mime.text import MIMEText

github_api_url = 'https://api.github.com/repos/{owner}/{repo}/pulls'

owner = 'npm'
repo = 'cli'
email_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_address': 'sender.email@gmail.com',
    'email_password': 'password1',
    'recipient_email': 'recipient.email@gmail.com'
}

import datetime
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=7)

date_range = f'{start_date.isoformat()}..{end_date.isoformat()}'

response = requests.get(github_api_url.format(owner=owner, repo=repo), params={'state': 'all', 'sort': 'created', 'direction': 'desc', 'date': date_range})

if response.status_code == 200:
    pull_requests = response.json()

    opened_prs = [pr for pr in pull_requests if pr['state'] == 'open']
    closed_prs = [pr for pr in pull_requests if pr['state'] == 'closed']
    draft_prs = [pr for pr in pull_requests if pr['state'] == 'draft']

    subject = f"Pull Request Summary for {repo}"
    body = f"""
    Here is a summary of the pull requests for the repository {owner}/{repo} in the last week:

    - Opened Pull Requests:
    {len(opened_prs[1])} pull request(s) opened.

    - Closed Pull Requests:
    {len(closed_prs)} pull request(s) closed.

    - Draft Pull Requests:
    {len(draft_prs)} pull request(s) in draft.
    """
    #print(body)
    email = MIMEText(body)
    email['From'] = email_config['email_address']
    email['To'] = email_config['recipient_email']
    email['Subject'] = subject
    print(f"\nEmail from: -\n{email_config['email_address']} \nTo: -\n{email_config['recipient_email']} \n\nSubject: -\n{email['Subject']} \n\nbody: -\n{body}")
    # with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
    #     server.starttls()
    #     print('trying to login')
    #     server.login(email_config['email_address'], email_config['email_password'])
    #     server.send_message(email)
    #     print("Email sent successfully.")

else:
    print("Failed to retrieve pull requests from GitHub API.")
