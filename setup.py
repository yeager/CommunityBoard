from setuptools import setup, find_packages

setup(
    name="communityboard",
    version="1.0.0",
    description="Lokalt anslagstavla för funktionshinderrörelsen",
    author="CommunityBoard",
    license="GPL-3.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["PyGObject>=3.42"],
        package_data={
        "": ["locale/*/LC_MESSAGES/*.mo"],
    },
    entry_points={
        "console_scripts": [
            "communityboard=communityboard.app:main",
        ],
    },
)
