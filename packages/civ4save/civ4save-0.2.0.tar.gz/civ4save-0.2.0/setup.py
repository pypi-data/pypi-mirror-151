# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['civ4save']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.68,<3.0.0']

extras_require = \
{'xml': ['Jinja2>=3.1.2,<4.0.0', 'xmltodict>=0.12.0,<0.13.0']}

entry_points = \
{'console_scripts': ['civ4save = civ4save.cli:run']}

setup_kwargs = {
    'name': 'civ4save',
    'version': '0.2.0',
    'description': 'Extract data from a .CivBeyondSwordSave file',
    'long_description': "# Beyond the Sword Save File Reader\n\nUncompresses and decodes the data in a `.CivBeyondSwordSave` file.\ncheck out this [example](example.json) to see what data you can get.\n\nSo far I've only tested with the vanilla version of the Civ4 BTS and the slightly tweaked XML files Sullla uses in the [AI survivor series](https://sullla.com/Civ4/civ4survivor6-14.html).\nMods like BAT/BUG/BULL change the structure of the save file and do not work.\nI'd like to support them but I need specific details on what changes the mods are making to the binary save format.\n\nThanks to [this repo](https://github.com/dguenms/beyond-the-sword-sdk) for hosting\nthe Civ4 BTS source. Wouldn't have been possible to make this without it.\n\n\n### Usage\n\n#### Install\n\n* Requires >= python3.10\n* If someone opens an issue requesting 3.6-3.9 I'll get to it\n\n`python -m pip install civ4save`\n\n#### Command line Tool\nOutput is JSON.\n\n`python -m civ4save <options> <save_file>`\n\n```\nusage: civ4save [-h] [--max-players MAX_PLAYERS]\n    [--with-plots | --just-settings | --just-players | --player PLAYER | --list-players]\n    file\n\nExtract data from .CivBeyondSwordSave file\n\npositional arguments:\n  file                  Target save file\n\noptions:\n  -h, --help            show this help message and exit\n  --max-players MAX_PLAYERS\n                        Needed if you have changed your MAX_PLAYERS value in CvDefines.h\n  --with-plots          Attempt to parse the plot data. WARNING: still buggy!\n  --just-settings       Only return the games settings. No game state or player data\n  --just-players        Only return the player data\n  --player PLAYER       Only return the player data for a specific player idx\n  --list-players        List all player idx, name, leader, civ in the game\n  --ai-survivor         Use XML settings from AI Survivor series\n  --debug               Print debug info\n```\n\n#### As a Libray\n\n```python\nfrom civ4save import save_file\nfrom civ4save.structure import get_format\n\nsave_bytes = save_file.read('path/to/save')\n\n# get_format takes 3 optional arguments\n# ai_survivor: bool  -- use the tweaked XML files as seen in ai survivor\n# with_plots: bool  -- try expiremental plot parsing\n# debug: bool  -- calls Construct.Probe() to print debug info\nfmt = get_format()\n# default max_players=19, you'll know if you changed this\ndata = fmt.parse(save_bytes, max_players=19)\n\n# do whatever you want to with the data, see organize.py for ideas\n```\n\n#### Developement / Contributing\n* [poetry](https://python-poetry.org/docs/)\n* run tests with `poetry run pytest -rP tests/`\n* If you open an issue please attach the save file you had the issue with\n\n\n### How it Works\nGames are saved in a binary format that kind of looks like a sandwich\n\n`| uncompressed data | zlib compressed data | uncompressed checksum |`\n\nwith most of the data in the compressed middle part. See `save_file.py` to understand\nhow the file is uncompressed.\n\nThe [construct](https://github.com/construct/construct) library makes it easy to declaratively\ndefine the binary format in `structure.py` and this gives us parsing/writing for free.\n\nFrom there the functions in `organize.py` sort and cleanup the parsed data.\n\nThe enums defined in `cv_enums.py` are automatically generated from the game\nXML files using `xml_to_enum.py`. To run this yourself you'll need to install the optional\n`jinja2` and `xmltodict` dependencies:\n\n`poetry install -E xml`\n\nRight now the paths to the XML files in `xml_to_enum.py` are hardcoded so you'll have to edit\nthem to match your system.\n\n\n#### Write Order\nThe game calls it's `::write` functions in this order:\n\n1. CvInitCore\n2. CvGame\n3. CvMap\n4. CvPlot (incomplete/buggy)\n4. CvTeam (not implemented)\n5. CvPlayer (not implemented)\n\nBut there's issues consistently parsing `CvPlot` so only up to CvMap is parsed by default.\nI haven't drilled down the exact cause but it seems to have something to do with the size of the save file.\nFiles under 136K (largest test save I have that works) parse fine but anything larger only makes it through ~30-80% of the plots before hitting a string of `0xff` bytes followed by data I can't make any sense of.\n\n`poetry run python -m civ4save.plots_bug.py` will demonstrate the bug and prints out debug info.\n",
    'author': 'Dan Davis',
    'author_email': 'dan@dandavis.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danofsteel32/civ4save',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
