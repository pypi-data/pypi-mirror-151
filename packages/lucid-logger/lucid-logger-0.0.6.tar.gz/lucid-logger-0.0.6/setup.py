import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lucid-logger",
    version="0.0.6",
    author="Kevin Lago",
    author_email="kevinthelago@gmail.com",
    description="Python Logging Library with Loading Bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kevin-Lago/LucidLogger",
    project_urls={
        "Bug Tracker": "https://github.com/Kevin-Lago/LucidLogger/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)