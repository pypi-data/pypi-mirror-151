from setuptools import setup, find_packages

setup(
    name="vais-frontend",
    version="20220519051104",
    description="The VAIS frontend",
    url="https://github.com/Vioneta/vais-frontend",
    author="Vioneta (Pvt) Ltd",
    author_email="admin@vioneta.com",
    packages=find_packages(include=["vais_frontend", "vais_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)