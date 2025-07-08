from setuptools import setup, find_packages

setup(
    name="cybercli",
    version="0.1.0",
    description="Una herramienta CLI para la gestión remota de clientes en un entorno de ciberseguridad.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="CyberCLI Team",
    author_email="contact@cybercli.example",
    url="https://github.com/tu_usuario/cybercli",
    packages=find_packages(),
    install_requires=[
        "cmd2==2.4.3",
        "rich==13.7.1",
        "lark==1.1.9",
        "colorama==0.4.6",
        "cryptography==42.0.5",
    ],
    entry_points={
        "console_scripts": [
            "cybercli = main:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)