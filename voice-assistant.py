from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import wikipedia
import sys
from selenium import webdriver
import webbrowser
import smtplib
import imghdr
from email.message import EmailMessage
import pyautogui
from pyautogui import *
from time import sleep
import imdb
from datetime import datetime
from tkinter import *
import PIL
from PIL import Image, ImageDraw
import pyqrcode
import png
from pyqrcode import QRCode


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def load():
    from tqdm import tqdm
    import time
    
    for i in tqdm (range (101), desc = "Loading...", ascii=False, ncols = 75):
        time.sleep(0.01)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(f"You said : {said}")
        except Exception as e:
            print("Exception : " + str(e))
    return said.lower()



def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def WishMe():
    hour = int(datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    
    else:
        speak("Good Evening ")
    
    speak("I am Ghost Sir")


def get_events(day, service):
    #Call the calender API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)


    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found, sir')
    else:
        if len(events) > 1:
            speak(f"you have {len(events)} events on this day, sir")
        else :
            speak(f"you have {len(events)} event on this day, sir")
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = str(start_time.split(":")[:2])
                start_time = start_time + "a m"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + str(start_time.split(":")[1:2])
                start_time = start_time + "p m"

            speak(event["summary"] + "at" + start_time )


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year += 1

    if day < today.day and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_week != -1 :
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif +=7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year) 

def qrcodedev():
    speak("Enter the link.")
    data = str(input("Enter the link :"))
    date = datetime.now()
    file_name = str(date).replace(":","-") + "-qrcode.png"
    img = pyqrcode.create(data)
    img.png(file_name, scale=8)
    

def lasttime():
    with open('data.txt', 'r') as l:
        last_run = l.read()

    start_run_time = datetime.now()
    last_time = datetime.strptime(last_run, "%Y-%m-%d %H:%M:%S.%f")
    total = start_run_time - last_time
    lastdate = str(total)

    if lastdate.split(",")[0] == True:
        try:
            days = lastdate.split(",")[0]
            hours = lastdate.split(",")[1].split(".")[0].split(":")[0]
            minutes = lastdate.split(",")[1].split(".")[0].split(":")[1]
            seconds = lastdate.split(",")[1].split(".")[0].split(":")[2]
            microseconds = lastdate.split(",")[1].split(".")[1]
            speak("It's been "+ days  + hours + " hours " + minutes + " minutes " + seconds + " seconds and " + microseconds + " microseconds since the last activity." )
        except:
            None
    else:
        try:
            hours = lastdate.split(".")[0].split(":")[0]
            minutes = lastdate.split(".")[0].split(":")[1]
            seconds = lastdate.split(".")[0].split(":")[2]
            microseconds = lastdate.split(".")[1]
            speak("It's been "+ hours + " hours " + minutes + " minutes " + seconds + " seconds and " + microseconds + " microseconds since the last activity.")
        except:
            None



def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def send_email():
    user_mail = os.environ.get("testmail")
    user_pass = os.environ.get("apppassword")
    speak("Enter the subject")
    subject = get_audio()
    speak("what should I say?")
    body = get_audio()

    contacts = []
    speak("How many contacts do you want to send ?")
    n = int(input("Number of contacts you want to send :"))
    for i in range(n):
        speak("Enter the email address")
        con = input("Enter the email address :")
        contacts.append(con)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = user_mail
    msg['To'] = contacts
    msg.set_content(body)

    speak("Do u want to send Images ?")
    ques = str(input( "(y \ n) :" ))

    if ques.lower() == "y":
        Images = []
        speak("How many images do you want to send ?")
        n = int(input("Number of Images you want to send :"))
        for i in range(n):
            speak("Enter the file names ?")
            im = input("Enter the file names :")
            Images.append(im)

        for file in Images:
            with open(file, "rb") as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    speak("Do u want to send documents ?")
    ques1 = input("(y \ n) :" )

    if ques1.lower() == "y":
        files = []
        speak("How many documents do you want to send ?")
        n = int(input("Number of documents you want to send :"))
        for i in range(n):
            speak("Enter the file names")
            doc = input("Enter the file names :")
            files.append(doc)

        for file in files:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = f.name

            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user_mail, user_pass)
        smtp.send_message(msg)

