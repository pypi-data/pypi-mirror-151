from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(name='lightgrid',
      version='2.0.5',
      keywords=("light", "grid","gridsearch","param","parameter"),   
      description='A Fast model parameter adjustment tool',
      long_description =long_description, 
      long_description_content_type="text/markdown",
      author='shuwei Yan',
      author_email='yan_shw@dlmu.edu.cn',
      include_package_data=True,
      platforms="any",
      license='MIT',
      packages= find_packages(),
      zip_safe=False, install_requires=[],
      python_requires=">=3.5",
      )