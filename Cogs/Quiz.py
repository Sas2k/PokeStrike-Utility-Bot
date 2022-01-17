import discord
from discord.ext import commands
import asyncio
import pymongo
from random import randint, randrange
from dotenv import load_dotenv
import os

load_dotenv("Cogs/.env")

psw = os.environ["MONGOPSW"]
client = pymongo.MongoClient(f"mongodb+srv://QuizWriter:{psw}@pokequiz.vi6j1.mongodb.net/PokeQuiz?retryWrites=true&w=majority")
db = client.Quiz
collection = db.PokeQuiz

class Quiz(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

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
                for ans in range(0, len(answer)-1):
                    if ans == msg.lower():
                        return True
                    else:
                        pass
            else:
                answer = str(question.get('answer'))
                return msg.lower() == answer
        try:
            mesg = await self.bot.wait_for('message', timeout=30.0, check=check)
            if mesg:
                await ctx.send(f"You got it {mesg.author.mention}, answer(s) are {question.get('answer')}")
        except asyncio.TimeoutError:
            membed = discord.Embed(title=f"Time Up. Nobody has solved it.", description=f"The answer(s) is/are {question.get('answer')}", colour=color)
            await ctx.send(embed=membed)

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
            await ctx.send("This question is already in the database ")
        
    @commands.command(name = "all_quiz",
                    brief="shows all of the quizez",
                    description = "Shows All of the quizez in the database")
    async def commandName(self, ctx:commands.Context):
        document = list(collection.find({}, {"_id": 0, "question": 1}))
        mesg = ""
        for x in range(0, len(document)):
            question = document[x]
            mesg += f"[{x+1}] {question.get('question')}\n\n"
        color = f'{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}'
        color = int(color, 16)
        embed = discord.Embed(title="Questions ❓", description=mesg, colour=color)
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Quiz(bot))