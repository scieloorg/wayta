import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
]

tests_requires = [
    'mocker'
]

setup(name='wayta',
      version='0.0',
      description='wayta',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='SciELO',
      author_email='tecnologia@scielo.org',
      url='http://docs.scielo.org',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      setup_requires=["nose>=1.0", "coverage"],
      tests_require=tests_requires,
      test_suite="nose.collector",
      entry_points="""\
      [paste.app_factory]
      main = wayta:main
      """,
      )
