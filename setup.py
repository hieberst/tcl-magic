from setuptools import setup

setup(
    name='tcl-magic',
    version='0.0.5',
    description='An IPython extension for Tcl.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Steffen Hieber',
    author_email='hieberst@gmx.de',
    url='https://github.com/hieberst/tcl-magic',
    license='MIT',
    keywords="ipython notebook tcl",
    py_modules=['tclmagic'],
    install_requires=['ipython'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Tcl',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
