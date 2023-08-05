# @author Luca Attanasio
import os
from .api.bitbucket_api import *
from .changelog.changelog import *
import argparse
import sys

def _get_access_token(client_id, secret):
   return auth(client_id, secret)["access_token"]

def list_pr_details(client_id, secret, workspace, repo):
   # get access token
   access_token = _get_access_token(client_id, secret)
   # proceed
   if access_token != None:
      print("auth ok")
      prs = list_pullrequests(access_token, workspace, repo)
      for pr in prs:
         print(pr)
   else:
      print("auth error")

def add_pr_details(client_id, secret, workspace, repo, pr_id, last_version=None):
   # get access token
   access_token = _get_access_token(client_id, secret)
   # proceed
   if access_token != None:
      print("auth ok")
      pr = list_pullrequest(access_token, workspace, repo, pr_id)
      if pr != None:
         print(pr.get_category(), ": " + repr(pr))
         if last_version != None:
            add_value_to_category_release(pr.get_category().value, repr(pr), last_version)
         else:
            add_value_to_category_unreleased(pr.get_category().value, repr(pr))
   else:
      print("auth error")

def main():
   parser = argparse.ArgumentParser(description='Add pull requests to changelog automatically with BitBucket pipelines and release changelog with keepachangelog.')
   # options
   parser.add_argument('--add-pull-request', help="adds the pipeline pull request to unreleased in CHANGELOG.md", action='store_true')
   parser.add_argument('--list-pull-requests', help="list the latest pull requests", action='store_true')
   parser.add_argument('--fix-release', nargs="?", const="-1", help="adds the pipeline pull request to the release in CHANGELOG.md (there should be only bufxies/hotfixes found after testing). Use -1 to get last release (-n to get older ones)", type=str)
   parser.add_argument('--release', help="release the CHANGELOG.md", action='store_true')
   # config
   parser.add_argument('--client-id', help="BitBucket client identifier", type=str, required='--release' not in sys.argv)
   parser.add_argument('--secret', help="BitBucket secret", type=str, required='--release' not in sys.argv)
   parser.add_argument('--workspace', help="BitBucket workspace", type=str, required='--release' not in sys.argv)
   parser.add_argument('--repo', help="BitBucket Repository", type=str, required='--release' not in sys.argv)
   parser.add_argument('--pr-id', help="Pull Request identifier", type=int, required='--add-pull-request' in sys.argv or '--fix-release' in sys.argv)

   args = parser.parse_args()

   if args.client_id and args.secret and args.workspace and args.repo:
      if args.add_pull_request and args.pr_id:
         print("adding pr to changelog...")
         add_pr_details(args.client_id, args.secret, args.workspace, args.repo, args.pr_id)
      elif args.list_pull_requests:
         print("listing prs...")
         list_pr_details(args.client_id, args.secret, args.workspace, args.repo)
      elif args.fix_release and args.pr_id:
         print("adding pr to changelog on {}...".format(args.fix_release))
         add_pr_details(args.client_id, args.secret, args.workspace, args.repo, args.pr_id, args.fix_release)
      else:
         parser.print_help()
   else:
      if args.release:
         print("attempt to release...")
         make_release()
      else:
         parser.print_help()

if __name__ == "__main__":
   main()