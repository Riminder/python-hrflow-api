from setuptools import setup

setup(name='hrflow',
      version='1.5.2',
      description='python hrflow api package',
      url='https://github.com/hrflow/python-hrflow-api',
      author='riminder',
      author_email='contact@rimider.net',
      license='MIT',
      packages=['hrflow'],
      install_requires=[
          'requests',
          'python-magic'
      ],
      python_requires='>=3.5',
      zip_safe=False)
