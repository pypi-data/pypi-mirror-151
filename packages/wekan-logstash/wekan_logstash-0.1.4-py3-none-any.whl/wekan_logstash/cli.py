#!/usr/bin/env python
"""Simple script that will print cards data for logstash (ELK Kibana) in JSON format"""

import json

import click
import requests

from wekan_logstash.logstash import call_logstash, get_cardsdata, get_whitelist_boards, logstashEndpoint

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--boardId", is_flag=False, help="Single Board ID")
@click.option(
    "--logstash",
    is_flag=True,
    show_default=True,
    default=False,
    help="Make a HTTP request to Logstash endpoint, defined at LOGSTASH SERVER environment variable",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show cards JSON data")
@click.argument(
    "boardsfile",
    type=click.Path(exists=True, file_okay=True, readable=True),
    required=False,
)
def cli(boardid, logstash, verbose, boardsfile) -> None:
    """Script to read Wekan cards belonging to one or more boards, directly from Mongodb in JSON format.

    Make a request to Logstash configured to use the HTTP input plugin to ingest the cards into Elasticsearch.

    """
    # Get all cards and iterate over them
    try:
        if boardsfile is not None:
            boardlist = get_whitelist_boards(boardsfile)
            cards = get_cardsdata(boardlist)
        else:
            cards = get_cardsdata([boardid])
        for card in cards.values():
            if verbose:
                print(json.dumps(card, ensure_ascii=False, sort_keys=True))
            if logstash:
                call_logstash(json.dumps(card, ensure_ascii=True, sort_keys=True))
        click.echo(
            f'{len(cards)} cards processed {":). Congrats!" if len(cards) > 0 else ":(. Sorry, enter an board ID that exists by --boardId option or boardfile argument"}'
        )
    except requests.exceptions.RequestException:
        # click.echo(error)
        click.echo(f"Error - Sorry, Logstash endpoint URL {logstashEndpoint} is not reachable! :(")


if __name__ == "__main__":
    cli()
