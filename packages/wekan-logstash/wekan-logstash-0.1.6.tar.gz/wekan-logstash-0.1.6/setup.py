# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wekan_logstash']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4',
 'click>=8.1.3',
 'pymongo>=4.1.1',
 'python-slugify>=6.1.2',
 'requests>=2.27.1']

entry_points = \
{'console_scripts': ['get_cards = wekan_logstash.cli:cli']}

setup_kwargs = {
    'name': 'wekan-logstash',
    'version': '0.1.6',
    'description': 'Simple script that will print cards data for logstash (ELK Kibana) in JSON format',
    'long_description': '# wekan-logstash\n\n## Install\n\nTo install the package run the following command\n\n```bash\npython -m pip install wekan-logstash\n```\n\nAfter installed the package from [PyPi]([https://](https://pypi.org/project/wekan-logstash/)), the script **get_cards** is available and ready to be running\n\n```bash\n#get_cards --help\n\nUsage: get_cards [OPTIONS] [BOARDSFILE]\n\n  Script to read Wekan cards belonging to one or more boards, directly from\n  Mongodb in JSON format.\n\n  Make a request to Logstash configured to use the HTTP input plugin to ingest\n  the cards into Elasticsearch.\n\nOptions:\n  --boardId TEXT  Single Board ID\n  --logstash      Make a HTTP request to Logstash endpoint, defined at\n                  LOGSTASH SERVER environment variable\n  -v, --verbose   Show cards JSON data\n  -h, --help      Show this message and exit.\n```\n\n> **Warning**: It is necessary before executing the above script that we define the following environment variables used for the connection to the mongodb database and the logstash URL\n>\n>- **MONGODB_USER**: Database username\n>- **MONGODB_PWD**: Database password\n>- **MONGODB_HOST**: Database hostname\n>- **MONGODB_PORT**: Database port\n>- **MONGODB_DB**: Database name\n>- **LOGSTASH_SERVER**: Logstash endpoint url\n\n## Data format\n\nTo format data for logstash and ELK (Kibana) - Format below :\n\n```json\n{\n  "id": "7WfoXMKnmbtaEwTnn",\n  "title": "Card title",\n  "storyPoint": 2.0,\n  "nbComments": 1,\n  "createdBy": "fmonthel",\n  "labels": [\n    "I-U",\n    "I-Nu"\n  ],\n  "assignees": "fmonthel",\n  "members": [\n    "fmonthel",\n    "Olivier"\n  ],\n  "boardSlug": "test",\n  "description": "A subtask description",\n  "startAt": "2021-06-07T20:36:00.000Z",\n  "endAt": "2021-06-07T20:36:00.000Z",\n  "requestedBy": "LR",\n  "assignedBy": "MM",\n  "receivedAt": "2021-06-07T20:36:00.000Z",\n  "archivedAt": "2021-06-07T20:36:00.000Z",\n  "createdAt": "2021-06-07T20:36:00.000Z",\n  "lastModification": "2017-02-19T03:12:13.740Z",\n  "list": "Done",\n  "dailyEvents": 5,\n  "board": "Test",\n  "isArchived": true,\n  "dueAt": "2021-06-07T20:36:00.000Z",\n  "swimlaneTitle": "Swinline Title",\n  "customfieldName1": "value1",\n  "customfieldName2": "value2",\n  "boardId": "eJPAgty3guECZf4hs",\n  "cardUrl": "http://localhost/b/xxQ4HBqsmCuP5mYkb/semanal-te/WufsAmiKmmiSmXr9m",\n  "checklists": [\n      {\n          "name": "checklist1",\n          "items": [\n              {"title": "item1", "isFinished": true},\n              {"title": "item2", "isFinished": false}\n            ]\n      },\n      {\n          "name": "checklist2",\n          "items": [\n              {"title": "item1", "isFinished": true},\n              {"title": "item2", "isFinished": true}\n            ]\n      }\n  ]\n}\n```\n\nGoal is to export data into Json format that we can be used as input for Logstash and ElastisSearch / Kibana (ELK)\n\nImport in logstash should be done daily basic (as we have field daily event)\n',
    'author': 'Franklin Gomez',
    'author_email': 'fgomezotero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fgomezotero/wekan-logstash',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
