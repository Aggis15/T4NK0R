from flask import Flask, request, Response
import json
import hmac
import hashlib
from dotenv import load_dotenv, set_key
import os
import requests as r
from discord_webhook import DiscordWebhook, DiscordEmbed
load_dotenv()
import os
from waitress import serve

# Public vars
app = Flask(__name__)
secret = os.environ.get('TWITCH_SECRET')
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
TWITCH_ACCESS_TOKEN = os.environ.get('TWITCH_ACCESS_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
WEBHOOK_URL = DiscordWebhook(url=WEBHOOK_URL)


@app.route("/")
def index():
    return "The website is working!"


@app.route("/twitch/live", methods=["POST"])
def twitchPost():
    requestJson = request.json
    print(request.headers)
    if "webhook_callback_verification" in request.headers["Twitch-Eventsub-Message-Type"]:
        response = Response(requestJson["challenge"], status=200)
        response.headers["Content-Type"] = "application/json"
        return response
    elif "notification" in request.headers["Twitch-Eventsub-Message-Type"]:
        twitchID = request.headers["Twitch-Eventsub-Message-Id"]
        twitchTimestamp = request.headers["Twitch-Eventsub-Message-Timestamp"]
        twitchSignature = request.headers["Twitch-Eventsub-Message-Signature"]
        total_params = twitchID + twitchTimestamp + request.get_data().decode("utf-8")
        signature = hmac.new(secret.encode(), total_params.encode(), hashlib.sha256).hexdigest()
        signature = f"sha256={signature}"
        if signature == twitchSignature:
            print(signature)
            print(twitchSignature)
            userID = requestJson["event"]["broadcaster_user_id"]
            headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"}
            req = r.get(f"https://api.twitch.tv/helix/streams?user_id={userID}", headers=headers)
            if req.status_code == 401:
                print("401. retrying...")
                get_new_key = r.post(f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&grant_type=client_credentials")
                access_token = get_new_key.json()["access_token"]
                set_key(".env", "TWITCH_ACCESS_TOKEN", access_token)
                headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {access_token}"}
                req = r.get(f"https://api.twitch.tv/helix/streams?user_id={userID}", headers=headers)
            req = json.loads(req.text)
            name = req["data"][0]["user_name"]
            game = req["data"][0]["game_name"]
            title = req["data"][0]["title"]
            viewers = req["data"][0]["viewer_count"]
            thumbnail = req["data"][0]["thumbnail_url"]
            embed = DiscordEmbed(
                title=f"{name} is streaming!",
                url=f"https://twitch.tv/{name}",
                description=f"{name} is now live! Come watch and support!",
                colour="00FF00"
            )
            embed.set_image(url=thumbnail.format(width=640, height=360))
            embed.add_embed_field(name="Stream Title", value=title, inline=True)
            embed.add_embed_field(name="Viewers", value=viewers, inline=True)
            embed.add_embed_field(name="Currently Playing", value=game, inline=True)
            WEBHOOK_URL.add_embed(embed)
            WEBHOOK_URL.execute()
            return Response(status=200)

        else:
            print(signature)
            print(twitchSignature)
            print("Signature failed")
            return Response(status=403)
    else:
        return Response(status=403)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080, url_scheme="https")