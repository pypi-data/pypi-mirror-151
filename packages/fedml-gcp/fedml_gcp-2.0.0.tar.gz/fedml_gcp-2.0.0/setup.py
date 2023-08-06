#!/usr/bin/env python

import setuptools
setuptools.setup(
    name="fedml_gcp",
    version="2.0.0",
    author="SAP SE",
    description="A python library for building machine learning models on Google Cloud Platform using a federated data source",
    license='Apache License 2.0',
    license_files=['LICENSE.txt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "hdbcli",
        "google",
        "google-api-python-client",
        "google-cloud-aiplatform",
        "pyyaml",
        "requests"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    scripts=['src/fedml_gcp/build_and_push.sh',
             'src/fedml_gcp/install_kubectl.sh'],
    include_package_data=True
    # package_data={'fedml_gcp': ['internal_config.json']}
)
