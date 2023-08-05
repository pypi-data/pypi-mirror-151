from enum import Enum

class PullRequestState(Enum):
   MERGED = "MERGED"
   SUPERSEDED = "SUPERSEDED"
   OPEN = "OPEN"
   DECLINED = "DECLINED"

class BranchTypes(Enum):
   RELEASE = "release/"
   HOTFIX = "hotfix/"
   FEATURE = "feature/"
   BUGFIX = "bugfix/"
   # additional branch types
   DEPRECATED = "deprecated/"
   CHANGED = "changed/"
   REMOVED = "removed/"
   SECURITY = "security/"