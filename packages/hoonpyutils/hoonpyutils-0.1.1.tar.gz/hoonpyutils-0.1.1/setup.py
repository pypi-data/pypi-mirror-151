from setuptools import setup
from setuptools import find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hoonpyutils',
    version='0.1.1',
    author='NeoHoon',
    author_email='hoon.paek@neoplatform.net',
    description='Hoon Python Utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/neohoon/hoonpyutils',
    download_url='https://github.com/neohoon/hoonpyutils/archive/master.zip',
    # 해당 패키지를 사용하기 위해 필요한 패키지를 적어줍니다. ex. install_requires= ['numpy', 'django']
    # 여기에 적어준 패키지는 현재 패키지를 install할때 함께 install됩니다.
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['hoon python utilities'],
    # 해당 패키지를 사용하기 위해 필요한 파이썬 버전을 적습니다.
    python_requires='>=3.6',
    # 파이썬 파일이 아닌 다른 파일을 포함시키고 싶다면 package_data에 포함시켜야 합니다.
    package_data={},
    # 위의 package_data에 대한 설정을 하였다면 zip_safe설정도 해주어야 합니다.
    zip_safe=False,
    # PyPI에 등록될 메타 데이터를 설정합니다.
    # 이는 단순히 PyPI에 등록되는 메타 데이터일 뿐이고, 실제 빌드에는 영향을 주지 않습니다.
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

'''
import setuptools
import shutil
import os

os.makedirs("temp")
shutil.move("smartxpyutils/.git", "temp")
shutil.move("smartxpyutils/.idea", "temp")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartxpyutils",
    version="0.2.0",
    author="HOON PAEK",
    author_email="hoon.paek@gmail.com",
    description="Smart X Python Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neohoon/smartxpyutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

shutil.move("temp/.git", "smartxpyutils")
shutil.move("temp/.idea", "smartxpyutils")
os.rmdir("temp")
'''
