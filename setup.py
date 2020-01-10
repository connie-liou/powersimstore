from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {

        'includes': [
            'cx_Logging', 'idna'
        ],
        'include_files':['assets/', 'Presets/', 'classes/'],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress', 'numpy', 'pandas'
        ],
        'excludes': ['tkinter']
    }
}

executables = [
    Executable('server.py',
               base='console',
               targetName='EPSDesignTool.exe')
]

setup(
    name='EPSDesignTool',
    packages=find_packages(),
    version='0.2.0',
    description='EPS Design Tool Beta',
    executables=executables,
    options=options
)