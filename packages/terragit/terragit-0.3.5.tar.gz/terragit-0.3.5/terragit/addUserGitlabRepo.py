import requests
import re
import base64
from terragit.utilsFunctions import *
from terragit.terragrunt import *

class AddUserGitlabRepo:
    def __init__(self, gitlab_token, git_url):
        self.gitlab_token = gitlab_token
        self.git_url = git_url
        self.utils_functions = UtilsFunctions(gitlab_token, git_url)
        self.bcolor = bcolors()
    def add_user(self, project_id, grp_id, gitlab_username, access_level, exist, keybase):
        headers = {'PRIVATE-TOKEN': self.gitlab_token}
        if "user does not exist in gitlab group" in exist:
            if access_level.lower() == "guest":
                level = 10
            elif access_level.lower() == "reporter":
                level = 20
            elif access_level.lower() == "developer":
                level = 30
            elif access_level.lower() == "maintainer":
                level = 40
            elif access_level.lower() == "owner":
                level = 50
            url = self.git_url + "/api/v4/users?username=" + str(gitlab_username)
            user = requests.get(url, headers=headers).json()
            if grp_id is not None:
                url = self.git_url + "/api/v4/groups/" + str(grp_id) + "/members?user_id=" + str(
                    user[0]['id']) + "&access_level=" + str(level)
                add = requests.post(url, headers=headers)
        if "IAM user not found" in exist:
            self.utils_functions.apply_service(project_id, self.gitlab_token, "addUser", "create_user", "master",
                                               gitlab_username, keybase)

    def check_user_existance(self, project_id, grp_id, gitlab_username):
        headers = {'PRIVATE-TOKEN': self.gitlab_token}
        exist = ""
        url = self.git_url + "/api/v4/users?username=" + str(gitlab_username)
        user = requests.get(url, headers=headers).json()
        # print("user", user)
        try:
            url = self.git_url + "/api/v4/groups/" + str(grp_id) + "/members/all?user_ids=" + str(user[0]['id'])
            exist = requests.get(url, headers=headers).json()
            # print("exist", exist)
            if len(exist) > 0:
                exist = "user exist in gitlab group & "
            else:
                exist = "user does not exist in gitlab group & "
        except:
            exist = "problem occured while checking user existance in gitlab "
            print(bcolors.FAIL, exist)
            return exist
        res = self.utils_functions.check_content_existance_in_service(project_id,'https://git@gitlab.com/commons-acp/terraform/aws/user.git','name="' + gitlab_username + '"')
        if "content_found" in res:
            print(bcolors.OKGREEN, exist + "IAM user found")
            return exist + "IAM user found"
        else:
            print(bcolors.OKGREEN, exist + "IAM user found")
            return exist + "IAM user not found"

