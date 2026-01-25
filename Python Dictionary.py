import sys

from tkinter import *
import sv_ttk
from bs4 import BeautifulSoup
import requests

if sys.platform.startswith("win"):
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

class text(Text):
    def replace_text(self, replace):
        self.configure(state="normal", font="Calibri")
        output.delete("1.0", END)
        output.insert(INSERT, replace)
        output.configure(state="disabled")

def main(event):
    global h

    word = input.get()
    input.delete(0, len(word))
    if word == "exit":
        window.quit()

    if "define" in word or "Define" in word:
        word = word.replace("define ", "")
        word = word.replace("Define", "")

    else:
        try:
            response = requests.get("https://www.merriam-webster.com/dictionary/" + word)
            soup = BeautifulSoup(response.text, "html.parser")
            code = soup.findAll(class_="dtText")

            part_of_speech = soup.find(class_="important-blue-link").getText()
            output_text = f"{word}: {part_of_speech} \n"

            x = 1
            for definition in code:
                output_text = output_text + str(x) + definition.getText() + "\n"
                x = x + 1
                h = h + 1

            output.replace_text(output_text)
            output.configure(height=h)
        except AttributeError:
            output.replace_text("---Error---")
            output.configure(height=2)


window = Tk()
sv_ttk.set_theme("dark")
window.geometry("900x500")
window.title("Dictionary")

input = Entry(bg="white", fg="black", font=("Segoe UI", 15))
input.bind("<Return>", main)
input.configure(insertbackground="black")
input.pack(pady=10)
input.focus()

enter = Button(text="Submit", bg="#2360B5", font=("Segoe UI", 12))
enter.bind("<Button-1>", main)
enter.pack()

h = 2
output = text(bg="#3b3b3b", height=h, width=120)
output.configure(state="disabled")
output.pack(pady=20)

window.mainloop()
