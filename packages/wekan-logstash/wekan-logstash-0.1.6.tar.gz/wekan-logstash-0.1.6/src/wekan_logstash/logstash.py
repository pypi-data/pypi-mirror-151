"""Simple module that will get cards data for logstash (ELK Kibana) in JSON format"""


import datetime
import os

import requests

# from pandas import isna
from pymongo import mongo_client
from slugify import slugify

# Globals Variables
mongo_user = os.getenv("MONGODB_USER", "")
mongo_password = os.getenv("MONGODB_PWD", "")
mongo_server = os.getenv("MONGODB_HOST", "localhost")
mongo_port = os.getenv("MONGODB_PORT", "27017")
mongo_database = os.getenv("MONGODB_DB", "wekan")
baseURL = os.getenv("BASEURL", "http://localhost")
logstashEndpoint = os.getenv("LOGSTASH_SERVER", "http://localhost:5044")
# time_start = datetime.datetime.now()
date_start = datetime.datetime.today().date()
# create connection string depending on whether mongo database accepts username and password or not
conn_str = (
    "mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_server + "/" + mongo_database
    if mongo_user != ""
    else "mongodb://" + mongo_server + "/" + mongo_database
)


def call_logstash(card):
    """Make a request to logstash endpoint services

    :param card: A single card
    :return: Response status code
    """
    response = requests.post(
        logstashEndpoint,
        data=card,
        headers={"Content-type": "application/json", "Accept": "text/plain"},
    )
    return response.status_code


def get_dropdown_value(cf_id, dropdown):
    """Function that will get a value of a customfield of type dropdown

    :param cf_id: customfield id
    :param dropdown: specific dict inside of customfield
    :return: value selected in the customfield of type dropdown
    """
    result = None
    for item in dropdown:
        if cf_id == item.get("_id"):
            result = item.get("name")
            break
    return result


def get_whitelist_boards(filepath: str):
    """Get list of boards that will be in whitelist

    :return: A list of boards ids
    """
    text_file = open(
        filepath,
        "r",
        encoding="utf-8",
    )
    lines = text_file.read().split("\n")
    text_file.close()
    return lines


