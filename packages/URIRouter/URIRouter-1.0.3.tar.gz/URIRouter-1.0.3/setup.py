import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
__version__ = "1.0.3"


setup(
    name="URIRouter",
    version=__version__,
    description="Flask-style routing for URIs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/The-Nicholas-R-Barrow-Company-LLC/uri-router",
    author="The Nicholas R. Barrow Company, LLC",
    author_email="me@nicholasrbarrow.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["urirouter"],
    package_data={},
    include_package_data=True,
    install_requires=[],
    project_urls={
        'Source': 'https://github.com/The-Nicholas-R-Barrow-Company-LLC/uri-router',
        'Tracker': 'https://github.com/The-Nicholas-R-Barrow-Company-LLC/uri-router/issues',
    }
        # 'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
)