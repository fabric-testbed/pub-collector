from setuptools import find_packages, setup

setup(
    name="google-scholar-pub-tracker",
    version="1.0",
    description="Track FABRIC citations from Google scholar",
    author="FABRIC team",
    url="https://github.com/fabric-testbed",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requirements=["scholarly"],
    platforms=["any"],
)
