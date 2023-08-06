import setuptools

setuptools.setup(
    name="fedml_azure",
    version="2.0.0",
    author="SAP SE",
    description="A python library for building machine learning models on AzureML using a federated data source",
    license='Apache License 2.0',
    license_files = ['LICENSE.txt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "hdbcli","ruamel.yaml"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    package_data={'fedml_azure':['internal_config.json']},
    scripts=['src/fedml_azure/install_validate.sh', 'src/fedml_azure/kyma_deploy.sh'],
    include_package_data=True
)