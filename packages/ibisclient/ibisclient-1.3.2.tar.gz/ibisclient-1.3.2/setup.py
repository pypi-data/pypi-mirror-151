"""
Lookup/Ibis web service API

Python installation.
"""

from setuptools import setup

setup(
    name="ibisclient",
    version="1.3.2",
    description="Lookup API client",
    license="LGPL",
    url="https://www.lookup.cam.ac.uk/doc/ws-doc/",
    packages=["ibisclient"],
    package_dir={"ibisclient": "src/python3/ibisclient"},
    install_requires=[
        "requests~=2.26",
    ]
)
