from enum import Enum

class Categories(Enum):
    unreleased = "unreleased"
    uncategorized = "uncategorized"
    metadata = "metadata"
    added = "added" # feature release
    fixed = "fixed" # if it is the only section, patch is incremented
    ## other stuff which may be used
    deprecated = "deprecated" # deprecate feature
    changed = "changed" # breaking change (major update)
    removed = "removed" # breaking change (major update)
    security = "security" # increased security