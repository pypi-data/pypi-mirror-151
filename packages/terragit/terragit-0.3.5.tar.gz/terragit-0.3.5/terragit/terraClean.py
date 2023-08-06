from terragit.gitlabFunctions import *
from datetime import datetime, timedelta
import terragit.terragrunt as terragrunt


class TerraClean:
    def __init__(self, gitlab_token, git_url, ):
        self.bcolor = terragrunt.bcolors
        self.gitlab_functions = GitlabFunctions(gitlab_token, git_url)

    def clean(self, group_id, project_id, time, mr, branches):
        if project_id is not None:
            if branches == 'true':
                self.get_project_branches(project_id, time)
                return
            elif mr:
                self.clean_mrs(project_id, group_id, time)
                return
        elif group_id is not None:
            if branches == 'true':
                projects = []
                branches_to_delete = []
                page = 1
                per_page = 40
                while per_page == 40:
                    projects = projects+self.gitlab_functions.get_projects_of_group(group_id, page, per_page)
                    page = page + 1
                    per_page = len(projects)
                for project in projects:
                    branches_to_delete = branches_to_delete+self.get_project_branches(project['id'], time, "grp")
                self.delete_branches(branches_to_delete)
            elif mr == 'true':
                self.clean_mrs(project_id, group_id, time)
        # self.clean_mrs(project_id, group_id, time)

    def get_project_branches(self, project_id, time, param=""):
        branches = self.gitlab_functions.get_all_project_branches(project_id)
        branches_to_delete = []
        for br in branches:
            if 'commit' in br:
                commit_date = br['commit']['committed_date']
                commit_date = commit_date[0:commit_date.index('T')]
                datetime_object = datetime.strptime(commit_date, '%Y-%m-%d')
                commit_time_in_days = (datetime.utcnow() - datetime_object).days
                merged = ""
                if (commit_time_in_days >= time) and not (br["protected"]) and br["merged"]:
                    print(
                        self.bcolor.WARNING + "branch " + br["name"] + " is outdated by " + str(commit_time_in_days) +
                        " and it has been merged but not deleted its web_url is: " + br["web_url"])
                    br["project_id"] = project_id
                    branches_to_delete.append(br)
                elif (commit_time_in_days >= time) and not (br["protected"]) and not br["merged"]:
                    print(self.bcolor.WARNING + "last commit in branch " + br["name"] +
                          " it has been created " + str(commit_time_in_days)+" days ago, its web_url is: " + br["web_url"])
                    br["project_id"] = project_id
                    branches_to_delete.append(br)
                elif br["merged"]:
                    br["project_id"] = project_id
                    branches_to_delete.append(br)
                    print(self.bcolor.WARNING + "branch " + br["name"] +
                          " has been merged but not deleted its web_url is: " + br["web_url"])
        if param == "grp":
            return branches_to_delete
        else:
            self.delete_branches(branches_to_delete)

    def delete_branches(self, branches_to_delete):
        if len(branches_to_delete) == 0:
            print(self.bcolor.OKGREEN, "project is clean")
            return
        value = input(self.bcolor.OKBLUE + "would you like to delete all these branches at once, delete "
                                           "one by one or cancel clean operation ?[all/oneByOne/cancel]")
        if value == "all":
            for br in branches_to_delete:

                self.gitlab_functions.delete_branch(br["project_id"], br["name"])
        elif value == "oneByOne":
            for br in branches_to_delete:
                if input(self.bcolor.OKBLUE + "would you like to delete ths branch " +
                         br["name"] + " ?[yes/no]") == "yes":
                    self.gitlab_functions.delete_branch(br["project_id"], br["name"])

    def clean_mrs(self, project_id, group_id, time):
        created_before = datetime.now() - timedelta(days=time)
        created_before = created_before.strftime("%Y-%m-%dT%H:%M:%SZ")

        print("created_before ", created_before)
        mrs_to_delete = []
        if project_id is not None:
            mrs_to_delete = self.gitlab_functions.get_all_project_merge_requests(project_id, created_before)
        elif group_id is not None:
            mrs_to_delete = self.gitlab_functions.get_all_group_merge_requests(group_id, created_before)

        if len(mrs_to_delete) == 0:
            print(self.bcolor.OKGREEN, "project is clean")
        else:
            for mr in mrs_to_delete:
                print(self.bcolor.WARNING + "Merge request " + mr["title"] + " is created before " + str(
                    created_before))
            value = input(self.bcolor.OKBLUE + "would you like to delete all these merge requests at once, delete "
                                               "one by one or cancel clean operation ?[all/oneByOne/cancel]")

            if value == "all":
                for mr in mrs_to_delete:
                    self.gitlab_functions.delete_merge_request(mr["project_id"], mr["iid"])
            elif value == "oneByOne":
                for mr in mrs_to_delete:
                    if input(self.bcolor.OKBLUE + "would you like to delete this merge requests " +
                             mr["title"] + " ?[yes/no]") == "yes":
                        self.gitlab_functions.delete_merge_request(mr["project_id"], mr["iid"])
            elif value == "cancel":
                return
            print(self.bcolor.OKGREEN, "project has been cleaned successfully")