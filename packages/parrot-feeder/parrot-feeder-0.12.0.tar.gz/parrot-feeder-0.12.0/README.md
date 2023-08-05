## General Information
Advanced multichannel file sharing web server.

See also:
- https://hub.docker.com/r/lep0puglabs/parrot-feeder
- https://pypi.org/project/parrot-feeder/

Parrot-feeder is an all-in-one combination of the following tools:

- https://github.com/cyberhexe/ngflask
- https://github.com/mtalimanchuk/flask-filebox
- https://github.com/mtalimanchuk/file-squire-bot

It makes file transferring over Internet easier by giving you a tool to share a local directory through the Ngrok network. 
It lists the given directory, creates a local web server with Flask, make this server sharing the listed files and creates an Ngrok tunnel to the port used by the Flask server. 

In other words, parrot-feeder temporarily exposes your files for downloading on the Internet. 
Once you stop parrot-feeder, your files stop being shared over Ngrok.

It also exposes an HTML page under the `/api/upload` path with a form for uploading files to the remote machine.

If you supply the tool with a telegram bot token via the `--telegram-bot-token` argument or 
via the `TELEGRAM_BOT_TOKEN` env variable, 
you will also activate a telegram bot that will `/fetch` or `/tail` files for you from remote.


*Note-1: you also need to supply the `--telegram-bot-whitelist` or `TELEGRAM_BOT_WHITELIST` 
env variable to specify the users allowed to interact with the bot.*

*Note-2: you may need to sign up for Ngrok for tunneling HTML pages.*


## Screenshots or it didn't happen.
![image info](https://i.imgur.com/nZfsTEH.png)


## Installation

Download the Docker image:

```bash
docker pull lep0puglabs/parrot-feeder:latest
```

or build the Docker image yourself:

```bash
docker build -t parrot-feeder -f ./Dockerfile .
```

Run the Docker image:

```bash
docker run --rm -it -p 4200:4200 parrot-feeder
```

Or install the package using PyPI:

```bash
sudo pip3 install parrot-feeder
```

After starting the server, you can navigate to the following URLs:

- / - for seeing the listing
- /api/upload - for accessing the API for uploading files

## Usage

Serve files and folder from the current working directory 

`parrot-feeder`

or 

`docker run --rm -it -p 4200:4200 parrot-feeder`

Serve files and folders from the /tmp directory 

`parrot-feeder --directory /tmp`

Print served files to the console on startup 

`parrot-feeder --directory /tmp -pf`

Bind the server to the given address 

`parrot-feeder --ip 10.10.10.10 --port 5050`

Print help

`parrot-feeder -h`

On startup print the actual files being shared over Ngrok

`parrot-feeder -pf`

Use a telegram bot to serve you files from the remote server:

`parrot-feeder --telegram-bot-token token --telegram-bot-whitelist username1,username2`
