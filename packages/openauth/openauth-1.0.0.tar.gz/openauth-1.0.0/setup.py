import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openauth",
    version="1.0.0",
    author="Py Bash",
    description="OpenAuth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pybash1/openbase",
    project_urls={
        "Bug Tracker": "https://github.com/pybash1/openbase/issues"
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Database",

    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
