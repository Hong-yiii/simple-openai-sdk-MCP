#!/usr/bin/env python3
"""
Setup script for simple_mcp package.
"""

from setuptools import setup, find_packages

setup(
    name="simple_mcp",
    version="1.0.0",
    description="OpenAI Agent Demo with MCP Tools - Interactive Chat",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    author="MCP Demo",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "openai-agents>=0.1.0",
        "httpx>=0.24.0",
    ],
    include_package_data=True,
    package_data={
        "simple_mcp": ["config.json"],
    },
    entry_points={
        "console_scripts": [
            "simple-mcp=simple_mcp.demo:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 