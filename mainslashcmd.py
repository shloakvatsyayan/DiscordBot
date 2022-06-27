import interactions
import config

cfg = config.AppConfig()
token = cfg.get_discord_slash_bot_key()
bot = interactions.Client(token=token)


@bot.command(name="help", description="Help command.", scope=755061738415587328)
async def handle_help_command(ctx: interactions.CommandContext):
    await ctx.send(
        "Hi! I see you asked what you can do with this bot. The currently running code is just started developement "
        "so only two commands exist so far."
        "\nThe only current exitsing commands are:"
        "\n \t/help = Gives this text."
        "\n \t/test = Sends a test message.", ephemeral=True)


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
    await ctx.send("This test was successful, '{}' was entered into the required text field.".format(text), ephemeral=True)


bot.start()
