"""
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  let's be lazy

"""

import sys
import json
import google.auth
from google.auth.transport.requests import AuthorizedSession
from slack_webhook import Slack
from string import Template

# full google api docs: https://developers.google.com/android-publisher/api-ref/rest/

# requires GOOGLE_APPLICATION_CREDENTIALS path to service json in environment, e.g.:
# export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/google-play-service.json"

PACKAGE_NAME = "your.app.package.name"
DRY_RUN = False
TRACK = 'production'
# define slack webhook url to enable notifications, empty string to disable
SLACK_URL = ''
# tweak message to your needs
MSG_TEMPLATE = Template(':android: $version Live scaled to $percentage%')


def scale(current_scale):
    '''select next step in scaling scheme'''
    scaling = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    i = 0
    while scaling[i] <= current_scale:
        i += 1
    return scaling[i]


def post_notification(version, scale):
    if SLACK_URL:
        s = MSG_TEMPLATE.substitute(version=version, percentage=int(scale*100))
        Slack(url=SLACK_URL).post(text=s)


API_V3 = "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/%s"%PACKAGE_NAME


def connect():
    '''connect to google api, expects GOOGLE_APPLICATION_CREDENTIALS in env'''
    credentials, _ = google.auth.default(
        scopes=['https://www.googleapis.com/auth/androidpublisher'])
    return AuthorizedSession(credentials)


authed_session = connect()

# create edit
response = authed_session.post(API_V3 + '/edits')
edit_id = response.json()["id"]

# get tracks
response = authed_session.get(API_V3 + "/edits/%s/tracks"%edit_id)
tracks = response.json()["tracks"]

releases = []

for track in tracks:
    print("\n-----------\nTrack: " + track["track"] + "\n-----------")
    if track["track"] == TRACK:
        # print(json.dumps(track, indent = 4))
        for release in track["releases"]:
            print(release["name"],
                  str(release["versionCodes"]),
                  release["status"], end=" ")
            if "userFraction" in release:
                print(release["userFraction"])
            if release["status"] != "completed":
                version = release["name"] + ' (' + str(max(release["versionCodes"])) + ")"
                # print("user fraction is currently %f" % release["userFraction"])
                scale = scale(release["userFraction"])
                print('--> scale %s to %d%%'%(version,(scale*100)))
                if scale == 1.0:
                    release["status"] = "completed"
                    release.pop('userFraction', None)
                else:
                    release["userFraction"] = scale
                releases.append(release)
            print("")

print("--- edit track ---")
json_track = {'track': TRACK, 'releases': releases}
json_string = json.dumps(json_track, indent=4)
# print(json_string)
response = authed_session.put(API_V3 + '/edits/%s/tracks/%s'%(edit_id, TRACK), data = json_string)
print(response)

if response.status_code != 200:
    print("editing failed")
    sys.exit(1)
# print(response.json())

print("--- commit ---")
if DRY_RUN is False:
    response = authed_session.post(API_V3 + '/edits/%s:commit'%edit_id)
    print(response)
    if response.status_code == 200:
        post_notification(version, scale)
    else:
        sys.exit(1)
else:
    print("Dry run, don't commit, validate instead and clean up")
    print("--- validate ---")
    response = authed_session.post(API_V3 + '/edits/%s:validate'%edit_id)
    print(response)
    # print(json.dumps(response.json()))
    print("--- clean up ---")
    response = authed_session.delete(API_V3 + '/edits/%s'%edit_id)
    print(response)

