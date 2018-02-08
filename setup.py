from setuptools import setup, find_packages

setup(name='parallelcorpora',
      version='0.1',
      description='Extention for Lingcorpora with parallel corpora',
      long_description='Includes ru-pol corpus. Is able to represent the output data in kwic format.',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='linguistics corpora parallel kwic',
      url='https://github.com/maria-terekhina/parallelcorpora',
      author='Maria Terekhina',
      author_email='maria.myslina@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'lingcorpora', 'nltk', 'bs4', 'requests', 're'
      ],
      include_package_data=True,
      zip_safe=False)