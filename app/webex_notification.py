#! /bin/env python
"""
Description: This module contains Webex notification techniques.

This module was tested with Bearer Token authentication. Refinement for
bot accounts may need to occur.

Title: webex_notification.py

Author: Shayne Cardwell
"""
import os
from pathlib import Path

from httpx import Client

from app.env_manipulation import read_env_file
from app.logger import set_up_stream_logging

log = set_up_stream_logging()  # pylint: disable=C0103


def _handle_token_errors(payload):
    look_for = 'authorization request header'
    if 'errors' in payload and look_for.lower() in f"{payload['message']}".lower():
        message = (f"The cake is a lie.\nA new token is needed.\n"
                   f"See https://developer.webex.com/docs/getting-started for more details.")
        raise ValueError(message)


def _handle_malformed_errors(payload, response_obj):
    look_for = 'malformed syntax'
    if 'errors' in payload and look_for.lower() in f"{payload['message']}".lower():
        print('The cake is a lie.')
        print('Malformed request.')
        print(response_obj.url)
        print(response_obj.status_code)
        print(response_obj.reason_phrase)
        print(response_obj.content)
        print(response_obj.request)
        print(response_obj.request.headers)
        raise RuntimeError('This is just to stop the execution. See statements above')


def webex_request(
        url_path: str,
        *,
        method: str = 'get',
        headers: dict = None,
        url_params: dict = None,
        data: dict = None,
        json: dict = None
):
    """This function communicates with Webex."""
    if not headers:
        headers = {
            'Content-Type':  'application/json',
            'Authorization': f"Bearer {os.getenv('WEBEX_TOKEN')}"
        }
    ca_bundle = os.getenv('CA_BUNDLE')
    if not ca_bundle:
        ca_bundle = False

    client = Client(
        base_url='https://webexapis.com',
        verify=ca_bundle,
        timeout=120
    )
    response_obj = client.request(
        method=method.upper(),
        url=url_path,
        headers=headers,
        params=url_params,
        data=data,
        json=json
    )
    json_response = response_obj.json()
    _handle_token_errors(json_response)
    _handle_malformed_errors(json_response, response_obj)
    return json_response


def get_webex_teams() -> dict:
    """Collect all Webex spaces."""
    url_path = '/v1/teams'
    return webex_request(url_path)


def find_webex_team(team_name: str) -> dict:
    """Find a specific team."""
    webex_teams: list = get_webex_teams()['items']
    for webex_team in webex_teams:
        if f"{webex_team['name']}".lower() == team_name.lower():
            return webex_team
    return {}


def team_name_to_id(team_name: str) -> str:
    """Return the unique identifier for a team."""
    team_information = find_webex_team(team_name)
    return team_information.get('id', '')


def get_team_rooms(team_name: str) -> dict:
    """Return a list of rooms for a webex team."""
    url_path = '/v1/rooms'
    params = {
        'teamId': team_name_to_id(team_name)
    }
    response = webex_request(url_path, url_params=params)
    return response


def find_team_room(team_name: str, room_name: str) -> dict:
    """Find a specific team."""
    team_rooms: list = get_team_rooms(team_name)['items']
    if room_name.lower() == 'general':
        room_name = team_name

    for webex_team in team_rooms:
        if f"{webex_team['title']}".lower() == room_name.lower():
            return webex_team
    return {}


def room_name_to_id(team_name: str, room_name: str) -> dict:
    """Return the unique identifier for a team."""
    room_information = find_team_room(team_name, room_name)
    return room_information.get('id', {})


def get_team_memberships(team_id: str):
    """Return all the members of a team."""
    url_path = '/v1/team/memberships'
    params = {
        'teamId': team_id
    }
    response = webex_request(url_path, url_params=params)
    return response


def get_messages(team_name: str, room_name: str) -> dict:
    """Return all messages."""
    url_path = '/v1/messages'
    membership_details = get_team_memberships(team_name_to_id(team_name))
    member_ids = [member['personId'] for member in membership_details['items']]
    print(member_ids)
    params = {
        'roomId': room_name_to_id(team_name, room_name),
        'mentionedPeople': member_ids
    }
    response = webex_request(url_path, url_params=params)
    return response


def send_message(team_name: str, room_name: str, text: str = None,
                 body_parameters: dict = None) -> dict:
    """Test send message."""
    url_path = '/v1/messages'
    if not text:
        text = 'Hello World!'

    if not body_parameters:
        body_parameters = {
            'roomId': room_name_to_id(team_name, room_name),
            'text':   text
        }
    response = webex_request(url_path, method='post', json=body_parameters)
    return response


def main():
    """Provide access to module as standalone project."""
    read_env_file()
    team_name = 'ckr'
    room_name = 'general'
    print(get_team_rooms(team_name))
    print(get_messages(team_name, room_name))
    print(send_message(team_name, room_name, text='Hello World from python!'))
    body_parameters = {
        'roomId':   room_name_to_id(team_name, room_name),
        'markdown': '<@all> **Hello World** _from python constructed body!_'
    }
    print(send_message(team_name, room_name, body_parameters=body_parameters))


if __name__ == '__main__':
    main()
