# Delulu Gen

A text-based game that leverages OpenAI's GPT-4 framework to generate a game that is unique to each player. Players define the setting of the game they want to play, and GPT-4 generates a character for them and gives the player an immersive experience.

![](https://i.imgur.com/jV8drGv.png)
![](https://i.imgur.com/mrHg2ZQ.png)

## Dependencies
* python 3
* A valid OpenAI key (get one [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key))

## Running instructions
* Install the openai and tkinter python packages
  * `pip install openai tk`
* Add your OpenAI key to the file `openai_key`
* Make sure you add some money to your OpenAI account so that the app can make GPT-4 requests
* Run the game using the following command
  * `python game_frontend.py`

## How to Play

Type in the setting you want for your game in the text input box at the bottom of the screen and either press enter or click on the send button. Once GPT-4 generates your character, you can do whatever you want. Just tell GPT-4 what you want to do in the text box at the bottom.

## Project details
The project uses the GPT-4 framework from OpenAI to generate all the details of this game. It is initially told that it will control the game and has to generate the players characters and stats. I wanted to display the user's stats and the current items they had as part of the UI, so to facilitate this, I also told GPT-4 that it would need to add the struct `ITEMSTATS: {Health: \<health>, SP: \<sp>, Items: []}` to the end of each of its messages. By using string processing in python, I am able to extract this data and show it in the UI. Sometimes GPT-4 forgets to include this in its responses so I ask it to give it to me again, and if it still doesn't work I display an error and ask the user to retry.

As for the UI of the project, I use a library called tkinter to create all of the UI. I separated all the frontend code into the file `game_frontend.py` and all the backend code into the file `game_backend.py`. I wanted the game to be fun and for the program to feel like it was alive, so I added an emoji under the log of the messages between the user and GPT-4. I send the message that GPT-4 returned to me back to it and tell it to tell me what kind of sentiment the text is displaying. It returns `H` for happy, `S` for sad, `A` for angry, and `N` for neutral. After my program receives the response, it randomly picks an emoji that shows the specified emotion. Just in case I got a bad response from GPT-4, I also included emojis that showed confusion. 

The inspiration for this project was that I've seen a lot of games that say that they react to player choice and that everything you do matters to the story, but I feel like no computer game every comes close to it. The only thing that I would consider to be like that is Dungeons and Dragons, where a human is the one that creates the world and everything in it, so they can change everything based on what the players do. I wanted to replicate something like that in this game, where instead of a human making everything, AI creates it. I have notices in testing that the things GPT-4 generates feels a little similar, but I feel that this is a good proof of concept that a game that truly reacts to all of your choices could be in our future.