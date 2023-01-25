# issue_on_error.py
# Requires python 3.6+, PyGithub
#
# Creates or updates an issue on action failure. 
#
# Looks though REPO for open issues with FLAG_LABEL. If none,
# creates a new issue. If there is an open issue with FLAG_LABEL,
# looks for WORKFLOW in body. If none, creates an issue. If an
# issue for WORKFLOW exists, makes adds a comment.
#
# Requires the environment provide the variables in the block below.
# TOKEN must have access to update issues.


from datetime import datetime
import os
import json
import subprocess

REPO = os.environ['REPO']
WORKFLOW = os.environ['WORKFLOW']
FLAG_LABEL = os.environ['FLAG_LABEL']
RUN_NUMBER = os.environ['RUN_NUMBER']

def get_tagged_issues(flag_label, workflow):
    issues = subprocess.check_output(["gh", "issue", "list",
                                        "--state", "open",
                                        "--label", flag_label,
                                        "--json", "title,number,body"], 
                                        encoding="utf-8")
    issues = json.loads(issues)
    tagged_issues =[]
    for issue in issues:
        if workflow in issue.body:
            tagged_issues.append(issue)
    return(tagged_issues)

def create_issue(flag_label, workflow, run_number):
    body_string = f"{workflow} run number {run_number} failed.\n"
    body_string += "Please examine the run itself for details.\n\n"
    body_string += "This issue has been automatically generated for "
    body_string += "notification purposes."

    title_string = f"{workflow} Scheduled Run Failed"
    new_issue = subprocess.check_output(["gh", "issue", "create", 
                                        "--title", title_string,
                                        "--body", body_string,
                                        "--label", flag_label], 
                                        encoding="utf-8")
    return(new_issue)


def add_comment(issue_number, run_number):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg_string = "Error reoccurred: " + dt_string
    msg_string += " run number: " + run_number
    subprocess.run(["gh", "issue", "comment", issue_number, 
                    "--body", msg_string])
    return()

if __name__ == "__main__":
    tagged_issues = get_tagged_issues(FLAG_LABEL, WORKFLOW)
    if not tagged_issues:
        create_issue(FLAG_LABEL, WORKFLOW, RUN_NUMBER)
    else:
        for issue in tagged_issues:
            add_comment(issue["number"], RUN_NUMBER)
    for issue in tagged_issues:
        print(issue["number"])
        
    



