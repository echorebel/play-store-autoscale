# play-store-autoscale
this script in combination with a cronjob can take care
of scaling a release on play-store automatically.

## Requirements
- python 3.x
- `pip` for installing jira module
- [google-auth](https://github.com/googleapis/google-auth-library-python)
    - install via `pip install google-auth`
- play store service account + json with credentials

## usage
1. get play store service account and download json with access tokens
2. export path to google-play-service.json
3. configure script with your app id and track u want to scale
4. the script is configured to scale in 7d from Wednesday to Wednesday, tweak
   function `scale` to your needs and configure a cronjob or similar to trigger
   daily


## usage of Docker image
1. copy google-play-service.json to the project
2. docker build -t playstore-autoscale .
3. docker run -it --rm --name playstore-autoscale playstore-autoscale
