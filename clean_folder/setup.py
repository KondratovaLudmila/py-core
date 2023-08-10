from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_01',
    version='0.0.1',
    description='It will sort your unsorted files',
    url='http://github.com/dummy_user/useful',
    author='Kondratova Ludmila',
    author_email='kondratova.l.a@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)