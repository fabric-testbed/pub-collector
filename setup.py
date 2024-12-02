from setuptools import find_packages, setup

setup(
    name="pub-collector",
    version="1.0",
    description="Collect FABRIC related publications from Google scholar",
    author="FABRIC team",
    url="https://github.com/fabric-testbed",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["scholarly"],
    platforms=["any"],
)
