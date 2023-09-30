from tkinter import *
from tkinter.ttk import *
import game_backend as gb
from threading import Thread

log_messages = ["Please describe the setting of the game you want to play"]


prompt_given = False
window = Tk()
window.minsize(1000, 700)

emoji_text = StringVar(value="ヾ(•ω•`)o")
stats_text = StringVar(value="🤖")

scrollframe = Frame(master=window, border=1)
stats = Label(textvariable=stats_text, master=scrollframe)
stats.pack()
itemlabel = Label(master=scrollframe, text='\nItems')
itemlabel.pack()
scrollbar = Scrollbar(master=scrollframe)
scrollbar.pack(side = RIGHT, fill=Y)
itemlist = Listbox(scrollframe, yscrollcommand = scrollbar.set)
itemlist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = itemlist.yview )

scrollframe.pack(side=LEFT, fill=Y)

# greeting = Label(text="Please describe the setting of the game you want to play")
# greeting.pack(side  = LEFT)

logframe = Frame(master=window)
loglabel = Label(master=logframe, text='Log')
loglabel.pack(side=TOP)
logscroll = Scrollbar(master=logframe)
logscroll.pack(side = RIGHT, fill=Y)
log = Text(master=logframe, yscrollcommand = logscroll.set)
log.insert(END, "Please describe the setting of the game you want to play")
log.config(state=DISABLED)
log.pack(fill=BOTH)
logframe.pack(fill=BOTH)

def add_to_log(text):
   log.config(state=NORMAL)
   log.insert(END, text)
   log.config(state=DISABLED)
    # Label(master=log, text=text).pack()

funframe = Frame(master=window)
emoji = Label(textvariable=emoji_text, master=window, font=('Arial', 100))
emoji.pack()
funframe.pack()

entryframe = Frame(master=window)
entry = Entry(width=100, master=entryframe)
entry.pack(side=LEFT)

sendbutton = Button(master=entryframe, text='Send')

def change_stats_and_items():
    itemlist.delete(0, END)
    item_str = ''
    for stat in gb.stats:
        if stat == 'Items':
            for item in gb.stats['Items']:
                itemlist.insert(END, str(item))
            continue
        item_str += stat + ": " + str(gb.stats[stat]) + '\n'
    global stats_text
    stats_text.set(item_str)
    #stats.config(text=item_str)
    #print('done?')
                
def handle_backend(user_data):
    global prompt_given
    if (not prompt_given):
        data, code = gb.prompt_user(user_data)
        if code == 0: prompt_given = True
    else:
        data, code = gb.game_loop(user_data)
    global emoji_text
    emoji = gb.sentiment_emoji(data)
    add_to_log(data)
    emoji_text.set(emoji)
    entry.config(state=NORMAL)
    sendbutton.config(state=NORMAL)
    entry.delete(0, END)

    change_stats_and_items()

def send_clicked(event=None):
    user_data = entry.get()
    add_to_log('\n\n> ' + user_data + '\n\n')
    entry.delete(0, END)
    entry.insert(0, 'Loading...')
    entry.config(state=DISABLED)
    sendbutton.config(state=DISABLED)
    Thread(target=handle_backend, args=(user_data,)).start()

window.bind('<Return>', send_clicked)

sendbutton.config(command=send_clicked)

sendbutton.pack(side=RIGHT, padx=10)
entryframe.pack(side=BOTTOM)


window.config(padx=10, pady=10)
window.mainloop()