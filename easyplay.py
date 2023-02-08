import pygetwindow as gw
import customtkinter
import keyboard
import pickle
import os
from time import sleep


try:
    color_theme = pickle.load(open("data/theme.dat", "rb"))
except:
    color_theme = 'blue'

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(color_theme)

try:
    bots = pickle.load(open("data/bot.dat", "rb"))
except:
    bots = [("Hydra", ".p", 3), ("Vexera", "+p", 4), ("Nekotina", "!p", 5), ("Jockie Music", "m!play", 3)]


def find_discord(str1=[]):
    strlist = ' '.join(str(x) for x in str1)
    result = ""
    for i in range(0, len(strlist)):
        if strlist[i] == '-' and strlist[i + 1] == ' ' and strlist[i + 2] == 'D' and strlist[i + 3] == 'i' and \
                strlist[i + 4] == 's' and strlist[i + 5] == "c":
            temp = i + 9
    for j in range(temp, 0, -1):
        if strlist[j] == '=':
            break
        result += strlist[j]
    result = result[:-1]
    result = result[1:]
    return result[::-1]


def open_discord():
    app_list = gw.getAllWindows()
    find_discord(app_list)
    win = gw.getWindowsWithTitle(find_discord(app_list))[0]
    win.activate()
    win.restore()


def create_window():
    width = 416
    height = 740
    window = customtkinter.CTk()
    window.title("EasyPlay")
    ScreenWidth = window.winfo_screenwidth()
    ScreenHeight = window.winfo_screenheight()
    x = (ScreenWidth / 2) - (width / 2)
    y = (ScreenHeight / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    window.iconbitmap('assets/music.ico')
    window.config(padx=10, pady=10)
    window.resizable(width=False, height=False)
    return window


def make_data_path():
    newpath = os.getcwd()
    newpath = newpath + "\data"
    print(os.getcwd())
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


def open_input_dialog_event():
    dialog = customtkinter.CTkInputDialog(text="Type in the bot's name:", title="Name")
    NewName = dialog.get_input()
    if NewName == "":
        return

    dialog1 = customtkinter.CTkInputDialog(text="Type in the bot's command:", title="Command")
    NewCommand = dialog1.get_input()

    if NewCommand == "":
        return
    bots.append((NewName, NewCommand, 5))
    optionmenu_1.configure(values=[x[0] for x in bots])


def clear_text_box():
    my_text.delete("1.0", "end")


def paste_select():
    data = window.clipboard_get()
    my_text.insert(customtkinter.END, data)  # Paste data from clipboard


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)
    startbutton.grid_remove()
    progressbar.grid_remove()


def make_popup(sc_x, sc_y, title, str):
    ScreenWidth = window.winfo_screenwidth()
    ScreenHeight = window.winfo_screenheight()
    x = (ScreenWidth / 2) - (sc_x / 2)
    y = (ScreenHeight / 2) - (sc_y / 2)
    popup = customtkinter.CTkToplevel()
    popup.title(title)
    popup.geometry(f'{sc_x}x{sc_y}+{int(x)}+{int(y)}')
    popup.resizable(width=False, height=False)
    popup.grab_set()
    temp_label = customtkinter.CTkLabel(popup, text=str, font=("Segoe UI", 16,))
    temp_label.pack(pady=25)


def change_accent_color_event(new_accent: str):
    make_data_path()
    global color_theme
    color_theme = new_accent
    string = "Changes will be \n taken to affect after restart"
    make_popup(300, 100, "Done", string)
    pickle.dump(color_theme, open("data/theme.dat", "wb"))


def save_bots():
    make_data_path()
    pickle.dump(bots, open("data/bot.dat", "wb"))


def tab_switched():
    if tabview.get() == "Play":
        startbutton.grid()
        progressbar.grid()
    elif tabview.get() == "Settings":
        startbutton.grid_remove()
        progressbar.grid_remove()
    elif tabview.get() == "Help":
        startbutton.grid_remove()
        progressbar.grid_remove()


def import_song():
    try:
        text_file = customtkinter.filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),))
        text_file = open(text_file, 'r+', encoding="utf8")
        songs = text_file.read()
        my_text.insert(customtkinter.END, songs)
    except:
        pass


def export_song():
    try:
        text_file = customtkinter.filedialog.asksaveasfilename(title="Save", filetypes=(("Text Files", "*.txt"),))
        text_file = open(text_file, 'w', encoding="utf8")
        text_file.write(my_text.get(1.0, customtkinter.END))
        text_file.close()
    except:
        pass


def find_command(string):
    for i in range(len(bots)):
        if string == bots[i][0]:
            return bots[i][1]


def find_delay(string):
    for i in range(len(bots)):
        if string == bots[i][0]:
            return bots[i][2]


def start_queue():
    if my_text.get(0.0, customtkinter.END) == "\n":
        return
    open_discord()
    sleep(3)
    startbutton.configure(state="disabled")
    songs = my_text.get(1.0, customtkinter.END)
    songs = songs.splitlines()
    command = find_command(optionmenu_1.get())
    delay = find_delay(optionmenu_1.get())
    for song in songs:
        keyboard.write(command + " " + song)
        keyboard.press_and_release('enter')
        sleep(delay)

    startbutton.configure(state="enabled")
    make_popup(200, 130, "Done", "Done!")


# create window
window = create_window()


# window.bind('<Motion>', motion)

# create and build header
head = customtkinter.CTkLabel(window, text="Easy Play", font=("Edwardian Script ITC", 47,), corner_radius=8)
head.grid(row=0, column=0, sticky='W', padx=(103, 0), pady=(20, 0))

