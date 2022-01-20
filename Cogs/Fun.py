import discord
from discord.ext import commands
from random import randint
import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "coin",
                    usage="@the_person_who_chose_heads(optional) @the_person_who_chose_tails(optional)",
                    brief="Flips a coin",
                    description = "flips a coin, the first person is heads, the second person is tails")
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
                    brief="rolls a dice",
                    description="rolls a 6 sided dice if the amount sides aren't put")
    async def roll(self, ctx:commands.Context, sides: int = None):
        if sides == None:
            dice = randint(1, 6)
            await ctx.send(f"🎲 is rolled and it lands on {dice}")
        else:
            dice = randint(1, sides)
            await ctx.send(f"A 🎲({sides}) is rolled by {ctx.author.mention} and lands on {dice}")
        
    @commands.command(name = "simulate",
                    aliases=["sim"],
                    usage="rule-number(0-255) postion[right, left, center] initial-condition[random, impule(starts with 1 cell)",
                    brief="simulates a cells",
                    description = "Simulates a rule of an elementry cellular automaton")
    async def commandName(self, ctx:commands.Context, rule, position, init_cond):
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

        await ctx.send(file=discord.File("/Cogs/elementary_cellular_automaton.png"))

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))