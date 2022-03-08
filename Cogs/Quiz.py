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
async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except discord.Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except discord.Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

class Quiz(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name= "quiz",
                    help="Asks a Pokemon related question from the database")
    async def quiz(self, ctx:commands.Context):
        document = list(collection.find({}, {'_id': 0}))
        qn = randint(0, len(document)-1)
        question = document[qn]
        answer = str(question.get('answer'))
        color = f'{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}'
        color = int(color, 16)
        embed = discord.Embed(title=f"[{qn+1}]{question.get('question')}", description="Answer this you have 30 secs", colour=color)
        await send_embed(ctx, embed)
        def check(m):
            msg = m.content
            if '/' in question.get('answer'):
                answer = str(question.get('answer'))
                answerr = answer.split('/')
                if msg.lower() == answerr[0]:
                    return True
                elif msg.lower() == answerr[1]:
                    return True
                elif msg.lower() == answer:
                    return True
                else:
                    return False
            else:
                answer = str(question.get('answer'))
                return msg.lower() == answer
        try:
            mesg = await self.bot.wait_for('message', timeout=30.0, check=check)
            if mesg:
                if '/' in answer:
                    answer = answer.replace('/', ', ')
                await ctx.send(f"You got it {mesg.author.mention}, answer(s) are {answer}")
        except asyncio.TimeoutError:
            if '/' in answer:
                answer = answer.replace('/', ', ')
            membed = discord.Embed(title=f"Time Up. Nobody has solved it.", description=f"The answer(s) is/are {question.get('answer')}", colour=color)
            await send_embed(ctx, membed)

    @commands.command(name="add_quiz",
                    help="Adds a pokemon related quiz to the database, `add_quiz 'question' 'answer[if there are 2 answers put a / between]'`",
                    usage="Question Answer")
    async def add_quiz(self, ctx:commands.Context, question: str, answer: str):
        question = question.lower()
        answer = answer.lower()
        myquery = { "question": question }
        if collection.count_documents(myquery) == 0:
            post = {"question": question,
                    "answer": answer}
            collection.insert_one(post)
            await ctx.send("Accepted")
        else:
            await ctx.send("This question is already in the database ")
        
    @commands.command(name = "all_quiz",
                    help = "Shows All of the quizez in the database")
    async def commandName(self, ctx:commands.Context):
        document = list(collection.find({}, {"_id": 0, "question": 1}))
        mesg = ""
        for x in range(0, len(document)):
            question = document[x]
            mesg += f"[{x+1}] {question.get('question')}\n\n"
        color = f'{randrange(16**2):x}{randrange(16**2):x}{randrange(16**2):x}'
        color = int(color, 16)
        embed = discord.Embed(title="Questions ❓", description=mesg, colour=color)
        await send_embed(ctx, embed)

def setup(bot:commands.Bot):
    bot.add_cog(Quiz(bot))