def direction_map():
    speak("Where do you want to go?")
    fromloc = get_audio()
    speak("Where are you now?")
    toloc = get_audio()
    webbrowser.open("https://www.google.com/maps/dir/" + fromloc + "/" + toloc)

def place_map():     
    speak("Which place do you want to check")
    location = get_audio()
    webbrowser.open("https://www.google.com/maps/place/" + location)
        
def date_today():
    from datetime import date
    date_ = date.today()
    speak(f"Sir, the date is {date_}")

def time_now():
    import time
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S", t)
    speak(f"Sir, the time is {current_time}")

def day_today():
    from datetime import datetime
    day_ = datetime.today().strftime('%A')
    speak(f"Sir, today is {day_}")

def spotify():
    press('Win')
    typewrite("spotify")
    sleep(2)
    press('enter')
    sleep(9)
    press('tab')
    press('enter')
    sleep(3)
    press('tab')
    press('tab')
    press('enter')

def imdbreview():
    movideDB = imdb.IMDb()
    search = movideDB.search_movie(film)
    id = search[0].getID()
    movie = movideDB.get_movie(id)

    title = search[0]['title']
    kind = search[0]['kind']
    print(kind.capitalize() + " : " + title)

    year = search[0]['year']
    print("Year of Release : " + str(year))

    rating = movie.data['rating']
    print("Rating : " + str(rating))

    print("Cast : ")
    for i in range(3):
        casting = movie.data['cast'][i]
        print(casting)

    try:
        director = movie.data['director']
        num = int(len(director))
        if num == 1:
            print("Director : ")
        if num > 1:
            print("Directors : ")
        for n in range(num):
            print(director[n])
    except:
        None

    speak("Sir, the " + kind + "was released in the year " + str(year) + "and has a rating of " + str(rating) + "."  )


def stop():
    with open('data.txt', 'w') as f:
        last_run_time = datetime.now()
        f.write(str(last_run_time))
    speak("Have a good day, Sir")
    sys.exit()

def shutdown():
    speak("Are you sure, you want to shutdown your Laptop?")
    choice = get_audio()
    if choice == "yes":
        speak("Shutting down !")
        os.system("shutdown /s /t 0")
        sys.exit()
    else:
        speak("Do something interesting !")

def logoff():
    speak("Are you sure, you want to logoff your Laptop?")
    choice = get_audio()
    if choice == "yes":
        speak("Logging Off !")
        os.system("shutdown /l")
        sys.exit()
    else:
        speak("Do something interesting !")

def restart():
    speak("Are you sure, you want to restart your Laptop?")
    choice = get_audio()
    if choice == "yes":
        speak("Restarting your computer !")
        os.system("shutdown /r")
        sys.exit()
    else:
        speak("Do something interesting !")
                


WishMe()
Wake = "ghost"
SERVICE = authenticate_google()
lasttime()
speak("How can I help you?, sir")

