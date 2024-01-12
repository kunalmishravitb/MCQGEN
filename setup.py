from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='kunal mishra',
    author_email='mishrakunal065@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages() # This method is responsible for finding local package from local directory
)