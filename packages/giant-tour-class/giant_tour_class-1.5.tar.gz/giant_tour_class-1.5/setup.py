from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description=fh.read()
setup(
    name="giant_tour_class",
    version="1.5",
    description="giant tour class",
    py_modules=["GiantTour"],
    package_dir={"": "src"},
    # classifiers=[
    #         "Programming Language :: Python :: 2.7",
    #         "License :: OSI Approved :: MIT License",
    # ],
    # long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ortools", "kmedoids"],
    license="LICENSE.txt",
    author="Mr. Hanh",
)