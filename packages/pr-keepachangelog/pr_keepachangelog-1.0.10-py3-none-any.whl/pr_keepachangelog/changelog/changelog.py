import keepachangelog
import os
import os.path
from collections import defaultdict
from .enums import Categories

CHANGELOG_FILE = "CHANGELOG.md"

def _overwrite_file(buf, FILE_NAME):
    with open(FILE_NAME, "w") as out_file:
        out_file.write(buf)

def _unreleased_remove_hotfix(changes, bugfixed_values):
    unreleased = changes[Categories.unreleased.value]
    if len(bugfixed_values) > 0:
        unreleased[Categories.fixed.value] = bugfixed_values
    else:
        del unreleased[Categories.fixed.value]
    return unreleased

def _add_hotfix_only(changes, hotfixed_values):
    changes[Categories.unreleased.value] = {
        Categories.fixed.value: hotfixed_values,
        Categories.metadata.value: changes[Categories.unreleased.value][Categories.metadata.value]
    }
    # write file with hotfix
    _overwrite_file(keepachangelog.from_dict(changes), CHANGELOG_FILE)

def _add_unreleased(unreleased):
    changes = keepachangelog.to_dict(CHANGELOG_FILE, show_unreleased=True)
    changes = defaultdict(dict, changes)
    # add unreleased to file
    changes[Categories.unreleased.value] = unreleased

    _overwrite_file(keepachangelog.from_dict(changes), CHANGELOG_FILE)

def add_value_to_category_release(category, value, release_version="-1"):
    changes = keepachangelog.to_dict(CHANGELOG_FILE, show_unreleased=True)
    changes = defaultdict(dict, changes)
    if release_version.startswith("-"):
        release_version = list(changes.keys())[-int(release_version)]
    print("added to version:", release_version)
    if release_version in changes:
        # if key exists, append, else create array with entry
        if category in changes[release_version].keys():
            changes[release_version][category].append(value)
        else:
            changes[release_version][category] = [value]

        _overwrite_file(keepachangelog.from_dict(changes), CHANGELOG_FILE)
    else:
        print("version not found")

def add_value_to_category_unreleased(category, value):
    add_value_to_category_release(category, value, Categories.unreleased.value)

def make_release():
    # check if there is hotfix, then release
    changes = keepachangelog.to_dict(CHANGELOG_FILE, show_unreleased=True)
    changes = defaultdict(dict, changes)

    if Categories.fixed.value in changes[Categories.unreleased.value].keys():
        fixed_values = changes[Categories.unreleased.value][Categories.fixed.value]

        hotfixed_values = list(filter(lambda x: x.find("[hotfix/") != -1, fixed_values))
        bugfixed_values = list(filter(lambda x: x.find("[hotfix/") == -1, fixed_values))

        if len(hotfixed_values) > 0:
            print("hotfix found")
            # save bugfix and other stuff in unreleased
            unreleased = _unreleased_remove_hotfix(changes, bugfixed_values)

            # release hotfix only
            _add_hotfix_only(changes, hotfixed_values)
            new_version = keepachangelog.release(CHANGELOG_FILE)

            # add back bugfixes
            print("adding back other stuff, you can release again")
            _add_unreleased(unreleased)
        else:
            # no bugfix or hotfix found
            new_version = keepachangelog.release(CHANGELOG_FILE)
    # no fixes
    else:
        new_version = keepachangelog.release(CHANGELOG_FILE)

    if new_version != None:
        print("released version {}".format(new_version))
        # place new_version somewhere! e.s. environment variable
    else:
        print("no updates")

# def main():
#     add_value_to_category(Categories.added, "tester")

# if __name__ == "__main__":
#     main()