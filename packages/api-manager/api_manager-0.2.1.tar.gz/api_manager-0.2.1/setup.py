from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['requests', 'allure-python-commons', 'waiting']

setup(
    name="api_manager",
    version="0.2.1",
    author="Nikita Filonov",
    author_email="filonov.nikitkaa@gmail.com",
    description="Api Manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikita-Filonov/models_manager",
    packages=find_packages(),
    install_requires=requirements,
    package_data={'api_manager.templates': ['*.html']},
    include_package_data=False
)
