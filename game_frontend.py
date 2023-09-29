from tkinter import *
from tkinter.ttk import *
import game_backend as gb

log_messages = ["Please describe the setting of the game you want to play"]

prompt_given = False
window = Tk()
window.minsize(1000, 700)

scrollframe = Frame(master=window)
stats = Label(text="hello", master=scrollframe)
stats.pack()
scrollbar = Scrollbar(master=scrollframe)
scrollbar.pack(side = RIGHT, fill=Y)
itemlist = Listbox(scrollframe, yscrollcommand = scrollbar.set)
itemlist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = itemlist.yview )

scrollframe.pack(side=LEFT, fill=Y)

# greeting = Label(text="Please describe the setting of the game you want to play")
# greeting.pack(side  = LEFT)


logframe = Frame(master=window)
logscroll = Scrollbar(master=logframe)
logscroll.pack(side = RIGHT, fill=Y)
log = Text(master=logframe, yscrollcommand = logscroll.set, wrap=WORD)
log.insert(END, "Please describe the setting of the game you want to play")
log.config(state=DISABLED)
log.pack(fill=BOTH)
logframe.pack(fill=BOTH)

def add_to_log(text):
   log.config(state=NORMAL)
   log.insert(END, text)
   log.config(state=DISABLED)

entryframe = Frame(master=window)
entry = Entry(width=50, master=entryframe)
entry.pack(side=LEFT)

sendbutton = Button(master=entryframe, text='send')

def change_stats_and_items():
    itemlist.delete(0, END)
    item_str = ''
    for stat in stats:
        item_str += stat + ": " + str(stats[stat]) + '\n'
        if stat == 'Items':
            for item in stats['Items']:
                itemlist.insert(END, str(item))
                

def handle_backend(user_data):
    global prompt_given
    if (not prompt_given):
        add_to_log(gb.prompt_user(user_data))
        prompt_given = True
    else:
        add_to_log(gb.game_loop(user_data))
    entry.config(state=NORMAL)
    sendbutton.config(state=NORMAL)
    change_stats_and_items()

def send_clicked():
    user_data = entry.get()
    add_to_log('\n\n> ' + user_data + '\n\n')
    entry.delete(0, END)
    entry.config(state=DISABLED)
    sendbutton.config(state=DISABLED)
    handle_backend(user_data)

sendbutton.config(command=send_clicked)

sendbutton.pack(side=RIGHT)
entryframe.pack(side=BOTTOM)


window.mainloop()