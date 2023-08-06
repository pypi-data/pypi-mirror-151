from setuptools import setup, find_packages


setup(
    name='ECS Client',
    version='1.0',
    license='MIT',
    author="Steven Guerrero",
    author_email='imstevenguerrero@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/iStevenGuerrero/ecs_client',
    keywords='ecs client',
    install_requires=[
          'scikit-learn',
      ],

)