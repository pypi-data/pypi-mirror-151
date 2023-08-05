import requests
import json
from datetime import datetime
from .pull_request_details import *
from .enums import *

def _parse_response(response):
   match response.status_code:
      case 200:
         return json.loads(response.text)
      case 401:
         print("unauthorized")
         return None
      case 404:
         print("not found")
         return None
      case _:
         return None

def auth(client_id, secret):
   url = "https://bitbucket.org/site/oauth2/access_token"
   response = requests.post(
      url,
      auth = (client_id, secret),
      data = {'grant_type': 'client_credentials'}
   )
   return _parse_response(response)

def get_last_commit(access_token, workspace, repo, branch="develop"):
   url = "https://api.bitbucket.org/2.0/repositories/{}/{}/commits/{}?start=1&limit=1".format(workspace,repo,branch)
   headers = {
      "Accept": "application/json",
      "Authorization": "Bearer %s" % access_token
   }

   response = requests.get(
      url,
      headers = headers,
   )

   return _parse_response(response)

def list_pullrequests(access_token, workspace, repo, state = PullRequestState.MERGED, page = 1):
   url = "https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests".format(workspace,repo)

   headers = {
      "Accept": "application/json",
      "Authorization": "Bearer %s" % access_token
   }

   response = requests.get(
      url,
      headers = headers,
      params = {
         'state': state.value, 
         'page': page
      }
   )

   json_parsed = _parse_response(response)
   pr_list = []
   for value in json_parsed["values"]:
      pr = PullRequestDetails(value["author"]["display_name"], value["source"]["branch"]["name"], value["title"], value["description"].rstrip('\n'), value["links"]["html"]["href"], value["created_on"])
      if value != None:
         pr = PullRequestDetails(value["author"]["display_name"], value["source"]["branch"]["name"], value["title"], value["description"].rstrip('\n'), value["links"]["html"]["href"], value["created_on"])
         pr_list.append(pr)      
   return pr_list

def list_pullrequest(access_token, workspace, repo, pull_request_id):
   url = "https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests/{}".format(workspace,repo, pull_request_id)

   headers = {
      "Accept": "application/json",
      "Authorization": "Bearer %s" % access_token
   }

   response = requests.get(
      url,
      headers = headers
   )

   value = _parse_response(response)
   if value != None:
      pr = PullRequestDetails(value["author"]["display_name"], value["source"]["branch"]["name"], value["title"], value["description"].rstrip('\n'), value["links"]["html"]["href"], value["created_on"])
      return pr

   return None