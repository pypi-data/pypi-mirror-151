# wekan-logstash

## Install

To install the package run the following command

```bash
python -m pip install wekan-logstash
```

After installed the package from [PyPi]([https://](https://pypi.org/project/wekan-logstash/)), the script **get_cards** is available and ready to be running

```bash
#get_cards --help

Usage: get_cards [OPTIONS] [BOARDSFILE]

  Script to read Wekan cards belonging to one or more boards, directly from
  Mongodb in JSON format.

  Make a request to Logstash configured to use the HTTP input plugin to ingest
  the cards into Elasticsearch.

Options:
  --boardId TEXT  Single Board ID
  --logstash      Make a HTTP request to Logstash endpoint, defined at
                  LOGSTASH SERVER environment variable
  -v, --verbose   Show cards JSON data
  -h, --help      Show this message and exit.
```

> **Warning**: It is necessary before executing the above script that we define the following environment variables used for the connection to the mongodb database and the logstash URL
>
>- **MONGODB_USER**: Database username
>- **MONGODB_PWD**: Database password
>- **MONGODB_HOST**: Database hostname
>- **MONGODB_PORT**: Database port
>- **MONGODB_DB**: Database name
>- **LOGSTASH_SERVER**: Logstash endpoint url

## Data format

To format data for logstash and ELK (Kibana) - Format below :

```json
{
  "id": "7WfoXMKnmbtaEwTnn",
  "title": "Card title",
  "storyPoint": 2.0,
  "nbComments": 1,
  "createdBy": "fmonthel",
  "labels": [
    "I-U",
    "I-Nu"
  ],
  "assignees": "fmonthel",
  "members": [
    "fmonthel",
    "Olivier"
  ],
  "boardSlug": "test",
  "description": "A subtask description",
  "startAt": "2021-06-07T20:36:00.000Z",
  "endAt": "2021-06-07T20:36:00.000Z",
  "requestedBy": "LR",
  "assignedBy": "MM",
  "receivedAt": "2021-06-07T20:36:00.000Z",
  "archivedAt": "2021-06-07T20:36:00.000Z",
  "createdAt": "2021-06-07T20:36:00.000Z",
  "lastModification": "2017-02-19T03:12:13.740Z",
  "list": "Done",
  "dailyEvents": 5,
  "board": "Test",
  "isArchived": true,
  "dueAt": "2021-06-07T20:36:00.000Z",
  "swimlaneTitle": "Swinline Title",
  "customfieldName1": "value1",
  "customfieldName2": "value2",
  "boardId": "eJPAgty3guECZf4hs",
  "cardUrl": "http://localhost/b/xxQ4HBqsmCuP5mYkb/semanal-te/WufsAmiKmmiSmXr9m",
  "checklists": [
      {
          "name": "checklist1",
          "items": [
              {"title": "item1", "isFinished": true},
              {"title": "item2", "isFinished": false}
            ]
      },
      {
          "name": "checklist2",
          "items": [
              {"title": "item1", "isFinished": true},
              {"title": "item2", "isFinished": true}
            ]
      }
  ]
}
```

Goal is to export data into Json format that we can be used as input for Logstash and ElastisSearch / Kibana (ELK)

Import in logstash should be done daily basic (as we have field daily event)
