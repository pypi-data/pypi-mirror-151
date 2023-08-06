from setuptools import setup, find_packages


def get_file_content_as_list(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        content = [line.strip() for line in file]
    return content


def get_file_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


packages = find_packages()
VERSION = get_file_content("refdatatypes/VERSION")
DOCUMENTATION_MD = get_file_content("README.md")

setup(
    name="refdatatypes",
    version=VERSION,
    license='MIT',
    author='Ales Adamek',
    author_email='alda78@seznam.cz',
    description='Pyton basic datatypes as a references.',
    long_description=DOCUMENTATION_MD,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/alda78/refdatatypes",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=[],
    include_package_data=True,  # MANIFEST.in
    zip_safe=False,  # aby se spravne vycitala statika pridana pomoci MANIFEST.in
)
