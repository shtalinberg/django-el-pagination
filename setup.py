import os
from distutils.core import setup

PROJECT_NAME = 'el_pagination'
ROOT = os.path.abspath(os.path.dirname(__file__))
VENV = os.path.join(ROOT, '.venv')
VENV_LINK = os.path.join(VENV, 'local')

install_requires = [
    'django>=1.11.0',
]

project = __import__(PROJECT_NAME)

root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))


def read(filename):
    return open(os.path.join(ROOT, filename)).read()


class VenvLinkDeleted(object):

    restore_link = False

    def __enter__(self):
        """Remove the link."""
        if os.path.islink(VENV_LINK):
            os.remove(VENV_LINK)
            self.restore_link = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore the link."""
        if self.restore_link:
            os.symlink(VENV, VENV_LINK)


with VenvLinkDeleted():
    setup(
        name='django-el-pagination',
        version=project.get_version(),
        description=(
            "Django pagination tools supporting Ajax, multiple and lazy "
            "pagination, Twitter-style and Digg-style pagination."
        ),  # project.__doc__,
        long_description=read('README.rst'),
        author='Oleksandr Shtalinberg',
        author_email='O.Shtalinberg@gmail.com',
        url='http://github.com/shtalinberg/django-el-pagination',
        keywords='django endless pagination ajax',
        packages=[
            PROJECT_NAME,
            '{0}.templatetags'.format(PROJECT_NAME),
            '{0}.tests'.format(PROJECT_NAME),
            '{0}.tests.integration'.format(PROJECT_NAME),
            '{0}.tests.templatetags'.format(PROJECT_NAME),
        ],
        package_data={PROJECT_NAME: data_files},
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Utilities',
        ],
        install_requires=install_requires,
    )
