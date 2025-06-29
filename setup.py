from setuptools import setup, find_packages

setup(
    name='bark_python',
    version='0.0.2',
    description='Bark encrypted push client',
    long_description=open('README.md', encoding='utf-8').read(),  # 读取 README 作为描述
    long_description_content_type='text/markdown',
    author='horennel',
    author_email='nelsonhoren@gmail.com',
    url='https://github.com/horennel/bark-python',
    packages=['bark_python'],
    install_requires=[
        'requests~=2.32.4',
        'pycryptodome~=3.23.0',
    ],
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    include_package_data=True,
    zip_safe=False,
)
