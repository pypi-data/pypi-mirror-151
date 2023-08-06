# Starmerx Apollo Client


## Description

Client for Apollo Server.The following are provided by it:

- heartbeat once every ten minutes
- polling once every two seconds(it means that your config would be update in tow seconds)
- Disaster Tolerance(it reads your config in order of memory cache, requesting apollo server by http and cache file)


## Demo

The demo is in ./test/client_test.py

