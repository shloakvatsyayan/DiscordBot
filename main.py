import discord
from discord.ext import commands
import time
import config
import not_allowed_words as na

client = discord.Client()

bot = commands.Bot(command_prefix='!')
bot.remove_command('!help')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


not_allowed = na.not_allowed


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    contents = message.content
    norm_content = contents.strip().lower()
    if norm_content.startswith('!ssvf112playzsite'):
        await message.channel.send(
            'Hi! I am a Discord bot SSVF112 Playz made. Here is the website: https://ssvf112playz.wixsite.com/website')

    if norm_content.startswith("!help"):
        await message.channel.send(
            "Hi! I see you asked what you can do with this bot. Nothing much yet, it's still being developed."
            "\nThe only current exitsing commands are:"
            "\n \t!ssvf112playzsite = Gives the link to the channel website made on wix.com"
            "\n \t!help = Gives this text."
            "\nThe only other features are:"
            "\n \tA bad word filter. Currently only filters 2 bad words."
            "\n \tA message when you say !play because music bot(Rythm) was removed."
            "\nBot made by SSVF112 Playz.")

    if norm_content.startswith("!ban"):
        author = message.author
        roles = author.roles
        id_list = []
        for role in roles:
            role_id = role.id
            id_list.append(role_id)
            print("Role  name:{}, ID:{}".format(role.name, role.id))
        admin_id = 708353267188629586
        if admin_id in id_list:
            await message.channel.send(
                "Please enter the name of the name with # number of the user to ban (ex:SSVF112 Playz YT#3323)."
                "\n This may take a minute.")
            time.sleep(30)
            ban_user = norm_content
            await ban_user.ban(reason="Banned by {} with SSVF112 Playz Bot".format(ban_user), delete_message_days=7)
            await message.channel.send("Hey {}! I successfully used the ban hammer on {}.".format(author,ban_user))
        else:
            await message.channel.send("You do not have permission to use this command!")

    if norm_content.startswith('!play'):
        await message.channel.send(
            "Sorry for the inconvenience, Music Bot was removed from this server and will be added back soon.")

    if any(word in norm_content for word in not_allowed):
        author = message.author
        pchannel = message.channel
        await message.delete()
        await message.channel.send('For this to be a friendly server, NO inappropriate language is allowed. '
                                   'Admin will ban/kick/warn/mute you as a punishment in some time {}.'.format(author),
                                   tts=True)
        channel = client.get_channel(708354188643401799)
        await channel.send("INAPPROPRIATE LANGUAGE SAID IN {} by {}.".format(pchannel, author))


cfg = config.AppConfig()
token = cfg.get_discord_bot_key()
client.run(token)
