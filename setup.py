import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    all_lines = f.read().split("\n")
    requirements = [line for line in all_lines if "@" not in line]
    requirements_git = [
        line.replace("-e", line.split("=")[-1] + " @")
        for line in all_lines
        if "@" in line
    ]
    requirements += requirements_git

setuptools.setup(
    name="wenet_realtime",
    version="1.1.0",
    author="Idiap - William Droz",
    author_email="william.droz@idiap.ch",
    description="Realtime APIs for the Wenet project (personal context builder component)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=requirements,
)
