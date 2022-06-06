import discord
from discord.ext import commands
import config
import not_allowed_words as na
import user

client = discord.Client()

bot = commands.Bot(command_prefix='!')
bot.remove_command('!help')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    user.load_coins()
    user.load_inv()
    user.start_inv_thread()

not_allowed = na.not_allowed


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    contents = message.content
    norm_content = contents.strip().lower()
    if norm_content.startswith("!help"):
        await message.channel.send(
            "Hi! I see you asked what you can do with this bot. Nothing much yet, it's still being developed."
            "\nThe only current exitsing commands are:"
            "\n \t!help = Gives this text."
            "\n \t!ban = bans a user"
            "\nThe only other features are:"
            "\n \tA bad word filter.")

    if norm_content.startswith("!ban"):
        author = message.author
        roles = author.roles
        id_list = []
        for role in roles:
            role_id = role.id
            id_list.append(role_id)
            print("Role  name:{}, ID:{}".format(role.name, role.id))
        admin_id = 803449218701590569
        if admin_id in id_list:
            clean_up_content = contents.strip()
            ban_member = clean_up_content[5:]
            g = client.get_guild(755061738415587328)
            member = g.get_member_named(ban_member)
            if not member:
                print("Could not locate member {} in guild".format(ban_member))
            else:
                print("Located member {}. Attemptting ban.".format(ban_member))
                await member.ban()
                await message.channel.send("Successfully used the ban hammer on {}.".format())
        else:
            await message.channel.send("You do not have permission to use this command!")

    if norm_content.startswith("!start"):
        author = message.author
        key = to_coin_key(author)
        user.add_money(key, 0)
        money = user.get_money(key)
        await message.channel.send("You have created an account for this bot.")
        await message.channel.send("Your balance is ${}.".format(money))

    if contents.startswith("!addmoney"):
        author = message.author
        roles = author.roles
        print(roles)
        admin_role = 766037459791904779
        #if admin_role in roles:
        command = contents
        parts = command.split()
        if parts[1].isnumeric() == True:
            memberstr = to_coin_key(parts[2])
            if user.is_user_registered(memberstr):
                amount = int(parts[1])
                user.add_money(memberstr, amount)
                balance = user.get_money(memberstr)
                await message.channel.send("{}'s balance is now ${}.".format(memberstr, balance))
            elif user.is_user_registered(memberstr) == False:
                await message.channel.send("Member is not registered.")
        else:
            await message.channel.send("Incorrect format, correct format (type without brackets): !addmoney {amount} "
                                       "{user}")
    #else:
        #await message.channel.send("You do not have permision to use this command.")

    if norm_content.startswith("!sell"):
        author = message.author
        authorstr = to_coin_key(author)
        user_coins = user.get_money(authorstr)
        user_inv = user.get_inv(authorstr)
        user.add_money(authorstr, user_coins+user_inv)
        user.set_inv(authorstr, 0)
        new_user_coins = user.get_money(authorstr)
        await message.channel.send("Your new balance is now ${}.".format(new_user_coins))


    if norm_content.startswith("!bal"):
        author = message.author
        authorstr = to_coin_key(author)
        if user.is_user_registered(authorstr) == True:
            mbalance = user.get_money(authorstr)
            ibalance = user.get_inv(authorstr)
            await message.channel.send("Your balance is ${}.".format(mbalance))
            await message.channel.send("You currently have {} ore in you inventory. Use !sell to sell!".format(ibalance))
        else:
            await message.channel.send("You have not registered! Use !start to register.")

    if any(word in norm_content for word in not_allowed):
        author = message.author
        pchannel = message.channel
        await message.delete()
        await message.channel.send('For this to be a friendly server, NO inappropriate language is allowed. '
                                   'Admin will ban/kick/warn/mute you as a punishment in some time {}.'.format(author),
                                   tts=True)
        channel = client.get_channel(980999567455711304)
        await channel.send("INAPPROPRIATE LANGUAGE SAID IN {} by {}.".format(pchannel, author))


def to_coin_key(member):
    return "{}".format(member)


cfg = config.AppConfig()
token = cfg.get_discord_bot_key()
client.run(token)
