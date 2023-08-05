from dateutil.parser import parse
from .enums import *
from ..changelog.enums import *

class PullRequestDetails():
   def __init__(self, author, branch_name, title, description, link, created_on):
      self.author = author
      self.branch_name = branch_name
      self.title = title
      self.description = description
      self.link = link
      self.created_on = parse(created_on)

   def format_date(self, date_to_format):
      return date_to_format.strftime("%Y-%m-%d %H:%M")

   @staticmethod
   def get_sub_category(branch_trimmed_name):
      if branch_trimmed_name.startswith(BranchDetails.DEPRECATED.value):
         return Categories.deprecated
      elif branch_trimmed_name.startswith(BranchDetails.CHANGED.value):
         return Categories.changed
      elif branch_trimmed_name.startswith(BranchDetails.REMOVED.value):
         return Categories.removed
      elif branch_trimmed_name.startswith(BranchDetails.SECURITY.value):
         return Categories.security
      return None

   def get_category(self):
      if self.branch_name.startswith(BranchTypes.RELEASE.value):
         return None
      elif self.branch_name.startswith(BranchTypes.HOTFIX.value):
         return Categories.fixed
      elif self.branch_name.startswith(BranchTypes.FEATURE.value):
         return Categories.added
      elif self.branch_name.startswith(BranchTypes.BUGFIX.value):
         return Categories.fixed
      # additional branch types
      elif self.branch_name.startswith(BranchTypes.DEPRECATED.value):
         return Categories.derecated
      elif self.branch_name.startswith(BranchTypes.CHANGED.value):
         return Categories.changed
      elif self.branch_name.startswith(BranchTypes.REMOVED.value):
         return Categories.removed
      elif self.branch_name.startswith(BranchTypes.SECURITY.value):
         return Categories.security

   def __repr__(self):
      return """{title} from {author} at {created_on} on [{branch_name}]({link})""".format(author=self.author, branch_name=self.branch_name, title=self.title, description=self.description, link=self.link, created_on=self.format_date(self.created_on))