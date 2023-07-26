# Third Party Library
from setuptools import find_packages, setup

setup(
    name="app",
    version="0.1.0",
    description="Service responsible for generating business logic data in dashboard",
    author="Gowrav Tata",
    author_email="gowravsaitata@gmail.com",
    license="SKY",
    url="https://scm.isp.sky.com/network-automation/components/analytics-and-reporting/dataflow-automation",
    python_requires="~=3.8",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: SysAdmins",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
