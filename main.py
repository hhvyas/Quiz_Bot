import discord
import html
import random
import urllib.request, json 
# API Fetch
with urllib.request.urlopen("https://opentdb.com/api.php?amount=50&type=multiple") as url:
    data = json.loads(url.read().decode())

playerScore = {
  #Will Contain Player Scored, in Dictionary
}
ArrChoice = []
act_user = "NONE"
client = discord.Client()
rnd = 0
cnt = 0
timedel = 0

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  global timedel
  global act_user
  global ArrChoice
  global rnd
  global cnt
  username = str(message.author).split("#")[0]
  # If a player is answering and someone writes !quiz, but if leftSec > 5 than discard previous partipant
  if str(act_user) != "NONE" and str(username) != act_user and str(message.content) == "!quiz":
    timedel += 1
    if timedel > 4:
      act_user = "NONE"
      timedel = 0
      await message.channel.send("!quiz to play")
      ArrChoice.clear()
      return
    await message.channel.send(username + " Please Wait! or Ask for Quiz " +  str(5 - timedel) + " times incase " + act_user + " is Offline")
    return
  if message.content == "!quiz" and act_user == username:
    await message.channel.send("Answer before asking Next Question")
    return
  if message.content == "!quiz":
    act_user = username
    if not username in playerScore:
      playerScore[username] = 0
    rnd = random.randint(0, 49)
    Question = html.unescape(data['results'][rnd]['question'])
    await message.channel.send("Question: " + Question)
    ArrChoice.append(html.unescape(data['results'][rnd]['correct_answer']))
    for i in range (0, 3):
      ArrChoice.append(html.unescape(data['results'][rnd]['incorrect_answers'][i]))
    #print(list(ArrChoice))
    random.shuffle(ArrChoice)
    #print(list(ArrChoice))
    option = "A"
    for word in ArrChoice:
      print(word)
      await message.channel.send(chr(ord(option) + cnt) + ") " + word)
      cnt += 1
    cnt = 0
    return
  if (len(message.content) > 1):
    return
  curr_ans = str(html.unescape(data['results'][rnd]['correct_answer']))
  usr_ans = ArrChoice[ord(message.content.upper()) - 65]
  if username == act_user:
    if curr_ans == usr_ans:
      #print("Hey")
      await message.channel.send("Correct!")
      #Score Calculation
      playerScore[act_user] += 1
      await message.channel.send("::Leaderboard::")
      act_user = "NONE"
      ArrChoice.clear()

      for ok in playerScore:
        await message.channel.send(str(ok) + " --> " + str(playerScore[ok]))
      return
    await message.channel.send("Incorrect!")
    await message.channel.send("Correct Answer is " + curr_ans)
    ArrChoice.clear()
    await message.channel.send("::Leaderboard::")
    for ok in playerScore:
      await message.channel.send(str(ok) + " --> " + str(playerScore[ok]))
    act_user = "NONE"
    return
client.run('Token')