import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "perovskite_intercalation",
    version = "0.1.2",
    author = "Kevin Whitham",
    author_email = "kevin.whitham@gmail.com",
    description = "Routines to create intercalated perovskite crystals",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kevinwhitham/perovskite_intercalation",
    install_requires=["ase>=3.21.1",
                      "pymatgen>=2022.0.5",
                      "networkx>=2.5",
                      "numpy>=1.20.2",
                      "matplotlib>=3.4.1",
                      "pillow>=8.1.2"],
    classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: OS Independent",
    ],

    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3",
)

