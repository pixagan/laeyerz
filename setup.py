from setuptools import setup, find_packages

setup(
    name="laeyerz",
    version="1.0", 
    author="Anil Variyar",
    author_email="pixagan@gmail.com",
    description="Building Graph based Works, AI Workflow, RAG and AI Agents",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/pixagan/laeyerz",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="ai agents workflow rag llm graph",
    license="Apache License 2.0",
    python_requires=">=3.8",  # Minimum Python version required
    project_urls={
    "Source": "https://github.com/pixagan/laeyerz",
    "Documentation": "https://laeyerz.com",
}
)