def getstorypoint(title):
    """Function that will get in the title the first characters as storypoints

    :param title: Card title
    :return:
    """
    tmp = ""
    for letter in title:
        if letter in [".", ",", " ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            tmp += letter
        else:
            break
    try:
        return float(tmp)
    except ValueError:
        return 0


def get_checklist(cardid: str, checklists, checklistitems) -> list:
    """Get a list of the checklist that belongs to a card

    Example of return:
    [
        {
            'name': 'checklist1',
            'items': [
                {'title': valor, 'isFinished': valor},
                {'title': valor, 'isFinished': valor}
                ]
        },
        {
            'name': 'checklist2',
            'items': [
                {'title': valor, 'isFinished': valor},
                {'title': valor, 'isFinished': valor}
                ]
        }
    ]

    Args:
        cardid (str): Card id
        checklists (_type_): Mongo object with all the checklist
        checklistitems (_type_): Mongo object with all the checklistItems

    Returns:
        list: _description_
    """
    result = list()
    if checklists.count_documents({"cardId": cardid}):
        checklist_iterator = checklists.find({"cardId": cardid})
        for checklist_item in checklist_iterator:
            item = {"name": checklist_item.get("title"), "items": list()}
            if checklistitems.count_documents({"checklistId": checklist_item.get("_id")}):
                checklistitems_iterator = checklistitems.find({"checklistId": checklist_item.get("_id")})
                for checklistitems_item in checklistitems_iterator:
                    element = {
                        "title": checklistitems_item.get("title"),
                        "isfinished": checklistitems_item.get("isFinished"),
                    }
                    item["items"].append(element)
            result.append(item)
    return result


def get_cardsdata(boardlist: list):
    """Function that will populate dict for logstash

    :return: A dict with the collections of all cards
    """

    mongo = mongo_client.MongoClient(conn_str)
    database = mongo[mongo_database]
    users = database["users"]
    boards = database["boards"]
    lists = database["lists"]
    cards = database["cards"]
    card_comments = database["card_comments"]
    activities = database["activities"]
    swimlanes = database["swimlanes"]
    customfields = database["customFields"]
    checklists = database["checklists"]
    checklistsitems = database["checklistItems"]

    # Get cards data
    data = dict()
    # select cards for boards in whitelist file
    for card in cards.find({"boardId": {"$in": boardlist}}):
        try:
            # Create index on id of the card
            data[card["_id"]] = dict()

            # Get id
            data[card["_id"]]["id"] = card["_id"]

            # Get archived data
            data[card["_id"]]["isArchived"] = card["archived"]
            if card["archived"]:
                # Get date of archive process
                if activities.count_documents({"cardId": card["_id"], "activityType": "archivedCard"}):
                    activity = activities.find_one({"cardId": card["_id"], "activityType": "archivedCard"})
                    data[card["_id"]]["archivedAt"] = datetime.datetime.strftime(
                        activity["createdAt"], "%Y-%m-%dT%H:%M:%S.000Z"  # type: ignore
                    )

            # Get storypoint data
            if "title" in card and card["title"] is not None:
                data[card["_id"]]["storyPoint"] = getstorypoint(card["title"])

            # Get created date data
            data[card["_id"]]["createdAt"] = datetime.datetime.strftime(card["createdAt"], "%Y-%m-%dT%H:%M:%S.000Z")

            # Get receivedAt data card
            if "receivedAt" in card and card["receivedAt"] is not None:
                data[card["_id"]]["receivedAt"] = datetime.datetime.strftime(
                    card["receivedAt"], "%Y-%m-%dT%H:%M:%S.000Z"
                )

            # Get startAt data card
            if "startAt" in card and card["startAt"] is not None:
                data[card["_id"]]["startAt"] = datetime.datetime.strftime(card["startAt"], "%Y-%m-%dT%H:%M:%S.000Z")

            # Get dueAt date data
            if "dueAt" in card and card["dueAt"] is not None:
                data[card["_id"]]["dueAt"] = datetime.datetime.strftime(card["dueAt"], "%Y-%m-%dT%H:%M:%S.000Z")

            # Get endAt data card
            if "endAt" in card and card["endAt"] is not None:
                data[card["_id"]]["endAt"] = datetime.datetime.strftime(card["endAt"], "%Y-%m-%dT%H:%M:%S.000Z")

            # Get number of comments data
            data[card["_id"]]["nbComments"] = card_comments.count_documents({"cardId": card["_id"]})

            # Get creator name
            if users.count_documents({"_id": card["userId"]}):
                data[card["_id"]]["createdBy"] = dict(users.find_one({"_id": card["userId"]}))["username"]

            # Get swimlane name
            if swimlanes.count_documents({"_id": card["swimlaneId"]}):
                data[card["_id"]]["swimlaneTitle"] = dict(swimlanes.find_one({"_id": card["swimlaneId"]}))["title"]

            # Get list name
            if lists.count_documents({"_id": card["listId"]}):
                data[card["_id"]]["list"] = dict(lists.find_one({"_id": card["listId"]}))["title"]

            # Get board id
            board = dict(boards.find_one({"_id": card["boardId"]}))
            data[card["_id"]]["boardId"] = board.get("_id")

            # Get board title
            data[card["_id"]]["board"] = board["title"]

            # Get board title slug
            data[card["_id"]]["boardSlug"] = slugify(board["title"])

            # Get title data
            if "title" in card:
                data[card["_id"]]["title"] = card["title"]

            # Get card description
            if "description" in card:
                data[card["_id"]]["description"] = card["description"]

            # Get assignedBy card field
            if "assignedBy" in card and card["assignedBy"] != "":
                data[card["_id"]]["assignedBy"] = card["assignedBy"]

            # Get requestedBy card field
            if "requestedBy" in card and card["requestedBy"] != "":
                data[card["_id"]]["requestedBy"] = card["requestedBy"]

            # Get labels card field
            data[card["_id"]]["labels"] = list()
            if "labelIds" in card and len(card["labelIds"]):
                for labelid in card["labelIds"]:
                    # We will parse board label
                    for label in board["labels"]:
                        if "_id" in label.keys() and labelid == label["_id"]:
                            if "name" in label or label["name"] is not None:
                                data[card["_id"]]["labels"].append(label["name"])
            else:
                data[card["_id"]]["labels"].append("No label")

            # add card URL to dict
            data[card["_id"]]["cardUrl"] = (
                baseURL + "/b/" + card["boardId"] + "/" + data[card["_id"]]["boardSlug"] + "/" + card["_id"]
            )

            # Get the members data or we will set unassigned if there is no
            members = list()
            if len(card["members"]):
                for member in card["members"]:
                    if users.count_documents({"_id": member}):
                        members.append(dict(users.find_one({"_id": member}))["username"])
            else:
                members.append("Unassigned")
            data[card["_id"]]["members"] = members

            # Get assignees data or we will set unassigned if there is no
            assignees = list()
            if len(card["assignees"]):
                for member in card["assignees"]:
                    if users.count_documents({"_id": member}):
                        assignees.append(dict(users.find_one({"_id": member}))["username"])
            if "assignees" not in card or len(card["assignees"]) == 0:
                assignees.append("Unassigned")
            data[card["_id"]]["assignees"] = assignees

            # Get last activity date data (will be updated after)
            data[card["_id"]]["lastModification"] = card["dateLastActivity"]

            # Get daily events and update lastModification of card
            data[card["_id"]]["dailyEvents"] = 0
            for activity in activities.find({"cardId": card["_id"]}):
                if activity["createdAt"].date() == date_start:
                    data[card["_id"]]["dailyEvents"] += 1
                if activity["createdAt"] > data[card["_id"]]["lastModification"]:
                    data[card["_id"]]["lastModification"] = activity["createdAt"]

            # Fornat the lastModification date now
            data[card["_id"]]["lastModification"] = datetime.datetime.strftime(
                data[card["_id"]]["lastModification"], "%Y-%m-%dT%H:%M:%S.000Z"
            )

            # Get customs fields labels selected
            customfield_list = card["customFields"]
            for customfield in customfield_list:
                if (
                    customfields.count_documents({"_id": customfield.get("_id")})
                    and "value" in customfield.keys()
                    and customfield.get("value") is not None
                    # and not isna(customfield.get("value"))
                ):
                    ro_cfield = customfields.find_one({"_id": customfield.get("_id")})
                    if dict(ro_cfield).get("type") == "dropdown":
                        data[card["_id"]][dict(ro_cfield).get("name")] = get_dropdown_value(
                            customfield.get("value"),
                            dict(dict(ro_cfield).get("settings")).get("dropdownItems"),
                        )
                    elif (
                        dict(ro_cfield).get("type") == "checkbox"
                        or dict(ro_cfield).get("type") == "text"
                        or dict(ro_cfield).get("type") == "number"
                        or dict(ro_cfield).get("type") == "currency"
                    ):
                        data[card["_id"]][dict(ro_cfield).get("name")] = customfield.get("value")
                    elif dict(ro_cfield).get("type") == "date":
                        data[card["_id"]][dict(ro_cfield).get("name")] = datetime.datetime.strftime(
                            customfield.get("value"), "%Y-%m-%dT%H:%M:%S.000Z"
                        )

            # Get checklists list
            checklist_list = get_checklist(card["_id"], checklists, checklistsitems)
            if len(checklist_list) > 0:
                data[card["_id"]]["checklists"] = checklist_list

        except Exception as error:  # type: ignore
            print(error)
            print(card["_id"])
    # End, time to return dict :)
    return data
