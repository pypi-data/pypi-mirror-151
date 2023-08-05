from setuptools import setup

setup(
    name="pb-nbss-upload",
    version="0.1",
    url="http://127.0.0.1:8000",
    description="Upload notebooks to Private cloud",
    license="3-clause BSD",
    author="AbhishekJadhav-RamandeepMakkar",
    author_email="abhicjadhav@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["nbss_upload"],
    entry_points = {
        'console_scripts': ['pb-nbss-upload=nbss_upload:main'],
    },
    install_requires=["requests"],
    platforms="any",
    zip_safe=False,
)
