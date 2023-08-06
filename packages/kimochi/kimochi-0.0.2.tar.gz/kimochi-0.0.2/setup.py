from setuptools import setup

readme = ""
with open("README.rst") as f:
    readme = f.read()
setup(
    name="kimochi",
    version="0.0.2",
    author="VarMonke",
    license="MIT",
    requires=["aiohttp"],
    packages=["kimochi"],
    python_requires=">=3.6",
    description="Express yourself with kimochi.",
    long_description=readme,
    long_description_content_type="text/x-rst",
)
