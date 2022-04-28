#! /bin/env python
"""
Description: This module contains MatterMost notification techniques.

Title: mattermost_notification.py

Author: ObsidianX
"""

import os
from argparse import ArgumentParser
from inspect import currentframe
from pathlib import Path
from types import FrameType
from typing import Dict
from typing import SupportsInt
from typing import Text
from typing import cast

from requests import Session

try:
    from .logger import set_up_stream_logging
except ImportError:
    from app.logger import set_up_stream_logging

log = set_up_stream_logging()  # pylint: disable=C0103


def post_to_mattermost_incoming_webhook(key_: Text, session: Session = Session(),
                                        message: Text = None, payload: Dict = None) -> SupportsInt:
    """Generate MatterMost notification via webhook.

     This function will generate MatterMost notification by making a
     web services POST call via REST protocol. it logs debug
     information to standard error output.

    Args:
        key_(Text): MatterMost webhook url key.
        session(requests.Session): Session object to perform the web
            request.
        message(Text): Optional. Text to post message on MatterMost.
        payload(Dict): Optional. Customized MatterMost post.

    Returns:
        Response status code as an integer.

    """
    mattermost_server = "some mattermost fqdn"
    url = f"https://{mattermost_server}/hooks/{key_}"

    # https://stackoverflow.com/a/13514318
    function_name = f"{cast(FrameType, currentframe()).f_code.co_name}"  # Just go with it.

    if message:
        payload = {"Text": message}
    else:
        if not payload:
            message = f"@all: unexpected use of [{function_name}]"
            payload = {"Text": message}

    response = session.post(url, json=payload, verify=os.getenv("CA_BUNDLE", False))
    response.raise_for_status()

    log.debug('+++ request information +++')
    log.debug('request url: %s', response.url)
    log.debug('request status code: %s', response.status_code)
    log.debug('request reason: %s', response.reason)
    log.debug('request headers: %s', response.headers)
    log.debug('request content: %s', response.content)

    return response.status_code


def main():
    """Provide access to module as standalone project."""
    # Replace webhook key to test your webhook.

    parser = ArgumentParser()
    parser.add_argument('--key', required=True)
    parser.add_argument('--message', help="Text to post on MatterMost", type=Text)
    parser.add_argument('--payload', help="JSON string of custom MatterMost payload", type=Text)
    args = parser.parse_args()

    post_to_mattermost_incoming_webhook(key_=args.key, message=args.message, payload=args.payload)


if __name__ == '__main__':
    main()
