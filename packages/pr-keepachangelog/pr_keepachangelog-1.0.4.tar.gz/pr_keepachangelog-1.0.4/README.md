### Documentation
The package can be installed with `pip install pr-keepachangelog`.
For help and to use it: `python -m pr_keepachangelog`.

Based on a pull request that is merged on a certain branch, you can populate the changelog automatically. The category in which the changelog is populated depends on the prefix of the specified branch:
- hotfix/ -> Fixed
- feature/ -> Fixed
- bugfix/ -> Fixed
# additional branch types
- deprecated/ -> Deprecated
- changed/ -> Changed
- removed/ -> Removed
- security/ -> Security

### Keepachangelog categories
Keepachangelog will guess the new version number when you make a release with `--release`:
- Added: for new features. Results in minor update.
- Changed: for changes in existing functionality. Results in major update.
- Deprecated: for soon-to-be removed features. Results in major update.
- Removed: for now removed features. Results in major update.
- Fixed: for any bug fixes (hotfix/bugfix). Results in patch update.
- Security: in case of vulnerabilities. Results in patch update.