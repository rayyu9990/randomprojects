import tkinter as tk
import random
from tkinter import messagebox
from tkinter import simpledialog

root = tk.Tk()
root.title("Cube")
root.geometry("400x400")

scramble_options = [['F', "F'", "F2", 'B', "B'", "B2"], ['U', "U'", "U2", 'D', "D'", "D2"], ['R', "R'", "R2", 'L', "L'", "L2"]]
last_subset = None

scramble = []
times = []
scrambles = []
def generate_scramble():
    try:
        time = float(time_entry.get("1.0", tk.END))
    except ValueError:
        messagebox.showerror(title="Error", message="Invalid Input")
    else:
        global last_subset, scramble, times, scrambles
        scramble.clear()
        previous_times.insert(0, time_entry.get("1.0", tk.END))
        previous_times.delete(0, tk.END)
        scramblelength = random.randint(18, 22)
        for i in range(scramblelength):
            subset = random.choice(scramble_options)
            while subset == last_subset:
                subset = random.choice(scramble_options)
            move = random.choice(subset)
            scramble.append(move)
            last_subset = subset
        scramble_text = "Scramble: " + " ".join(scramble)
        scrambles.append(scramble_text)
        scramble_label.config(text=scramble_text)
        if time > 100:
            time = time / 100
        times.append(time)
        time_entry.delete("1.0", "end")
        for time in times:
            previous_times.insert(tk.END, time)

def add_time(event):
    global last_subset, scramble, scrambles
    scramble.clear()
    scramblelength = random.randint(18, 22)
    for i in range(scramblelength):
        subset = random.choice(scramble_options)
        while subset == last_subset:
            subset = random.choice(scramble_options)
        move = random.choice(subset)
        scramble.append(move)
        last_subset = subset
    scramble_text = "Scramble: " + " ".join(scramble)
    scrambles.append(scramble_text)
    scramble_label.config(text=scramble_text)

    try:
        time = float(time_entry.get("1.0", tk.END))
    except ValueError:
        messagebox.showerror(title="Error", message="Invalid Input")
    else:
        if time > 100:
            time = time / 100
        times.append(time)
        previous_times.insert(tk.END, time)
        time_entry.delete("1.0", "end")
        calculate_ao5()
        calculate_ao12()
        calculate_mean()
        find_pb()

def find_pb():
    if not times:
        return None
    pb = min(times)
    personal_best_label.config(text="Personal Best: " + str(pb))
    for time in times:
        if time < pb:
            pb = time
            personal_best_label.config(text="Personal Best: " + str(pb))

def calculate_ao5(event=None):
    old_times = times[-5:]
    if len(old_times) < 5:
        ao5_label.config(text="Average of 5: N/A")
    else:
        old_times.remove(max(old_times))
        old_times.remove(min(old_times))
        ao5 = round(float(sum(old_times) / 3), 2)
        ao5_label.config(text="Average of 5: " + str(ao5))

def calculate_ao12(event=None):
    old_times = times[-12:]
    if len(old_times) < 12:
        ao12_label.config(text="Average of 12: N/A")
    else:
        old_times.remove(max(old_times))
        old_times.remove(min(old_times))
        ao12 = round(float(sum(old_times) / 10), 2)
        ao12_label.config(text="Average of 12: " + str(ao12))

def calculate_mean(event=None):
    old_times = times
    mean = round(sum(old_times)/ len(old_times), 2)
    mean_label.config(text="Mean: "+ str(mean))

def show_solve():
    selected = previous_times.curselection()
    if selected:
        index = selected[0]
        past_time = times[index]
        past_scramble = scrambles[index]
        messagebox.showinfo(message=f"Time:{past_time}\nScramble:{past_scramble}")

def edit_time():
    selected = previous_times.curselection()
    if selected:
        index = selected[0]
        new_time = simpledialog.askfloat(title="Edit Time", prompt="Enter the updated time")
        if new_time is not None:
            times[index] = new_time
            previous_times.delete(index)
            previous_times.insert(index, new_time)
            find_pb()
            calculate_ao5()
            calculate_ao12()
            calculate_mean()


title_label = tk.Label(root, text="3x3 Scrambler")
title_label.pack()

scramble_label = tk.Label(root, text="Scramble: ")
scramble_label.pack()
time_entry_label = tk.Label(root, text="Time: ")
time_entry_label.pack()
time_entry = tk.Text(root, width=10, height=1)
time_entry.pack()
personal_best_label = tk.Label(root, text="Personal Best: ")
personal_best_label.pack()
ao5_label = tk.Label(root, text="Average of 5: ")
ao5_label.pack()
ao12_label = tk.Label(root, text="Average of 12: ")
ao12_label.pack()
mean_label = tk.Label(root, text="Mean: ")
mean_label.pack()


enter_button = tk.Button(root, text="Enter", command=generate_scramble)
enter_button.pack()
history_button = tk.Button(root, text="Show Details", command=show_solve)
history_button.pack()

previous_times = tk.Listbox(root)
previous_times.pack()

edit_button = tk.Button(root, text="Edit Time", command=edit_time)
edit_button.pack()

scramblelength = random.randint(18, 22)
for i in range(scramblelength):
    subset = random.choice(scramble_options)
    while subset == last_subset:
        subset = random.choice(scramble_options)
    move = random.choice(subset)
    scramble.append(move)
    last_subset = subset
scramble_text = "Scramble: " + " ".join(scramble)
scrambles.append(scramble_text)
scramble_label.config(text=scramble_text)

time_entry.bind("<Return>", add_time)
root.mainloop()