tabview = customtkinter.CTkTabview(window, width=250, corner_radius=15, command=tab_switched)
tabview.grid(row=1, column=0, padx=12.2, pady=(20, 0), sticky="nsew")
tab_1 = tabview.add("Play")
tab_2 = tabview.add("Settings")
tab_3 = tabview.add("Help")

# window.tabview.tab("Settings").configure(command=tab_click)
# select frame
SelectBotFrame = customtkinter.CTkFrame(tab_1, corner_radius=10)

my_label = customtkinter.CTkLabel(SelectBotFrame, text="Select A Discord Bot :", font=("Times New Roman", 20))
optionmenu_1 = customtkinter.CTkOptionMenu(SelectBotFrame, values=[x[0] for x in bots], width=200, )
button_1 = customtkinter.CTkButton(master=SelectBotFrame, text="Add", width=40, command=open_input_dialog_event)

my_label.grid(row=0, column=0, sticky='W', pady=(20, 0), padx=(15, 0))
optionmenu_1.grid(row=1, column=0, padx=(20, 20), pady=(20, 30))
button_1.grid(row=1, column=1, padx=(0, 20), pady=(20, 30))

SelectBotFrame.grid(row=1, column=0, pady=(20, 0))

# create text frame
TextBoxFrame = customtkinter.CTkFrame(tab_1, corner_radius=10)
my_label_2 = customtkinter.CTkLabel(TextBoxFrame, text="Your Songs", font=("Times New Roman", 20))
my_label_2.pack()
my_text = customtkinter.CTkTextbox(TextBoxFrame, width=300, height=200, wrap="none")
my_text.pack()
TextBoxFrame.grid(row=2, column=0, sticky='W', padx=20, pady=(20, 0))

# create button frame
TextBoxButtonFrame = customtkinter.CTkFrame(tab_1, fg_color="transparent")

button_2 = customtkinter.CTkButton(master=TextBoxButtonFrame, text="Open", width=40, command=import_song)
button_3 = customtkinter.CTkButton(master=TextBoxButtonFrame, text="Save", width=40, command=export_song)
button_4 = customtkinter.CTkButton(master=TextBoxButtonFrame, text="Paste", width=40, command=paste_select)
button_5 = customtkinter.CTkButton(master=TextBoxButtonFrame, text="Delete", width=40, command=clear_text_box)

button_5.pack(side=customtkinter.RIGHT, padx=(5, 20), pady=20)
button_4.pack(side=customtkinter.RIGHT, padx=5)
button_3.pack(side=customtkinter.RIGHT, padx=5)
button_2.pack(side=customtkinter.RIGHT, padx=(20, 5))

TextBoxButtonFrame.grid(row=3, column=0)

startbutton = customtkinter.CTkButton(master=window, text="Start", width=100, command=start_queue, height=23,
                                      corner_radius=10)
startbutton.grid(row=4, column=0, pady=25, sticky="nw", padx=35)

progressbar = customtkinter.CTkProgressBar(master=window, height=23, corner_radius=20, width=210)
progressbar.grid(row=4, column=0, padx=(115, 0))

# tab 2
my_label_3 = customtkinter.CTkLabel(tab_2, text="Appearance Mode:", font=("Times New Roman", 20))
appearance_mode = customtkinter.CTkOptionMenu(tab_2, values=["Light", "Dark", "System"],
                                              command=change_appearance_mode_event)
my_label_3.grid(row=0, column=0, padx=(5, 50), pady=(30, 0))
appearance_mode.grid(row=1, column=1)

my_label_4 = customtkinter.CTkLabel(tab_2, text="Ui Scaling:", font=("Times New Roman", 20))
scaling = customtkinter.CTkOptionMenu(tab_2, values=["80%", "90%", "100%", "110%", "120%"],
                                      command=change_scaling_event)
my_label_4.grid(row=2, column=0, sticky="nw", pady=(30, 0), padx=(5, 0))
scaling.grid(row=3, column=1)

my_label_5 = customtkinter.CTkLabel(tab_2, text="Accent Color:", font=("Times New Roman", 20))
accent_mode = customtkinter.CTkOptionMenu(tab_2, values=["blue", "green", "dark-blue"],
                                          command=change_accent_color_event)
my_label_5.grid(row=4, column=0, sticky="nw", pady=(30, 0), padx=(5, 0))
accent_mode.grid(row=5, column=1)

my_label_6 = customtkinter.CTkLabel(tab_2, text="Mac Ui:", font=("Times New Roman", 20), text_color="#83838B")
mac_switch = customtkinter.CTkSwitch(tab_2, switch_width=40, text="", state="disabled")

my_label_6.grid(row=6, column=0, sticky="nw", pady=(30, 30), padx=(6, 0))
mac_switch.grid(row=6, column=0, padx=(75, 0), pady=(30, 30))

# tab 3
str1 = "This bot " \
       "automatically queues \n selected songs in discord \n \n How to use : \n Just Have your discord open on any " \
       "text-channel \n select the discord bot that exists in the server \n and import your songs then press start \n" \
       "and wait for the process to finish\n \n " \
       "Made By AMIRSRAD \n my email : iamamirssr@gmail.com"

label_8 = customtkinter.CTkLabel(tab_3, text=str1, font=("Segoe UI", 16,))
label_8.pack(pady=25)

progressbar.start()
progressbar.stop()

window.mainloop()

save_bots()
make_data_path()
