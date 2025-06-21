from tkinter import *
from tkinter import ttk, messagebox
import json
import random
import pyttsx3
from difflib import get_close_matches

# Load data
with open('data.json') as f:
    data = json.load(f)

# TTS Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Globals
search_history = []
favorites = []
dark_mode = False

# App window
root = Tk()
root.title("🧠 Talking Dictionary Plus")
root.geometry("1100x700")
root.configure(bg="white")
style = ttk.Style(root)
style.theme_use('clam')


# === Functions ===
def speak(text):
    engine.say(text)
    engine.runAndWait()


def search():
    word = enterwordEntry.get().lower()
    if not word:
        return
    search_history.append(word)
    suggestion_list.delete(0, END)

    if word in data:
        display_meaning(word, data[word])
    else:
        close_matches = get_close_matches(word, data.keys(), n=5, cutoff=0.6)
        if close_matches:
            for match in close_matches:
                suggestion_list.insert(END, match)
            messagebox.showinfo('Suggestion', 'Word not found. Did you mean one of these?')
        else:
            messagebox.showinfo('Info', 'The Word Does Not Exist')
            textarea.delete(1.0, END)


def display_meaning(word, meanings):
    textarea.delete(1.0, END)
    for item in meanings:
        textarea.insert(END, f'• {item}\n\n')


def clear():
    enterwordEntry.delete(0, END)
    textarea.delete(1.0, END)
    suggestion_list.delete(0, END)


def iexit():
    if messagebox.askyesno('Exit', 'Do you want to exit?'):
        root.destroy()


def wordaudio():
    speak(enterwordEntry.get())


def meaningaudio():
    speak(textarea.get(1.0, END))


def pick_suggestion():
    selected = suggestion_list.curselection()
    if selected:
        word = suggestion_list.get(selected[0])
        enterwordEntry.delete(0, END)
        enterwordEntry.insert(END, word)
        display_meaning(word, data[word])


def show_history():
    history_window = Toplevel(root)
    history_window.title("🔍 Search History")
    history_window.geometry("300x400")
    history_list = Listbox(history_window, font=('arial', 14))
    history_list.pack(fill=BOTH, expand=True)
    for word in search_history:
        history_list.insert(END, word)


def add_favorite():
    word = enterwordEntry.get()
    if word and word not in favorites:
        favorites.append(word)
        messagebox.showinfo("Favorite", f"'{word}' added to favorites")


def show_favorites():
    fav_window = Toplevel(root)
    fav_window.title("★ Favorites")
    fav_window.geometry("300x400")
    fav_list = Listbox(fav_window, font=('arial', 14))
    fav_list.pack(fill=BOTH, expand=True)
    for word in favorites:
        fav_list.insert(END, word)


def word_of_the_day():
    word = random.choice(list(data.keys()))
    enterwordEntry.delete(0, END)
    enterwordEntry.insert(END, word)
    display_meaning(word, data[word])


def toggle_voice():
    current = engine.getProperty('voice')
    engine.setProperty('voice', voices[1].id if current == voices[0].id else voices[0].id)


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = '#1a1a1a' if dark_mode else '#f0f0f0'
    fg = '#ffffff' if dark_mode else '#2c3e50'
    accent = '#2980b9' if dark_mode else '#3498db'
    text_bg = '#2c2c2c' if dark_mode else 'white'

    root.configure(bg=bg)
    top_frame.configure(bg=bg)
    button_frame.configure(bg=bg)
    left_frame.configure(bg=bg)
    right_frame.configure(bg=bg)

    # Update labels
    for widget in root.winfo_children():
        if isinstance(widget, Label):
            widget.configure(bg=bg, fg=fg)

    # Update buttons
    for btn in button_frame.winfo_children():
        if isinstance(btn, Button):
            btn.configure(bg=accent, fg='white', activebackground=accent)

    # Update text areas
    textarea.configure(bg=text_bg, fg=fg, insertbackground=fg)
    suggestion_list.configure(bg=text_bg, fg=fg, selectbackground=accent)

    # Update frames
    textarea_frame.configure(bg=bg)
    suggestion_frame.configure(bg=bg)


# === UI Layout ===

# Top frame for entry and search
top_frame = Frame(root, bg='#f0f0f0')
top_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=20, sticky='ew')

