from setuptools import setup, find_packages
from typing import List

#Declaring Variables for setup function
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Somesh Trivedi"
DESCRIPTION="This a ML Project"
REQUIREMENTS_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:
    """Description: This function is going to return list of requirement
        mentioned in requirement.txt file
        
        return This function is going to return a list which contains name of libraries
        mentioned in requirements.txt file
        """
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)
