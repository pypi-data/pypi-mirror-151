import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloud-downloader-equitania",
    version="0.0.4",
    author="Equitania Software GmbH",
    author_email="info@equitania.de",
    description="A package to download files from cloud services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['cloud_downloader'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
    [console_scripts]
    cloud-download=cloud_downloader.cloud_downloader:start_cloud_downloader
    ''',
    install_requires=[
        'click>=8.1.3',
        'requests>=2.22.0'
    ]
)