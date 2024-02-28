import json
from tkinter import *
from tkinter import messagebox
import random
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

def gen_password():
  letters = [
    'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', 
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'
  ]
  numbers = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
  ]
  symbols = [
    '!', '#', '$', '%', '&', '(', ')', '*', '+'
  ]
  letters = [random.choice(letters) for letter in range(nr_letters)]
  numbers = [random.choice(numbers) for number in range(nr_numbers)]
  symbols = [random.choice(symbols) for symbol in range(nr_symbols)]

  password_list = letters + numbers + symbols

  random.shuffle(password_list)
  if len(pass_wrd_input.get()) != 0:
    pass_wrd_input.delete(0, END)
  pass_wrd_input.insert(0, "".join(password_list))
# ---------------------------- SAVE PASSWORD ------------------------------- #
def clear_fields(*args):
  for arg in args:
    arg.delete(0, END)

def empty_fields(*args):
  for arg in args:
    if len(arg) == 0:
      messagebox.showerror(
        title="Missing Information", 
        message="All fields must be filled out to proceed."
      )
      return False
  return True

def save_password():
  website = site_input.get()
  user_nm = user_input.get()
  pass_wrd = pass_wrd_input.get()
  to_dump = {
    website : {
      "email" : user_nm,
      "password" : pass_wrd
    }
  }

  fields_filled = empty_fields(website, user_nm, pass_wrd)
  
  if fields_filled:
    clear_fields(site_input, user_input, pass_wrd_input)
    confirmed = messagebox.askokcancel(
      title=website, 
      message=f"Save information provided for {website}?:\n{user_nm}\n{pass_wrd}"
    )
    
    if confirmed:
      with open("passwords.json", "w") as passwords:
        json.dump(to_dump, passwords, indent=2)
# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
  site_name = site_input.get()
  try:
    with open("passwords.json", "r") as passwords:
      data = json.load(passwords)
  except FileNotFoundError:
    messagebox.showerror(
      title="No Saved Passwords",
      message="No passwords have been saved."
    )
  else:
    try:
      entry = data[site_name]
    except KeyError:
      messagebox.showerror(
        title="Entry Not Found",
        message=f"No entry was found that matched {site_name}"
      )
    else:
      site_input.delete(0, END)
      return messagebox.showinfo(
        title="Account Information",
        message=f"User Name: {entry['email']}\nPassword: {entry['password']}"
      )
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo = PhotoImage("logo.png")
canvas.create_image(100, 100) #Can add image=logo
canvas.grid(column=1, row=0)

site_lbl = Label(text="Website:")
site_lbl.grid(column=0, row=1)

site_input = Entry(width=21)
site_input.grid(column=1, row=1)
site_input.focus()

user_lbl = Label(text="Email/Username:")
user_lbl.grid(column=0, row=2)

user_input = Entry(width=35)
user_input.grid(column=1, row=2, columnspan=2)

pass_wrd_lbl = Label(text="Password:")
pass_wrd_lbl.grid(column=0, row=3)

pass_wrd_input = Entry(width=21)
pass_wrd_input.grid(column=1, row=3, columnspan=1)

gen_pass_wrd_btn = Button(text="Generate Password", command=gen_password)
gen_pass_wrd_btn.grid(column=2, row=3)

save_btn = Button(text="Add", width=36, command=save_password)
save_btn.grid(column=1, row=4, columnspan=2)

search_btn = Button(text="Search", width=14, command=search_password)
search_btn.grid(column=2, row=1)



window.mainloop()