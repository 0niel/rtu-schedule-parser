import os
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r") as f:
    readme = f.read()


requires = [
    "openpyxl>=3.0.4",
    "requests>=6.7",
    "beautifulsoup4==4.11.1",
    "openpyxl>=2.5.8",
    "pandas>=1.4.3",
    "xls2xlsx==0.1.5",
    "currency-symbols==1.0.0",
]


def setup_package():
    metadata = dict(
        name="rtu-schedule-parser",
        version="0.2.0",
        description="Easy extraction of the MIREA - Russian Technological University schedule from Excel documents.",
        long_description=readme,
        author="Oniel (Sergey Dmitriev)",
        long_description_content_type="text/markdown",
        url="https://github.com/mirea-ninja/rtu-schedule-parser",
        license="MIT License",
        packages=find_packages(exclude=("tests",)),
        install_requires=requires,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.`0`",
        ],
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
