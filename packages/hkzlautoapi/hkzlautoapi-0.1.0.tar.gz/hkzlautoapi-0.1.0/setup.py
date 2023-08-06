import setuptools
from setuptools import setup

# with open("README.md", "r", encoding="utf-8") as f:
#     long_description = f.read()

setup(
    name="hkzlautoapi",
    version= "0.1.0",
    keywords=["接口自动化","pytest"],
    description="封装了pytest+request+excel数据驱动接口自动化框架",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="郑珊珊",
    author_email="zheng11071107@qq.com",
    url="http://10.0.40.18:8888/root/automated-testing", # github项目连接
    license="MIT License", #
    packages=setuptools.find_packages(),
    install_requires=[ # 依赖包
        "pandas", # panda包存在即可
        "numpy >= 1.0", # numpy包要求版本 >1.0
        "pymongo",#本人用的4.1.1
        "allure-python-commons",#本人用的2.9.45
        "allure-pytest",#本人用的2.9.45
        "paho-mqtt",#本人用的1.6.1
        "pytest",
        "pytest-base-url",
        "pytest-forked",
        "pytest-html",
        "pytest-metadata",
        "pytest-ordering",
        "requests",
        "urllib3",
        "xlrd == 1.2", #版本有要求，大于1.2版本可能有问题
        "xlwt == 1.3"
        ],
    classifiers=[ # 其他配置项
        "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 2", # 注意现在的项目当有依赖包时支持python2是很危险的，不建议这样
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
    # package_data={ # 配置除了python代码外的其他数据、文件，会一起打包
    #     # '项目文件目录': ['data.csv','*.pkl'],
    # }
)



