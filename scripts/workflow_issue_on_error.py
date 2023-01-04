from github import Github
from datetime import datetime
import os

TOKEN = os.environ['TOKEN']
REPO_NAME = os.environ['REPO']
WORKFLOW = os.environ['WORKFLOW']
FLAG_LABEL = os.environ['FLAG_LABEL']
RUN_NUMBER = os.environ['RUN_NUMBER']
RUN_ID = os.environ['RUN_ID']

def get_tagged_issues(repo, flag_label, workflow):
    issues = repo.get_issues(state='open', labels=[flag_label])
    tagged_issues =[]
    for issue in issues:
        if workflow in issue.body:
            tagged_issues.append(issue)
    return(tagged_issues)

def create_issue(repo, repo_name, flag_label, workflow, run_number, run_id):
    run_link = f"http://github.com/{repo_name}/actions/runs/{run_id}"
    body_string = f"{workflow} [run number {run_number}]({run_link}) failed.\n"
    body_string += "Please examine the run itself for details.\n\n"
    body_string += "This issue has been automatically generated for "
    body_string += "notification purposes."

    title_string = f"{workflow} Scheduled Run Failed"
    new_issue = repo.create_issue(title = title_string, body = body_string, 
                                  labels=[flag_label])
    return(new_issue)


def add_comment(issue, run_number):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg_string = "Error reoccurred: " + dt_string
    msg_string += " run number: " + run_number
    issue.create_comment(msg_string) 
    return()

if __name__ == "__main__":
    
    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)
    tagged_issues = get_tagged_issues(repo, FLAG_LABEL, WORKFLOW)
    if not tagged_issues:
        create_issue(repo, REPO_NAME, FLAG_LABEL, WORKFLOW, RUN_NUMBER, RUN_ID)
    else:
        for issue in tagged_issues:
            add_comment(issue, RUN_NUMBER)
    for issue in tagged_issues:
        print(issue.number)
        print(issue.closed_at)
    



