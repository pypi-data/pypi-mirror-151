import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bashtable",
    version="1.0.2",
    author="Bash Elliott",
    author_email="spicethings9@gmail.com",
    description="Table package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rackodo/bashtable",
    project_urls={
        "Bug Tracker": "https://github.com/rackodo/bashtable/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=['bashtable'],
    package_dir={"bashtable": "src"},
    package_data={'bashtable': ['']},
    python_requires=">=3.6",

    include_package_data=True
)
