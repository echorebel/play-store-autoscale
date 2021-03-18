# play-store-autoscale
this script in combination with a cronjob or any other trigger from your CI
system can take care of scaling a release on play-store automatically.
Optionally it can also informs your colleagues in a slack channel.

## Requirements
- play store service account + json with credentials, see usage 1.
- python 3.x
- `pip` for installing required modules
- install requirements via `pip install -r requirements.txt`


## Usage
1. get play store service account and download json with access tokens, here is
a [nice
explanation](https://github.com/Triple-T/gradle-play-publisher#service-account)
2. export path to google-play-service.json
3. Configure script with your app id, decide on track and scaling scheme
4. The script is configured to scale two next level whenever triggeredr.
It picks up the user fraction / scale of an in-progress app.
You can tweak function `scale` to your needs.
5. Configure a cronjob or a job on your CI system that triggers the script,
   e.g. daily
6. (Optional) For slack notifications configure a webhook and set SLACK_URL to it


## Usage of Docker image
With a docker you can put your secret client json and slack webhook into one
nice package and deploy it to your CI registry (never public).
1. copy google-play-service.json to the project
2. docker build -t playstore-autoscale .
3. docker tag
3. docker run -it --rm --name playstore-autoscale playstore-autoscale


## Used libs
- [google-auth](https://github.com/googleapis/google-auth-library-python)
- [slack-webhook](ihttps://github.com/10mohi6/slack-webhook-python)


## Credit
inspired by
[gradle-play-publisher](https://github.com/Triple-T/gradle-play-publisher)
doing an full app checkout and gradle run seemed overkill to just bump up
    scaling number for this use case, for app releases this is very good
