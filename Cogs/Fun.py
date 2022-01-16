import asyncio
import discord
from discord.ext import commands
from random import randint, randrange
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

if os.path.isfile('./.env'):
    load_dotenv('Cogs/.env')
else:
    pass

psw = os.environ['mongopsw']
client = MongoClient(f"mongodb+srv://QuizWriter:{psw}@pokequiz.vi6j1.mongodb.net/PokeQuiz?retryWrites=true&w=majority")
db = client.Quiz
collection = db.PokeQuiz

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
            await ctx.send(f"A 🎲({sides}) is rolled and lands on {dice}")

    @commands.command(name= "quiz",
                    brief="asks a random pokemon related quiz",
                    description="Asks a Pokemon related question from the database")
    async def quiz(self, ctx:commands.Context):
        document = list(collection.find({}, {'_id': 0}))
        qn = randint(0, len(document)-1)
        question = document[qn]
        color = f'{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}'
        color = int(color, 16)
        embed = discord.Embed(title=f"[{qn+1}]{question.get('question')}", description="Answer this you have 30 secs", colour=color)
        await ctx.send(embed=embed)
        def check(m):
            msg = m.content
            if '/' in question.get('answer'):
                answer = str(question.get('answer'))
                answer = answer.split('/')
            return msg.lower() == answer[0] or msg.lower() == answer[1]
        try:
            mesg = self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            ctx.send("Time Out!")
        else:
            ctx.send(f"You got it {mesg.author}, answer(s) are {question.get('answer')}")

        

    @commands.command(name="add_quiz",
                    brief="Adds a pokemon quiz",
                    description="Adds a pokemon related quiz to the database",
                    usage="Question Answer")
    async def add_quiz(self, ctx:commands.Context, question: str, answer: str):
        question = question.lower()
        answer = answer.lower()
        myquery = { "question": question }
        if collection.count_documents(myquery) == 0:
            post = {"question": question,
                    "answer": answer}
            collection.insert_one(post)
        else:
            ctx.send("This question is already in the database ")

def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))