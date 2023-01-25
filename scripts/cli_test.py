import subprocess
import json 

# Get the list of open issues with the label "ci:bot_issue"
#issues = subprocess.check_output(["gh", "issue", "list", "--state", "open", 
#                                "--label","ci:bot_issue",
#                                "--json", "title,number,labels"], encoding="utf-8")

#issues = json.loads(issues)
#for issue in issues:
#    print(issue["number"], issue["title"])

# create an arbitrary issue
new_issue= subprocess.check_output(["gh", "issue", "create", "--title", "test issue",
                "--body", "test body", "--label", "ci:bot_issue"], encoding="utf-8")
print(new_issue)
# comment on test issue
# subprocess.run(["gh", "issue", "comment", "90", "--body", "test comment"])