Label(top_frame, text="🔎 Enter Word:", font=('Segoe UI', 24, 'bold'), fg='#2c3e50', bg='#f0f0f0').grid(row=0, column=0,
                                                                                                       padx=15)
style.configure('Custom.TEntry', padding=10)
enterwordEntry = ttk.Entry(top_frame, font=('Segoe UI', 20), width=25, justify=CENTER, style='Custom.TEntry')
enterwordEntry.grid(row=0, column=1, padx=15)

# Button Frame with modern styling
button_frame = Frame(root, bg='#f0f0f0')
button_frame.grid(row=1, column=0, columnspan=2, pady=15)


def styled_button(text, cmd):
    btn = Button(button_frame, text=text, command=cmd,
                 font=('Segoe UI', 11),
                 bg='#3498db',
                 fg='white',
                 activebackground='#2980b9',
                 activeforeground='white',
                 bd=0,
                 padx=15,
                 pady=8,
                 cursor='hand2')
    btn.pack(side=LEFT, padx=8)
    btn.bind("<Enter>", lambda e: e.widget.configure(bg='#2980b9'))
    btn.bind("<Leave>", lambda e: e.widget.configure(bg='#3498db'))
    return btn


buttons = [
    ("🔍 Search", search),
    ("🗑️ Clear", clear),
    ("🔊 Speak Word", wordaudio),
    ("🔈 Speak Meaning", meaningaudio),
    ("★ Add Favorite", add_favorite),
    ("📜 Favorites", show_favorites),
    ("🕘 History", show_history),
    ("🌐 Word of Day", word_of_the_day),
    ("🎤 Toggle Voice", toggle_voice),
    ("🌙 Dark Mode", toggle_theme),
    ("❌ Exit", iexit)
]

for text, cmd in buttons:
    styled_button(text, cmd)

# Main content frames with improved styling
left_frame = Frame(root, bg='#f0f0f0')
left_frame.grid(row=2, column=0, padx=30, pady=20)

right_frame = Frame(root, bg='#f0f0f0')
right_frame.grid(row=2, column=1, padx=20, pady=20)

Label(left_frame, text="📖 Meaning", font=('Segoe UI', 22, 'bold'), fg='#2c3e50', bg='#f0f0f0').pack(anchor='w',
                                                                                                    pady=(0, 10))
textarea_frame = Frame(left_frame, bg='#f0f0f0')
textarea_frame.pack()
textarea = Text(textarea_frame, width=50, height=15,
                font=('Segoe UI', 14),
                bd=0,
                relief=FLAT,
                wrap=WORD,
                padx=10,
                pady=10,
                bg='white',
                fg='#2c3e50')
textarea.pack(side=LEFT)
scroll_y = Scrollbar(textarea_frame, command=textarea.yview)
scroll_y.pack(side=RIGHT, fill=Y)
textarea.config(yscrollcommand=scroll_y.set)

Label(right_frame, text="💡 Suggestions", font=('Segoe UI', 22, 'bold'), fg='#2c3e50', bg='#f0f0f0').pack(anchor='w',
                                                                                                         pady=(0, 10))
suggestion_frame = Frame(right_frame, bg='#f0f0f0')
suggestion_frame.pack()
suggestion_list = Listbox(suggestion_frame,
                          font=('Segoe UI', 14),
                          height=15,
                          width=15,
                          bd=0,
                          relief=FLAT,
                          bg='white',
                          fg='#2c3e50',
                          selectmode=SINGLE,
                          activestyle='none',
                          selectbackground='#3498db',
                          selectforeground='white')
suggestion_list.pack(side=LEFT)
scroll_sugg = Scrollbar(suggestion_frame, command=suggestion_list.yview)
scroll_sugg.pack(side=RIGHT, fill=Y)
suggestion_list.config(yscrollcommand=scroll_sugg.set)
suggestion_list.bind('<Double-1>', lambda e: pick_suggestion())

# Shortcuts
root.bind('<Return>', lambda e: search())
root.bind('<Control-c>', lambda e: clear())
root.bind('<Control-w>', lambda e: wordaudio())
root.bind('<Control-m>', lambda e: meaningaudio())

root.mainloop()