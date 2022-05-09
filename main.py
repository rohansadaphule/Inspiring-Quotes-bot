import discord
import os
import requests
import json
import random
from replit import db

token = os.environ['InspiringQuotesBot_token']
client = discord.Client()

sad_words = [
    'sad', 'frustate', 'frustated', 'frustating', 'bad', 'worse', 'life',
    'grief', 'grieve', 'grieving', 'disgust', 'disgusting', 'depressed',
    'unhappy', 'angry', 'miserable', 'depressing', 'die', 'tension', 'tensed',
    'headache', 'feeling', 'low'
]

starter_encouragements = [
    'Cheer Up!', 'Hang in there friend.', 'You are a great person/bot.',
    'Everything will be fine.'
]

thank_you_list = [
    'thanks',
    'thank you',
    'thx',
    'ty',
]

welcome_words = [
    'Welcome.', "You're Welcome.", 'No problem.', 'Np.', 'WC.',
    'No, Thank You.', 'My pleasure.', "It's my pleasure."
]


def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


# def get_joke():
#   response = requests.get("https://dadjokes.p.rapidapi.com/random/joke")
#   json_data = json.loads(response.text)
#   joke = json_data


@client.event
async def on_ready():
    print("WE have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements
    if "encouragements" in db.keys():
        options.extend(db["encouragements"])

    if any(word in msg.lower() for word in sad_words):
        await message.channel.send(random.choice(options))

    if any(word in msg.lower() for word in thank_you_list):
        await message.channel.send(random.choice(welcome_words))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
          index = int(msg.split("$del",1)[1])
          delete_encouragements(index)
          encouragements = db["encouragements"]
          await message.channel.send(encouragements)
      
client.run(token)
