import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "smtp-credentials-cdk-construct",
    "version": "2.0.0",
    "description": "A CDK construct that creates SMTP credentials permitting emails to be sent via SES.",
    "license": "MIT",
    "url": "https://github.com/charlesdotfish/smtp-credentials-cdk-construct",
    "long_description_content_type": "text/markdown",
    "author": "Charles Salmon<me@charles.fish>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/charlesdotfish/smtp-credentials-cdk-construct"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "smtp_credentials",
        "smtp_credentials._jsii"
    ],
    "package_data": {
        "smtp_credentials._jsii": [
            "smtp-credentials-cdk-construct@2.0.0.jsii.tgz"
        ],
        "smtp_credentials": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.59.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
