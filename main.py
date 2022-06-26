import time

import discord
from discord.ext import commands
import config
import not_allowed_words as na
import database as d
import requests

client = discord.Client()
user_db = d.Database()

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")


@bot.command(name="joke")
async def handle_joke_command(ctx):
    """
    See TestJokesAPI for learning how to use this
    :param ctx:
    :return:
    """

    await ctx.send("No Jokes!")


"""
@client.event
async def on_ready():
    import user
    print('Logged in as {0.user}'.format(client))
    user.load_coins()
    user.load_inv()
    # user.start_inv_thread()
"""

not_allowed = na.not_allowed


# @client.event
async def on_message(message):
    if message.author == client.user:
        return

    contents = message.content
    norm_content = contents.strip().lower()

#    if norm_content.startswith("!help"):
#        await handle_help_command(user_db, message)

#    if norm_content.startswith("!ban"):
#        await handle_ban_command(user_db, contents, message)

#    if norm_content.startswith("!start"):
#        await handle_start_command(user_db, message)

#    if contents.startswith("!addmoney"):
#        await handle_add_money_command(user_db, contents, message)

#    if norm_content.startswith("!sell"):
#        await handle_sell_command(user_db, message)

#    if norm_content.startswith("!bal"):
#        await handle_balance_command(user_db, message)

    if any(word in norm_content for word in not_allowed):
        await handle_banned_words_command(user_db, message)


#    if contents.startswith("$sudo "):
#        await handle_sudo_command(contents, message)


@bot.command(name="help")
async def handle_help_command(ctx):
    await ctx.send(
        "Hi! I see you asked what you can do with this bot. Nothing much yet, it's still being developed."
        "\nThe only current exitsing commands are:"
        "\n \t!help = Gives this text."
        "\n \t!ban = bans a user (not working)."
        "\n \t!start registers you into the currency system."
        "\n \t!bal or !balance tells you you're balance."
        "\n \t!sell sells your ore for money."
        "\n \tSome other $sudo commands."
        "\nThe only other features are:"
        "\n \tA bad word filter (disabled until API added).")


@bot.command(name="sudo")
async def handle_sudo_command(ctx, command, target):
    author = ctx.author
    if command == "heck":
        await ctx.send("hecked {} through hecker terminal".format(target))
    elif command == "destroy":
        await ctx.send("hecking {}".format(target))
        time.sleep(1)
        await ctx.send("hecked {}".format(target))
        time.sleep(1)
        await ctx.send("destroying {}".format(target))
        time.sleep(1)
        await ctx.send("❌{} was destroyed by {}".format(target, author))


async def handle_banned_words_command(user_database, message):
    author = message.author
    pchannel = message.channel
    await message.delete()
    await message.channel.send('For this to be a friendly server, NO inappropriate language is allowed. '
                               'Admin will ban/kick/warn/mute you as a punishment in some time {}.'.format(author),
                               tts=True)
    channel = client.get_channel(980999567455711304)
    await channel.send("INAPPROPRIATE LANGUAGE SAID IN {} by {}.".format(pchannel, author))

@bot.command(name="bal")
async def handle_bal_command(ctx):
    author = ctx.author
    authorstr = to_coin_key(author)
    if user_db.is_user_registered(authorstr) == True:
        mbalance = user_db.get_money(authorstr)
        ibalance = user_db.get_inv(authorstr)
        await ctx.send("Your balance is ${}.".format(mbalance))
        await ctx.send(
            "You currently have {} ore in you inventory. You earn 1 ore per second. Use !sell to sell!".format(
                ibalance))
    else:
        await ctx.send("You have not registered! Use !start to register.")

@bot.command(name="balance")
async def handle_balance_command(ctx):
    author = ctx.author
    authorstr = to_coin_key(author)
    if user_db.is_user_registered(authorstr) == True:
        mbalance = user_db.get_money(authorstr)
        ibalance = user_db.get_inv(authorstr)
        await ctx.send("Your balance is ${}.".format(mbalance))
        await ctx.send(
            "You currently have {} ore in you inventory. You earn 1 ore per second. Use !sell to sell!".format(
                ibalance))
    else:
        await ctx.send("You have not registered! Use !start to register.")

@bot.command(name="sell")
async def handle_sell_command(ctx):
    author = ctx.author
    authorstr = to_coin_key(author)
    if authorstr in user_db.coins:
        user_coins = user_db.get_money(authorstr)
        user_inv = user_db.get_inv(authorstr)
        user_db.add_money(authorstr, user_coins + user_inv)
        user_db.set_inv(authorstr, 0)
        new_user_coins = user_db.get_money(authorstr)
        await ctx.send("Your new balance is now ${}.".format(new_user_coins))
    else:
        await ctx.send("You are not registered. Use !start to register and be able to use this command.")

@bot.command(name="addmoney")
async def handle_add_money_command(ctx, a, u):
    author = ctx.author
    roles = author.roles
    id_list = []
    for role in roles:
        id_list.append(role.id)
        print("Role  name:{}, ID:{}".format(role.name, role.id))
    admin_role = 766037459791904779
    if admin_role in id_list:
        if a.isnumeric() == True:
            memberstr = to_coin_key(u)
            if user_db.is_user_registered(memberstr):
                amount = int(a)
                user_db.add_money(memberstr, amount)
                balance = user_db.get_money(memberstr)
                await ctx.channel.send("{}'s balance is now ${}.".format(memberstr, balance))
            elif user_db.is_user_registered(memberstr) == False:
                await ctx.send("Member is not registered.")
        else:
            await ctx.send("Incorrect format, correct format (type without brackets): !addmoney {amount} "
                                       "{user}")
    else:
        await ctx.send("You do not have permision to use this command.")

@bot.command(name="start")
async def handle_start_command(ctx):
    author = ctx.author
    key = to_coin_key(author)
    user_db.add_money(key, 0)
    money = user_db.get_money(key)
    await ctx.send("You have created an account for this bot.")
    await ctx.send("Your balance is ${}.".format(money))

@bot.command(name="ban")
async def handle_ban_command(ctx, ban_member: discord.Member):
    author = ctx.author
    roles = author.roles
    id_list = []
    for role in roles:
        role_id = role.id
        id_list.append(role_id)
        print("Role  name:{}, ID:{}".format(role.name, role.id))
    admin_id = 803449218701590569
    if admin_id in id_list:
        await ban_member.ban()
        await ctx.send("Successfully used the ban hammer on {}.".format(ban_member))
    else:
        await ctx.send("You do not have permission to use this command!")


def to_coin_key(member):
    return "{}".format(member)


cfg = config.AppConfig()
token = cfg.get_discord_bot_key()
bot.run(token)
# client.run(token)
