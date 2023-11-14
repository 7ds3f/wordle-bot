import discord
import discord.ext.commands

async def display_msg_embed(
    obj: discord.ext.commands.Context | discord.Interaction | discord.Thread,
    *,
    title: str,
    message: str,
    color: discord.Color,
    ephemeral: bool = True
) -> None:
    """
    A helper function that displays an embed to three different objects: a context, an
    interaction, and a thread.
    
    This function helps ease the tedious task of creating an embed. It allows you to make
    embeds visible only to one user, and it allows you to attach a few strings such as a
    title and message.
    """
    embed = discord.Embed(
        title = title,
        description = message,
        color = color
    )
    if isinstance(obj, discord.Interaction):
        # Raises an error if we had already responded to the interaction. So, if it has
        # been responded, we just follow it up with another response.
        if obj.response.is_done():
            await obj.followup.send(
                embed = embed,
                ephemeral = ephemeral
            )
        else:
            await obj.response.send_message(
                embed = embed,
                ephemeral = ephemeral
            )
    elif isinstance(obj, discord.ext.commands.Context):
        await obj.send(
            embed = embed,
            ephemeral = ephemeral
        )
    elif isinstance(obj, discord.Thread):
        await obj.send(embed=embed)
    else:
        raise ValueError('obj is not of type Context, Interaction, or Thread')