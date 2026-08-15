from setuptools import setup, find_packages
from pathlib import Path

def read_requirements():
    """Read dependencies from requirements.txt."""
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        return []
    
    with requirements_path.open("r", encoding="utf-8") as req_file:
        return [
            line.strip()
            for line in req_file
            if line.strip() and not line.strip().startswith("#")
        ]

def read_long_description():
    """Read project description from README.md."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        return ""
    
    return readme_path.read_text(encoding="utf-8")

setup(
    name="ChatBot Assistant",
    version="0.1.0",
    packages=find_packages(exclude=["tests*", "docs*", "notebooks*"]),
    install_requires=read_requirements(),
    python_requires=">=3.10",
    author="Hanie Fazli",
    description="A RAG-based assistant to answer knowledgebase-related questions",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
)
