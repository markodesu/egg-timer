import customtkinter as ctk
from PIL import Image, ImageTk
import os
import tkinter as tk

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("320x420")
app.title("Egg Timer")
app.configure(fg_color="#FFF7E6")

timer_label = None
egg_label = None
timer_running = False

# Resize egg image
egg_pil = Image.open("egg.png").resize((128,128), Image.Resampling.LANCZOS)
egg_img = ImageTk.PhotoImage(egg_pil)

# Resize main menu image
menu_pil = Image.open("menu.png").resize((150,150), Image.Resampling.LANCZOS)
menu_img = ImageTk.PhotoImage(menu_pil)

def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()

def float_image(label, y_min, y_max, direction=1, step=1):
    y = label.winfo_y() + direction * step
    if y < y_min:
        y = y_min
        direction = 1
    elif y > y_max:
        y = y_max
        direction = -1
    label.place(y=y)
    app.after(50, lambda: float_image(label, y_min, y_max, direction, step))

def countdown():
    global timer_running, current_seconds
    if not timer_running:
        return
    mins, secs = divmod(current_seconds, 60)
    timer_label.configure(text=f"{mins:02}:{secs:02}")
    if current_seconds > 0:
        current_seconds -= 1
        app.after(1000, countdown)
    else:
        timer_label.configure(text="🍳 Ready!")

def start_timer(seconds):
    global current_seconds, timer_label, egg_label, timer_running
    current_seconds = seconds
    timer_running = True
    clear_screen()

    timer_label = ctk.CTkLabel(
        app,
        text="00:00",
        font=("Arial", 36),
        text_color="#5A4A42"
    )
    timer_label.pack(pady=20)

    egg_label = tk.Label(app, image=egg_img, bg="#FFF7E6")
    egg_label.image = egg_img  # Keep a reference
    egg_label.place(x=96, y=160)  # initial position
    float_image(egg_label, y_min=150, y_max=170)

    back_button = ctk.CTkButton(
        app,
        text="Back",
        width=100,
        height=30,
        corner_radius=10,
        command=stop_timer
    )
    back_button.pack(pady=10)

    countdown()

def stop_timer():
    global timer_running
    timer_running = False
    show_selection_screen()

def show_welcome_screen():
    clear_screen()

    menu_label = tk.Label(app, image=menu_img, bg="#FFF7E6")
    menu_label.image = menu_img  # Keep a reference
    menu_label.place(x=85, y=50)  # initial position
    float_image(menu_label, y_min=40, y_max=60)

    welcome_button = ctk.CTkButton(
        app,
        text="Let's Cook an Egg",
        font=("Arial", 18),
        width=240,
        height=50,
        corner_radius=20,
        command=show_selection_screen
    )
    welcome_button.pack(pady=200)

def show_selection_screen():
    clear_screen()

    title = ctk.CTkLabel(
        app,
        text="How do you like your egg?",
        font=("Arial", 18),
        text_color="#5A4A42"
    )
    title.pack(pady=40)

    ctk.CTkButton(
        app,
        text="Soft",
        width=240,
        height=40,
        corner_radius=20,
        command=lambda: start_timer(180)
    ).pack(pady=6)

    ctk.CTkButton(
        app,
        text="Medium",
        width=240,
        height=40,
        corner_radius=20,
        command=lambda: start_timer(300)
    ).pack(pady=6)

    ctk.CTkButton(
        app,
        text="Hard",
        width=240,
        height=40,
        corner_radius=20,
        command=lambda: start_timer(420)
    ).pack(pady=6)

    back_button = ctk.CTkButton(
        app,
        text="Back",
        width=100,
        height=30,
        corner_radius=10,
        command=show_welcome_screen
    )
    back_button.pack(pady=10)

show_welcome_screen()
app.mainloop()
