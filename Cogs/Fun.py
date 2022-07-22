import discord
from discord.ext import commands
from random import randint, randrange
import numpy as np
import matplotlib.pyplot as plt
import asyncio

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except discord.Forbidden:
        try:
            await ctx.send("Heym seems like, I can't send embeds. Please check my permissions :)")
        except discord.Forbidden:
            await ctx.author.send(f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\nMay you inform the server team about this issue? :slight_smile:" , embed=embed)

powers_of_two = np.array([[4], [2], [1]])  # shape (3, 1)

def step(x, rule_binary):
    """Makes one step in the cellular automaton.
    Args:
        x (np.array): current state of the automaton
        rule_binary (np.array): the update rule
    Returns:
        np.array: updated state of the automaton
    """
    x_shift_right = np.roll(x, 1)  # circular shift to right
    x_shift_left = np.roll(x, -1)  # circular shift to left
    y = np.vstack((x_shift_right, x, x_shift_left)).astype(np.int8)  # stack row-wise, shape (3, cols)
    z = np.sum(powers_of_two * y, axis=0).astype(np.int8)  # LCR pattern as number

    return rule_binary[7 - z]

def cellular_automaton(rule_number, size, steps,
                       init_cond='random', impulse_pos='center'):
    """Generate the state of an elementary cellular automaton after a pre-determined
    number of steps starting from some random state.
    Args:
        rule_number (int): the number of the update rule to use
        size (int): number of cells in the row
        steps (int): number of steps to evolve the automaton
        init_cond (str): either `random` or `impulse`. If `random` every cell
        in the row is activated with prob. 0.5. If `impulse` only one cell
        is activated.
        impulse_pos (str): if `init_cond` is `impulse`, activate the
        left-most, central or right-most cell.
    Returns:
        np.array: final state of the automaton
    """
    assert 0 <= rule_number <= 255
    assert init_cond in ['random', 'impulse']
    assert impulse_pos in ['left', 'center', 'right']
    
    rule_binary_str = np.binary_repr(rule_number, width=8)
    rule_binary = np.array([int(ch) for ch in rule_binary_str], dtype=np.int8)
    x = np.zeros((steps, size), dtype=np.int8)
    
    if init_cond == 'random':  # random init of the first step
        x[0, :] = np.array(np.random.rand(size) < 0.5, dtype=np.int8)

    if init_cond == 'impulse':  # starting with an initial impulse
        if impulse_pos == 'left':
            x[0, 0] = 1
        elif impulse_pos == 'right':
            x[0, size - 1] = 1
        else:
            x[0, size // 2] = 1
    
    for i in range(steps - 1):
        x[i + 1, :] = step(x[i, :], rule_binary)
    
    return x

class Fun(commands.Cog):
    """The fun commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "coin",
                    usage="@the_person_who_chose_heads(optional) @the_person_who_chose_tails(optional)",
                    help="flips a coin, `@the_person_who_chose_heads(optional) @the_person_who_chose_tails(optional)`")
    async def coin(self, ctx:commands.Context, heads = None, tails = None):
        coin = randint(1,2)
        if heads == None:
            if coin == 1:
                await ctx.send("the :coin: was flippped and lands on 🤕")
            else:
                await ctx.send("the :coin: was flipped and lands on 🦖")
        else:
            if coin == 1:
                await ctx.send(f"the :coin: was flippped and lands on 🤕 and {heads} wins")
            else:
                await ctx.send(f"the :coin: was flipped and lands on 🦖 and {tails} wins")
    
    @commands.command(name = "roll",
                    usage="sides(optional)",
                    help="rolls a dice `sides (optional)`")
    async def roll(self, ctx:commands.Context, sides: int = None):
        if sides == None:
            dice = randint(1, 6)
            await ctx.send(f"🎲 is rolled and it lands on {dice}")
        else:
            dice = randint(1, sides)
            await ctx.send(f"A 🎲({sides}) is rolled by {ctx.author.mention} and lands on {dice}")
        
    @commands.command(name = "simulate",
                    aliases=["sim"],
                    help="Simulates a elementry cellular automaton `rule-number(0-255) postion[right, left, center] initial-condition[random, impule(starts with 1 cell`")
    async def commandName(self, ctx:commands.Context, rule: int, position: str, init_cond: str):
        rule_number = rule  # select the update rule
        size = 100  # number of cells in one row
        steps = 100  # number of time steps
        impulse_pos=position  # start with the center cell

        x = cellular_automaton(rule_number, size, steps, init_cond, impulse_pos)
        fig = plt.figure(figsize=(10, 10))

        ax = plt.axes()
        ax.set_axis_off()

        ax.imshow(x, interpolation='none',cmap='YlGnBu')

        plt.savefig('elementary_cellular_automaton.png', dpi=300, bbox_inches='tight')

        await ctx.send(file=discord.File("elementary_cellular_automaton.png"))

    @commands.command(name="number-guess",
                      aliases = ["ng"],
                      help="A number guessing game, you will have 1 minute to guess the number,\n`min-num max-num`")
    async def number_guess(self, ctx: commands.Context, min_num: int, max_num: int):
        embed = discord.Embed(title=f"Guess the Number", description=f"You have 60 secs, range {min_num}~{max_num}", color=int(f"{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}", 16)) 
        chosen_num = randint(int(min_num), int(max_num))
        await send_embed(ctx, embed)
        def check(m) -> bool:
            msg = m.content
            return msg == str(chosen_num)
        try:
            resp_msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            if resp_msg:
                await ctx.send(f"You got it {resp_msg.author.mention}, Number: {chosen_num}")
        except asyncio.TimeoutError:
            timeOut_embed = discord.Embed(title="Times Up!⏱", description=f"Nobody Guessed it. Answer: {chosen_num}", color=int(f"{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}", 16))
            await send_embed(ctx, timeOut_embed)

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))
