import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import pyjokes
import pywhatkit
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Change index for male/female voice
engine.setProperty('rate', 200)  # Adjust speaking speed

def respond(text):
    print("Ivy:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        respond("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        respond("Sorry, I'm having trouble connecting to the service.")
        return ""

def tell_joke():
    joke = pyjokes.get_joke()
    respond(joke)

def play_music(command):
    song = command.replace("play", "").strip()
    respond(f"Playing {song} on YouTube.")
    pywhatkit.playonyt(song)
    input("Press Enter after you're done listening to the music...")

reminders = []

def set_reminder(command):
    reminder = command.replace("remind me to", "").strip()
    reminders.append(reminder)
    respond(f"Okay, I'll remind you to {reminder}.")

def check_reminders():
    if reminders:
        for r in reminders:
            respond(f"Reminder: {r}")
        reminders.clear()

# 🔽 File Operation Functions 🔽
def create_file(command):
    try:
        filename = command.replace("create file", "").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        with open(filename, "w") as f:
            f.write("This is a new file created by your assistant.")
        respond(f"File '{filename}' has been created.")
    except Exception:
        respond("Sorry, I couldn't create the file.")

def read_file(command):
    try:
        filename = command.replace("read file", "").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        with open(filename, "r") as f:
            content = f.read()
        respond(f"Reading contents of {filename}: {content}")
    except FileNotFoundError:
        respond("Sorry, that file doesn't exist.")
    except Exception:
        respond("I had trouble reading the file.")

def delete_file(command):
    try:
        filename = command.replace("delete file", "").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        os.remove(filename)
        respond(f"File '{filename}' has been deleted.")
    except FileNotFoundError:
        respond("File not found.")
    except Exception:
        respond("Couldn't delete the file.")

# ✅ Write to file
def write_to_file(command):
    try:
        filename = command.replace("write to file", "").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        respond("What should I write?")
        content = listen()
        if content:
            with open(filename, "a") as f:
                f.write(content + "\n")
            respond(f"I wrote that to {filename}.")
        else:
            respond("Nothing to write.")
    except Exception:
        respond("Something went wrong while writing to the file.")

# 🔽 Command Processing 🔽
def execute_command(command):
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        respond("Opening Google. Let me know when you're done.")
        input("Press Enter after closing Google...")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        respond("Opening YouTube. Let me know when you're done.")
        input("Press Enter after closing YouTube...")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        respond(f"The time is {now}.")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            respond("According to Wikipedia: " + summary)
        except Exception:
            respond("Sorry, I couldn't find that on Wikipedia.")

    elif "joke" in command:
        tell_joke()

    elif "play" in command:
        play_music(command)

    elif "remind me to" in command:
        set_reminder(command)

    elif "do i have any reminders" in command or "reminders" in command:
        check_reminders()

    elif "create file" in command:
        create_file(command)

    elif "read file" in command:
        read_file(command)

    elif "delete file" in command:
        delete_file(command)

    elif "write to file" in command:
        write_to_file(command)

    elif "hello" in command:
        respond("Hello! How can I help you?")

    elif "exit" in command or "bye" in command:
        respond("Goodbye!")
        exit()

    else:
        respond("Sorry, I didn't understand that command.")

# 🔽 Main Loop 🔽
def main():
    respond("Hi! I'm Ivy. How can I help you?")
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()
