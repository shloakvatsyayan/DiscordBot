import time
import discord
import interactions
from discord.ext import commands
import config
import random
import not_allowed_words as na
import database as d
import requests

cfg = config.AppConfig()
token = cfg.get_discord_bot_key()

client = discord.Client()
user_db = d.Database()

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")


@bot.event
async def on_ready():
    import user
    print('Logged in as {0.user}'.format(bot))
    user.load_coins()
    user.load_inv()


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    author = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    labels = na.check_message(ctx)
    print(labels)
    labels_dict = {}
    for d in labels:
        labels_dict[d['label']] = d['level']
    print(labels_dict)
    if labels_dict["PROFANITY"] > 0:
        await author.add_roles(role)
    elif labels_dict["NSFW"] > 0:
        await author.add_roles(role)
    elif labels_dict["PERSONAL_INFO"] > 0:
        await author.add_roles(role)
    elif labels_dict["TOXIC"] > 0:
        msg_channel = ctx.channel
        channel = bot.get_channel(980999567455711304)
        await channel.send("Possibly toxic behavior detected by {} in {}.".format(author, msg_channel))
    else:
        pass

@bot.command(name="help")
async def handle_help_command(ctx):
    await ctx.send(
        "Hi! I see you asked what you can do with this bot. Nothing much yet, it's still being developed."
        "\nThe only current existing commands are:"
        "\n \t$help = Gives this text."
        "\n \t$ban = bans a user."
        "\n \t$start registers you into the currency system."
        "\n \t$bal or !balance tells you you're balance."
        "\n \t$sell sells your ore for money."
        "\n \t$calc solves simple math problems like 3-2. "
        "NOTE: You have to put spaces between the symbol and numbers else it will break. Supported actions: +, -, *, "
        "/, and rt "
        "\n \tSome other $sudo commands."
        "\nThe only other features are:"
        "\n \tA Profanity, toxic, NSFW, and personal info filter.")


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
    elif command == "delete":
        await ctx.send("Deleted {} from existence.".format(target))


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


@bot.command(name="balance", description="Tells you balance.")
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


@bot.command(name="sell", )
async def handle_sell_command(ctx):
    author = ctx.author
    auth_str = to_coin_key(author)
    if auth_str in user_db.coins:
        user_coins = user_db.get_money(auth_str)
        user_inv = user_db.get_inv(auth_str)
        user_db.add_money(auth_str, user_coins + user_inv)
        user_db.set_inv(auth_str, 0)
        new_user_coins = user_db.get_money(auth_str)
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


@bot.command(name="calc")
async def handle_calculator_cmd(ctx, a, sign, b):
    a = int(a)
    b = int(b)
    if sign == "+":
        c = a+b
        await ctx.send("The answer is {}.".format(c))
    if sign == "-":
        c = a - b
        await ctx.send("The answer is {}.".format(c))
    if sign == "*":
        c = a*b
        await ctx.send("The answer is {}.".format(c))
    if sign == "/":
        c = a/b
        await ctx.send("The answer is {}.".format(c))
    if sign == "^":
        c = a**b
        await ctx.send("The answer is {}.".format(c))
    if sign == "rt":
        c = a**(1/b)
        await ctx.send("The answer is {}.".format(c))

def to_coin_key(member):
    return "{}".format(member)


bot.run(token)