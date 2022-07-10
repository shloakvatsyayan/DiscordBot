import interactions
import discord
import config
import not_allowed_words as na

cfg = config.AppConfig()
token = cfg.get_discord_slash_bot_key()
bot = interactions.Client(token=token)

@bot.event()
async def on_ready():
    print("Bot has started.")


@bot.event()
async def on_message(ctx):
    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
    print("hi")
    """
    author = ctx.author
    labels = na.check_message(ctx)
    print(labels)
    labels_dict = {}
    for d in labels:
        labels_dict[d['label']] = d['level']
    print(labels_dict)
    if labels_dict["PROFANITY"] > 0:
        bot.addroles(author, 983051103585312818)
    """

@bot.command(name="help", description="Help command.", scope=755061738415587328)
async def handle_help_command(ctx: interactions.CommandContext):
    await ctx.send(
        "Hi! I see you asked what you can do with this bot. The currently running code is just started development "
        "so only two commands exist so far."
        "\nThe only current existing commands are:"
        "\n \t/help = Gives this text."
        "\n \t/test = Sends a test message."
        "\n \t/technoblade = A Technoblade memorial command.", ephemeral=True)


@bot.command(name="technoblade", description="A Technoblade memorial command.", scope=755061738415587328)
async def handle_techno_command(ctx: interactions.CommandContext):
    await ctx.send("May Technoblade aka. Alex rest in peace. He ment a lot to all of us. "
                   "Although he might be dead, Technoblade truly never dies. "
                   "He will remain in our hearts forever, till the end.")


@bot.command(
    name="test",
    description="A testing command",
    scope=755061738415587328,
    options=[
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def handle_test_command(ctx: interactions.CommandContext, text: str):
    await ctx.send("This test was successful, '{}' was entered into the required text field.".format(text))


bot.start()