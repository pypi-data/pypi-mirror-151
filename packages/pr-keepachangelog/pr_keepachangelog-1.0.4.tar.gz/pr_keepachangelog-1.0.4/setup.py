import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pr_keepachangelog",
    version="1.0.4",
    description="Add pull requests to changelog automatically with BitBucket pipelines and release changelog with keepachangelog.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/blackwiz4rd/pr-keepachangelog",
    author="blackwiz4rd",
    author_email="blackwiz4rd@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    packages=(
        find_packages() +
        find_packages(where="./api") +
        find_packages(where="./changelog")
    ),
    include_package_data=True,
    install_requires=["keepachangelog==2.0.0.dev2", "requests", "python-dateutil"],
    entry_points={
        "console_scripts": [
            "pr_keepachangelog=pr_keepachangelog.__main__:main",
        ]
    },
)