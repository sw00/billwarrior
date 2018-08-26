import os

from setuptools import setup

CONFIG_DIR = os.path.join(os.getenv("HOME"), ".config", "billwarrior")
print("CONFIG_DIR: %s" % CONFIG_DIR)


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="billwarrior",
    version="0.1.0",
    description="A Timewarrior report extension for creating invoices in LaTeX.",
    long_description=readme(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="timewarrior timesheet invoice freelance contract report",
    url="http://github.com/sw00/billwarrior",
    author="Sett Wai",
    author_email="exec@sett.sh",
    license="GPLv3",
    packages=["billwarrior"],
    install_requires=["timew-report==1.0.2"],
    scripts=["bin/billwarrior"],
    data_files=[
        (CONFIG_DIR, ["etc/billwarrior.ini"]),
        (os.path.join(CONFIG_DIR, "latex"), ["etc/latex/invoice.cls", "etc/latex/invoice.tex"]),
    ],
    zip_safe=False,
)
