import os
import re
from pathlib import Path

from setuptools import find_packages, setup

NAME = "qc_utils"
PACKAGES = find_packages()
META_PATH = Path("qc_utils", "__init__.py")
PROJECT_URLS = {
    "Documentation": "https://qc-utils.readthedocs.io/en/latest/",
    "Source Code": "https://github.com/ENCODE-DCC/qc-utils",
    "Issue Tracker": "https://github.com/ENCODE-DCC/qc-utils/issues",
}
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
]
INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {"docs": ["sphinx"], "tests": ["pytest", "pytest-cov", "pytest-mock"]}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["docs"] + EXTRAS_REQUIRE["tests"] + ["pre-commit"]
)
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with Path(HERE, *parts).open(encoding="utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")
URL = find_meta("url")
LONG = read("README.rst")
DESCRIPTION = find_meta("description")
LICENSE = find_meta("license")
AUTHOR = find_meta("author")
EMAIL = find_meta("email")


setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG,
    long_description_content_type="text/x-rst",
    url=URL,
    project_urls=PROJECT_URLS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.5",
)
