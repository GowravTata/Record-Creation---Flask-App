# Third Party Library
from setuptools import find_packages, setup

setup(
    name="app",
    version="0.1.0",
    author="Gowrav Tata",
    author_email="gowravsaitata@gmail.com",
    python_requires="~=3.8",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: SysAdmins",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
