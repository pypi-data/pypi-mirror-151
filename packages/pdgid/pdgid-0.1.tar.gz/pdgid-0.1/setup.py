from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="pdgid",
    version="0.1",
    description="Command-line tool to get the name of a particle given its PDGID (and vice versa).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kiran Ostrolenk",
    author_email="kostrolenk@gmail.com",
    url="https://gitlab.com/cardboardturkey/pdgid",
    packages=["pdgid"],
    package_dir={"pdgid": "pdgid"},
    package_data={"pdgid": ["data/*.json"]},
    entry_points={
        "console_scripts": ["pdgid=pdgid.pdgid:main"],
    },
    extras_require={
        "test": [
            "black",
            "pylint",
            "pytest",
            "pytest-xdist",
            "types-setuptools",
            "mypy",
        ]
    },
)
