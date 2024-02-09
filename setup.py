from setuptools import setup, find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(
    name='streamlit_exp',
    version="0.0.2",
    description="Description",
    packages=find_packages(),
    install_requires=requirements,
    author='Jan du Plessis',
    author_email='drjanduplessis@icloud.com'
)
