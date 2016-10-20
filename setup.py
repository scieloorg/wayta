import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'elasticsearch>=1.1.1',
    'pyramid>=1.5.2',
    'pyramid_chameleon>=0.3',
    'pyramid_debugtoolbar>=2.1'
]

setup(name='wayta',
      version='1.2.1',
      description='A tool to suggest the name of an institution or country in the original form and language.',
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
      entry_points="""\
      [paste.app_factory]
      main = wayta:main
      [console_scripts]
      wayta_loaddata=processing.loaddata:main
      """,
      )
