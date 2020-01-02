from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {

        'includes': [
            'cx_Logging', 'idna'
        ],
        'include_files':['assets/', 'Presets/', 'classes/'],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress'
        ],
        'excludes': ['tkinter']
    }
}

executables = [
    Executable('server.py',
               base='console',
               targetName='PowerSimApp.exe')
]

setup(
    name='PowerSimulationTool',
    packages=find_packages(),
    version='0.4.0',
    description='Power Simulation Tool 2019',
    executables=executables,
    options=options
)