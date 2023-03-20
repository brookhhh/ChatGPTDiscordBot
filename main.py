import openai
import discord
import sqlite3

token = "str"

openai.api_key = "str"

print(f'should be working in a second')


class ChatAI(discord.Client):

    async def on_ready(self):
        print(f"bot online")

    async def on_message(self, message):

        if message.author == self.user:
            return

        if client.user.mentioned_in(message):

            print(f"pray it works ")

            # sqlite database
            conn = sqlite3.connect('conversation_history.db')
            cursor = conn.cursor()

            print(f"database connected")

            # create the conversation history table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                              (user_id TEXT, question TEXT, response TEXT)''')
            conn.commit()

            print(f"conversation history table existing/created")

            # function to get the conversation history for a user
            def get_conversation_history(user_id):
                cursor.execute('SELECT question, response FROM conversation_history WHERE user_id=?', (user_id,))
                rows = cursor.fetchall()
                if not rows:
                    return []
                return [{'question': row[0], 'response': row[1]} for row in rows]

            print(f"conversation history func 1 done")

            # function to add a question and response to the conversation history for a user
            def add_to_conversation_history(user_id, question, response):
                cursor.execute('INSERT INTO conversation_history VALUES (?, ?, ?)', (user_id, question, response))
                conn.commit()

            print(f"conversation history func 2 done")

            # making the prompt
            prompt = "Gaynor is a hunky, dominant acting male who is a whopper eater and likes to converse with users.\n"
            prompt += "\n".join([qa["question"]+'\n'+qa["response"] for qa in get_conversation_history(user_id=message.author.id)])
            prompt += "\n You: " + message.content + "\n Gaynor:"

            print(f"prompt created")

            # generating the response
            responseA = openai.Completion.create(
             model="text-davinci-003",
             temperature=1.5,
             prompt=prompt,
             max_tokens=60,
             top_p=0.5,
             frequency_penalty=1,
             presence_penalty=0.0,
             stop=[" You:", " Gaynor:"],
            )

            # printing to diagnose any issues with the prompt
            print(responseA)

            # adding to the locally stored memory
            add_to_conversation_history(message.author.id, message.content, responseA.choices[0].text.strip())

            # send response to chat
            await message.channel.send(responseA.choices[0].text.strip(), reference=message)

            print(f"ok should've worked\n", get_conversation_history(user_id=message.author.id), "\n\n amazing and finished")


client = ChatAI()
client.run(token)
