# python setup.py develop
from setuptools import setup


DISTNAME = "complex_number"

AUTHOR = "Enzo Baraldi"
# AUTHOR_EMAIL = ""

VERSION = "0.1.3"
ISRELEASED = True

DESCRIPTION = "This is a simple complex number python package."

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

URL = "https://github.com/Enzo1603/ComplexNumber"

CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Topic :: Software Development",
    "Operating System :: OS Independent",
]


KEYWORDS = ["python", "python 3.10", "complex number", "complex numbers", "complex operations"]
LICENSE = "MIT"


PYTHON_MIN_VERSION = "3.10"
# PYTHON_MAX_VERSION = "3.10"
# PYTHON_REQUIRES = f">={PYTHON_MIN_VERSION}, <= {PYTHON_MAX_VERSION}""
PYTHON_REQUIRES = f">={PYTHON_MIN_VERSION}"

INSTALL_REQUIRES = []

PACKAGES = [
    "complex_number",
    "tests",
]


def setup_package() -> None:
    setup(
        name=DISTNAME,
        version=VERSION,
        author=AUTHOR,
        # author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        url=URL,
        classifiers=CLASSIFIERS,
        packages=PACKAGES,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
        license=LICENSE,
    )


if __name__ == "__main__":
    setup_package()
