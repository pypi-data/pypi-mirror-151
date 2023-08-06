from setuptools import setup

with open("README.md", "r") as fh:
    long_description=fh.read()
setup(
    name="SMLGT",
    version="0.1",
    description="create giant tour",
    py_modules=["GiantTour"],
    package_dir={"": "src"},
    classifiers=[
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ortools", "kmedoids"],
    license="LICENSE.txt",
    author="Mr. Hanh",
)