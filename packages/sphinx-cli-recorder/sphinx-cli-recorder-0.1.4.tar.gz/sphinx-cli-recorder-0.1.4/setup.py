# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_cli_recorder', 'sphinx_cli_recorder.testing']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Sphinx>=4.4.0,<5.0.0',
 'asciinema>=2.2.0,<3.0.0',
 'asyncer>=0.0.1,<0.0.2',
 'pexpect>=4.8.0,<5.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'unsync>=1.4.0,<2.0.0',
 'yamale>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'sphinx-cli-recorder',
    'version': '0.1.4',
    'description': 'A Sphinx extension that runs/automates recordings of CLI applications, without requiring any external services.',
    'long_description': '# Sphinx CLI Recorder\n[![Tests](https://img.shields.io/github/workflow/status/kai-tub/sphinx_cli_recorder/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/sphinx_cli_recorder/actions/workflows/main.yml)\n[![License](https://img.shields.io/pypi/l/sphinx_cli_recorder?color=dark-green)](https://github.com/kai-tub/sphinx_cli_recorder/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/sphinx-cli-recorder.svg)](https://pypi.org/project/sphinx-cli-recorder/)\n[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)\n\n```{warning}\nThe library is in its early stages!\n```\n\n:::{admonition} TL;DR\n:class: note\n\n- 🎥 Record interactions (input & output) with CLI applications\n- 🤖 Automate the recording process via simple Sphinx directives\n- ✔️ Simple; does not require any knowledge of the underlying recording application\n- ⛓️ No dependencies on external services; all files are generated and hosted locally\n:::\n\nThis Sphinx extension is a tool to allow you to easily automate the recording process of CLI applications (without you having to leave your editor 🤯).\n\nSuppose you are developing a neat CLI application, possibly with [rich](rich:introduction) (get it?) visual output. In that case, you put blood, sweat, and tears into the development part but do you want to put the same amount of effort into the documentation?\nShouldn\'t it be easy to show what your CLI application can do?\nIf you record a terminal session to show how to interact with your tool, you need to ensure that the recording is kept up-to-date and doesn\'t break with future updates.\nThen you need to know how to upload the file and embed it into your documentation.\nAnd all you want to do is to show something cool like:\n\n```{record_cli_cmd} python -m sphinx_cli_recorder.testing.animation_example\n:autoplay: "True"\n```\n\nOr give the user an example on how to navigate your CLI application:\n```{record_timed_cli_interaction} python -m sphinx_cli_recorder.testing.prompt\n\n    - "y"\n    - "5"\n    - "2"\n    - "poodle"\n    - "husky"\n```\n\nOr you are looking for a simple way always to include the most recent help text of a tool you are developing.\n```{record_cli_cmd} rich --help\n:rows: 67\n:autoplay: "True"\n```\n\nIn those cases, it is probably easier to let the _Sphinx-CLI-Recorder_ handle it for you. 😎\nIt uses [asciinema](https://asciinema.org), a text-based terminal recorder under the hood.\nUtilizing a text-based terminal player has the following advantages:\n- ✅ The output is _lossless_; no more pixelated videos/images with compression artifacts\n- ✅ No need to wait for huge-video file downloads\n- ✅ The terminal\'s content can be copied to the clipboard; no need to manually re-type the commands that are shown in a GIF/video\n\nThe benefits of using this Sphinx extension are:\n- 🤖 Automates the recording process of [asciinema](https://asciinema.org)\n- 📅 Ensures that the recordings are always up-to-date\n    - 💣 If the code changes and the commands from the documentation fail, no documentation will be built\n- 🏠 Keeps all of your files/data local:\n    - 🔐 No need to depend on external services/tokens to upload the recordings\n- 🚅 The recordings are done in parallel to minimize the documentation build time\n- ☑️ Simple; no need to understand how [asciinema](https://asciinema.org) works\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/sphinx_cli_recorder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
