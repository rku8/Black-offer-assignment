from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blackoffer project",
    version="0.0.1",
    description="This is a blackoffer project structure",
    long_description=long_description,
    author="Ravi Kumar",
    author_email="ravikumar46931@gmail.com",
    packages=find_packages(),
    install_requires=[  # List your project's dependencies
        "numpy",  # Example: replace with your actual dependencies
        "pandas",
        # Add other dependencies here
    ],
    include_package_data=True,
)
