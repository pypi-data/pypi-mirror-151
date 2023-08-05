from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    'mecab-python3==1.0.1',
    'unidic-lite==1.0.7',
]

setup(name='util_ds',
      version='0.5.3',
      description="This project is a convenient part of the NLP project, including several already exposed projects such as summy and text processing.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Sohone Guo',
      author_email='878153077@qq.com',
      packages=find_packages(),
      license='MIT',
      install_requires=requirements,
      zip_safe=False)
