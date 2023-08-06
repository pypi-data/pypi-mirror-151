import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_jingdong",
    version="0.0.1",
    author="17TheWord",
    author_email="17theword@gmail.com",
    description="基于NoneBot2的京东查询插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/17TheWord/nonebot-plugin-jingdong",
    project_urls={
        "Bug Tracker": "https://github.com/17TheWord/nonebot-plugin-jingdong",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['nonebot_plugin_jingdong'],
    python_requires=">=3.8",
    install_requires=[
        'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
        'nonebot2>=2.0.0-beta.1,<3.0.0',
        'bs4==0.0.1',
        'httpx==0.22.0',
        'lxml==4.8.0',
    ],
)
