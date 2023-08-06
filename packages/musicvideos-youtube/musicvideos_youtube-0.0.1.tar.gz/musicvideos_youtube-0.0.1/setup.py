from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Library to upload videos to youtube.'

# Setting up
setup(
    name="musicvideos_youtube",
    version=VERSION,
    author="JustCow",
    author_email="<justcow@pm.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['oauth2client', 'google-api-python-client', 'google-auth-oauthlib', 'google-auth-httplib2'],
    keywords=['python', 'musicvideos', 'upload', 'youtube', 'justcow'],
    include_package_data=True ,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
