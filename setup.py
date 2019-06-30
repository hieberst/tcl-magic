from setuptools import setup

setup(
    name='tcl-magic',
    version='0.0.2',
    description='An IPython extension for Tcl.',
    long_description= open('README.md').read(),
    author='Steffen Hieber',
    author_email='hieber_steffen@web.de',
    url='https://github.com/hieberst/tcl-magic',
    license='MIT',
    keywords="ipython notebook tcl",
    py_modules=['tclmagic'],
    install_requires=['ipython'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
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
