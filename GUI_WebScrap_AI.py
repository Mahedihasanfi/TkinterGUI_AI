# Personal Assistant Program
# This is a Python program that functions as a personal assistant.
# It provides various features such as task management, web scraping, and voice command recognition.


# Importing necessary modules from the tkinter library for GUI
import tkinter as tk # GUI application library
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

# Importing necessary modules for web scraping
from bs4 import BeautifulSoup # Web scraping library
import requests
import json

# Importing necessary modules for Voice Assistant
import speech_recognition as sr
import pyttsx3 # Text-to-speech
import datetime
import pywhatkit # Web search
import sys
import pyjokes # Provides a collection of jokes

# Task class to represent a task with a description and due date
class Task:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date

# TaskManager class to manage tasks
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task):
        self.tasks.remove(task)

    def edit_task(self, old_task, new_task):
        index = self.tasks.index(old_task)
        self.tasks[index] = new_task

    def get_all_tasks(self):
        return self.tasks

    def load_tasks_from_file(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.tasks = [Task(task["description"], task["due_date"]) for task in data]
                return (self.tasks)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks_to_file(self):
        data = [{"description": task.description, "due_date": task.due_date} for task in self.tasks]
        with open("tasks.json", "w") as file:
            json.dump(data, file)

class WebScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        try:
            response = requests.get(self.url)

            # Creating a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Finding elements in the HTML using BeautifulSoup's find_all() method
            info = soup.find_all("section", attrs={"id":"a-first-look-at-classes"})

            web_scraping_data = []  # Create an empty list to store the extracted text
            for store in info:
                web_scraping_data.append(store.get_text())  # Append the extracted text to the list

            # Save the data to a JSON file
            with open('web_scraping_data.json', 'w') as file:
                json.dump(web_scraping_data, file)

            # Read the JSON file and display its contents
            with open('web_scraping_data.json', 'r') as file:
                json_data = json.load(file)
                for line in json_data:
                    return line
        except requests.exceptions.RequestException:
            return None

# Class: Responsible for voice input and generating voice output
class VoiceAssistant:
    def __init__(self):
        # Initializing a Recognizer object from the speech_recognition library
        self.listener = sr.Recognizer()

        # Initializing a text-to-speech Engine (ida) using the pyttsx3
        self.ida = pyttsx3.init()

        # Retrieves the available voices from the text-to-speech engine
        self.voices = self.ida.getProperty('voices')

        # Second voice (as women for ida) has been selected
        self.ida.setProperty('voice', self.voices[1].id)

    def talk(self, text):
        self.ida.say(text) # Given text to be spoken by voice assistant ida
        self.ida.runAndWait() # Wait until the text is completely spoken

    def take_command(self):
        try:
            # Setting-up the microphone as the audio source for the speech recognition
            with sr.Microphone() as source:
                print('Listening...')

                # Captures the audio input from the microphone and stores it in the voice variable
                voice = self.listener.listen(source)

                # Uses the speech recognition library to convert the captured audio into text and and stored in the direction variable
                direction = self.listener.recognize(voice).lower()
        except:
            self.talk("Sorry, didn't catch. Repeat Please")
            self.run_ida()
        return direction

    def run_ida(self):
        while True:
            order = self.take_command()
            if 'hello' in order:
                greet='Hello! Tell me what can I do for you?'
                print(greet)
                self.talk(greet)

            elif 'time' in order:
                present_time = datetime.datetime.now().strftime('%I:%M %p')
                print(present_time)
                self.talk('Current time is ' + present_time)

            elif 'study' in order:
                college='You are studying web developmenmt at Turing College'
                print(college)
                self.talk(college)

            elif 'joke' in order:
                gotten_joke=pyjokes.get_joke() # Collect jokes
                print(gotten_joke)
                self.talk(gotten_joke)

            elif 'exit' in order:
                bye="Thanks! Bye Bye!"
                self.talk(bye)
                sys.exit(bye)

            else:
                dont_know='Didnt understand, going to search'
                print(dont_know)
                self.talk(dont_know)
                pywhatkit.search(order) # Initialize web searching

class PersonalAssistantGUI:
    def __init__(self):
        #Creating a new instance of the Tk class, configuring the root window's properties
        self.root = tk.Tk()
        self.root.configure(bg="#266E73")
        self.root.title("Personal Assistant")

        self.task_manager = TaskManager()
        self.web_scraper = WebScraper("https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes")
        self.voice_assistant = VoiceAssistant()

        self.create_gui() #  creating and configuring the graphical elements of the user interface

    def create_gui(self):

        # Creating task management section:

        task_frame = tk.Frame(self.root) # Creates a frame for task management section
        task_frame.pack(pady=10)

        # Creates a label widget with the text "Task Management"
        task_label = tk.Label(task_frame, text="Task Management", font=("Helvetica", 16))
        task_label.pack(pady=5)

        # Creates a label widget with the text "Description:"
        description_label = tk.Label(task_frame, text="Description:")
        description_label.pack()

        # Creates an entry widget to enter the task description, with a specified background color and width
        self.task_description_entry = tk.Entry(task_frame, bg="#4B4BC3", width=30)
        self.task_description_entry.pack()

        # Creates a label widget with the text "Due Date:"
        due_date_label = tk.Label(task_frame, text="Due Date:")
        due_date_label.pack()

        # Creates an entry widget to enter the task due date, with a specified background color and width
        self.task_due_date_entry = tk.Entry(task_frame, bg="#AC4D39", width=30)
        self.task_due_date_entry.pack()

        # Creates a button widget with the text "Create Task" and it will call create_task method if pressed
        create_task_button = tk.Button(task_frame, text="Create Task", command=self.create_task)
        create_task_button.pack(pady=5)

        # Creates a button widget with the text "Show All Tasks" and it will call show_all_tasks method if pressed
        show_tasks_button = tk.Button(task_frame, text="Show All Tasks", command=self.show_all_tasks)
        show_tasks_button.pack(pady=5)

        # Creates a button widget with the text "Edit Task" and it will call edit_task method if pressed
        edit_task_button = tk.Button(task_frame, text="Edit Task", command=self.edit_task)
        edit_task_button.pack(pady=5)

        # Creates a button widget with the text "Delete Task" and it will call delete_task method if pressed
        delete_task_button = tk.Button(task_frame, text="Delete Task", command=self.delete_task)
        delete_task_button.pack(pady=5)

        # Creating web scraping section:

        web_frame = tk.Frame(self.root) # Frame for web scraping section
        web_frame.pack(pady=10)

        web_label = tk.Label(web_frame, text="Web Scraping", font=("Helvetica", 16))
        web_label.pack(pady=5)

        scrape_button = tk.Button(web_frame, text="Scrape Website", command=self.scrape_website)
        scrape_button.pack(pady=5)

        # Creating a ScrolledText widget to display a scrollable text area for scraped data
        self.web_text = ScrolledText(web_frame, bg="olive", height=13, width=80)
        self.web_text.pack(pady=5)

        # Creating voice assistant section:
        voice_frame = tk.Frame(self.root) # Frame for voice assistant section
        voice_frame.pack(pady=10)

        voice_label = tk.Label(voice_frame, text="Voice Assistant", font=("Helvetica", 16))
        voice_label.pack(pady=5)

        voice_command_button = tk.Button(voice_frame, text="Voice Command", command=self.voice_command)
        voice_command_button.pack(pady=5)

    # Create task button in GUI
    def create_task(self):
        description = self.task_description_entry.get()
        due_date = self.task_due_date_entry.get()

        if description and due_date:
            task = Task(description, due_date)
            self.task_manager.add_task(task)
            self.task_manager.save_tasks_to_file()

            # Creating a messagebox to display a message
            messagebox.showinfo("Success", "Task created successfully.")
            self.clear_task_entries()
        else:
            messagebox.showinfo("Error", "Please enter task description and due date.")

    # Show all tasks button in GUI
    def show_all_tasks(self):
        tasks = self.task_manager.load_tasks_from_file()
        print(tasks)
        if tasks:
            messagebox.showinfo("All Tasks", "\n".join([f"Description: {task.description}\nDue Date: {task.due_date}\n" for task in tasks]))
        else:
            messagebox.showinfo("No Tasks", "No tasks found.")

    # Edit task button in GUI
    def edit_task(self):
        tasks = self.task_manager.get_all_tasks()
        if tasks:
            # Creating a simpledialog to get user input
            selected_task = simpledialog.askinteger("Edit Task", "Enter the task number to edit:")
            if selected_task and selected_task > 0 and selected_task <= len(tasks):
                task_to_edit = tasks[selected_task - 1]

                # Create a new window to edit the task
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Edit Task")

                description_label = tk.Label(edit_window, text="Description:")
                description_label.pack()

                # Getting new value for task-description
                description_entry = tk.Entry(edit_window, width=30)
                description_entry.insert(tk.END, task_to_edit.description)
                description_entry.pack()

                due_date_label = tk.Label(edit_window, text="Due Date:")
                due_date_label.pack()

                # Getting new value for task-date
                due_date_entry = tk.Entry(edit_window, width=30)
                due_date_entry.insert(tk.END, task_to_edit.due_date)
                due_date_entry.pack()

                save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_edited_task(edit_window, task_to_edit, description_entry.get(), due_date_entry.get()))
                save_button.pack(pady=10)
            else:
                messagebox.showinfo("Invalid Task Number", "Please enter a valid task number.")
        else:
            messagebox.showinfo("No Tasks", "No tasks found.")

    # Within edit task: Save button in GUI
    def save_edited_task(self, edit_window, old_task, new_description, new_due_date):
        if new_description and new_due_date:
            old_task.description = new_description
            old_task.due_date = new_due_date
            self.task_manager.save_tasks_to_file()
            messagebox.showinfo("Success", "Task edited successfully.")
            edit_window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter task description and due date.")

    # Delete task button in GUI
    def delete_task(self):
        self.voice_assistant.talk("You pressed delete button")
        tasks = self.task_manager.get_all_tasks()
        if tasks:
            selected_task = simpledialog.askinteger("Delete Task", "Enter the task number to delete:")
            if selected_task and selected_task > 0 and selected_task <= len(tasks):
                task_to_delete = tasks[selected_task - 1]
                confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the task:\nDescription: {task_to_delete.description}\nDue Date: {task_to_delete.due_date}"
                )
                if confirm:
                    self.task_manager.delete_task(task_to_delete)
                    self.task_manager.save_tasks_to_file()  # Save tasks to file
                    messagebox.showinfo("Success", "Task deleted successfully.")
            else:
                messagebox.showinfo("Invalid Task Number", "Please enter a valid task number.")
        else:
            messagebox.showinfo("No Tasks", "No tasks found.")

    # Scrape website button in GUI
    def scrape_website(self):
        data = self.web_scraper.scrape()
        if data:
            # Deleting the content of the ScrolledText widget starting from the first character (1.0) to the end (tk.END)
            self.web_text.delete(1.0, tk.END)
            # Inserting the value of the 'data' variable into the ScrolledText widget at the end of the current content (tk.END)
            self.web_text.insert(tk.END, data)
            messagebox.showinfo("Success", "Web scraped successfully.")
        else:
            messagebox.showinfo("Error", "Failed to scrape website.")

    # Voice command button in GuI
    def voice_command(self):
        self.voice_assistant.run_ida()

    # Clearing input data to be ready for new entry when creating new task
    def clear_task_entries(self):
        self.task_description_entry.delete(0, tk.END)
        self.task_due_date_entry.delete(0, tk.END)

    def run(self):
        # Starting the Tkinter event loop
        self.root.mainloop()

if __name__ == "__main__":
    assistant_gui = PersonalAssistantGUI()
    assistant_gui.run()
