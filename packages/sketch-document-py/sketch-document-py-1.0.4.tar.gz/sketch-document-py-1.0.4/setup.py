# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sketch_document_py',
 'sketch_document_py.sketch_file',
 'sketch_document_py.sketch_file_format']

package_data = \
{'': ['*']}

install_requires = \
['fastclasses-json>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'sketch-document-py',
    'version': '1.0.4',
    'description': 'This project contains the APIs to work with Sketch documents and document elements in Python dataclass.',
    'long_description': '# `.sketch` document for python\n\n[Sketch](https://sketch.com) stores documents in `.sketch` format, a zipped\narchive of JSON formatted data and binary data such as images.\n\nInspired by [sketch-hq/sketch-document](https://github.com/sketch-hq/sketch-document)\n\nBuilt package is avaliable in [Pypi](https://pypi.org/project/sketch-document-py/), install with Pip\n```shell\npip install sketch-document-py\n```\n\n## Sketch file format schemas and APIs.\n\nThis project contains the APIs to work with Sketch\ndocuments and document elements in Python dataclass.\n\n- `sketch-file-format-py`: Python dataclass type hint to strongly type objects\n  representing Sketch documents, or fragments of Sketch documents in TypeScript\n  projects.\n- `sketch-file`: Python APIs to read and write `.sketch` files.\n## Development\n\nTo build this project, you need install Python build dependency management tool [Poetry](https://python-poetry.org/), to install Poetry , follow [Poetry installation guide](https://python-poetry.org/docs/#installation)\n\nTo install nessasary deps and CLI tools, including a task runner [Poe the Poet](https://github.com/nat-n/poethepoet)(CLI executable named `poe`) that work with Poetry, run command:\n> This will also install current package to your environment root\n\n> For further usages of Poetry Install, check [Poetry Install](https://python-poetry.org/docs/cli/#install)\n\n```shell\npoetry install\n```\n\nTo generate Sketch Dataclass type file, which is nessasary for build or install development, run command:\n> For further usages of Poe the Poet, check [Poe the Poet Homepage](https://github.com/nat-n/poethepoet)\n```shell\npoe gen_types\n```\n\nTo check project typing, run command:\n> For further usages of Mypy, check [Mypy Documentation](https://mypy.readthedocs.io/en/stable/)\n```shell\npoe mypy\n```\n\nTo run project test and coverage, run command:\n> For further usages of Coverage, check [Coverage.py Documentation](https://coverage.readthedocs.io/en/6.3.2/)\n```shell\npoe test\n```\n\nTo build project to wheel and tar, run command:\n> For further usages of Poetry build, check [Poetry Build](https://python-poetry.org/docs/cli/#build)\n```shell\npoe build\n```\n\nTo publish project, run command:\n> For further usages of Poetry, check [Poetry Publish](https://python-poetry.org/docs/cli/#publish)\n```shell\npoe publish\n```\n\nFor further usages of Poetry, check [Poetry Documentation](https://python-poetry.org/docs)',
    'author': 'Borealin',
    'author_email': 'shichuning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Borealin/sketch-document-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
