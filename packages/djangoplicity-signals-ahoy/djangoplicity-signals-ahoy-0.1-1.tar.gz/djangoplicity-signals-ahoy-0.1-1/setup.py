from setuptools import setup, find_packages

version = __import__('signals_ahoy').__version__

setup(
    name = 'djangoplicity-signals-ahoy',
    version = version,
    description = "signals-ahoy",
    long_description = """Djangoplicity Signals Ahoy provides very useful common signals for larger Django applications.""",
    author = 'Bruce Kroeze',
    author_email = 'brucek@ecomsmith.com',
    url = 'https://github.com/djangoplicity/djangoplicity-signals-ahoy/',
    download_url = 'https://github.com/djangoplicity/djangoplicity-signals-ahoy/archive/refs/tags/0.1.1.tar.gz',
    license = 'New BSD License',
    platforms = ['any'],
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Framework :: Django'],
    packages = find_packages(),
    include_package_data = True,
)