while True:
    print("Listening...")
    text = get_audio()

    if text.count(Wake) > 0:
        speak("How can I help you?, sir")
        text = get_audio()

    Stop_str = ["stop it", "please stop", 'stop the program', "stop it please"]
    for phrase in Stop_str:
        if phrase in text:
            stop()

    date_str = ["what is the date", "what date is it" , "today's date"]
    for phrase in date_str:
        if phrase in text:
            date_today()
            break

    time_str = ["what is the time", "what time is it" , "time now"]
    for phrase in time_str:
        if phrase in text:
            time_now()
            break       

    day_str = ["what day is it", "what is today" , "which day", "which day is it"]
    for phrase in day_str:
        if phrase in text:
            day_today()
            break 

        if "shutdown the computer" in text:
            shutdown()
            break
    

        if "log off the computer" in text:
            logoff()
            break
            

        if "restart the computer" in text:
            restart()
            break
        

        if "hello" in text:
            speak("hello sir!")
            break

        if "what is your name" in text:
            speak("My name is Ghost")
            break
            
        if "who is your master" in text:
            speak("My master is Jithin Lakshman")
            break
        
        
        Calendar_str = ["what do i have", "do i have plans", "am i busy", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december","monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for phrase in Calendar_str:
            if phrase in text:
                date = get_date(text)
                if date:
                    get_events(date, SERVICE)
                else:
                    speak("Sorry, It was not clear !, sir")

        Note_str = ["remember this", "write this down", "note"]
        for phrase in Note_str:
            if phrase in text:
                speak("Tell me, Sir. What should I write?")
                note_text = get_audio()
                note(note_text)
                speak("Note is ready, Sir")

        if 'open wikipedia' in text:
            speak("What should I search Sir?")
            text = get_audio()
            print("Searching Wikipedia....")
            
            try: 
                text = text.replace("wikipedia", "")
                results = wikipedia.summary(text, sentences=5)
                speak("Do you want to note it sir ?")
                text = get_audio() 
                
                if "yes" in text:
                    note(results)
                    speak("Sir, According to Wikipedia")
                    speak(results)
                if "no" in text:
                    speak("Sir, According to Wikipedia")
                    speak(results)
            except:
                speak("Sorry, It was not clear, sir")

        if 'open spotify' in text:
            spotify()
            break

        if 'find the rating' in text:
            load()
            speak("What do you want to search, SIr?")
            film = get_audio()
            try:
                imdbreview()
                break
            except:
                speak("Sorry, It was not clear, sir")
                break

        if "make qr code" in text:
            qrcodedev()
            break

        if "open map" in text:
            speak("Do you want to open a direction ?")
            text = get_audio()
            if text == "yes":
                direction_map()
                speak("Search has been completed")
                break
            elif text == "no":
                place_map()
                speak("Search has been completed")
                break
            else:
                speak("Sorry, It was not clear, sir")


        if 'open google' in text:
            speak("What should I search, sir ?")
            text = get_audio()
            
            try: 
                new = 2
                url = "https://www.google.com/?#q="
                webbrowser.open(url + text, new=new)
                speak("Search has been completed!, sir")
            except:
                speak("Sorry, It was not clear, sir")


        if 'open youtube' in text:
            speak("What should I search sir ?")
            text = get_audio()
            
            try: 
                url = "https://www.youtube.com/results?search_query="
                webbrowser.open(url + text)
                speak("Search has been completed!, sir")
            except:
                speak("Sorry, It was not clear, sir")


        if 'open facebook' in text:
            try: 
                fbusername = os.environ.get("fbname")
                fbpassword = os.environ.get("fbpass")

                url = "https://www.facebook.com/"

                driver = webdriver.Chrome("J:\\Downloads\\chromedriver")

                driver.get(url)

                driver.find_element_by_id("email").send_keys(fbusername)
                driver.find_element_by_id("pass").send_keys(fbpassword)
                driver.find_element_by_id("loginbutton").click()
                speak("Facebook is open!, sir")
            except:
                speak("Sorry, It was not clear, sir")
        
        if 'open moodle' in text:
            try:
                username = os.environ.get("iitname")
                password = os.environ.get("iitpass")

                url = "https://courses.iitm.ac.in/login/index.php"

                driver = webdriver.Chrome("J:\\Downloads\\chromedriver")

                driver.get(url)

                driver.find_element_by_id("username").send_keys(username)
                driver.find_element_by_id("password").send_keys(password)
                driver.find_element_by_id("loginbtn").click()
            except:
                speak("Sorry, It was not clear, sir")

        if 'open whatsapp' in text:
            try:
                webbrowser.open("https://web.whatsapp.com/")
            except:
                speak("Sorry, It was not clear, sir")

        if 'play music' in text:
            try:
                music_dir = 'D:\\music'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
            except:
                speak("Sorry, It was not clear, sir")
        
        Email_str = ["send email", "send a mail", "send mail"]
        for phrase in Email_str:
            if phrase in text:
                try:
                    send_email()
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send the Email")

        

        if 'open visual studio' in text:
            path_code = "J:\\Microsoft VS Code\\Code.exe"
            os.startfile(path_code)

        if 'open telegram' in text:
            path_gram = "C:\\Users\\jithi\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
            os.startfile(path_gram)

        if "open codecogs" in text:
            webbrowser.open("https://latex.codecogs.com/legacy/eqneditor/editor.php")

        if "open udemy" in text:
            webbrowser.open("https://www.udemy.com/home/my-courses/learning/")

        if "open kindle" in text:
            path_kindle = "C:\\Users\\jithi\\AppData\\Local\\Amazon\\Kindle\\application\\Kindle.exe"
            os.startfile(path_kindle)