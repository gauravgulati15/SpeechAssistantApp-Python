import speech_recognition as sr
import webbrowser
from time import ctime
import time
import playsound
import os
import random
from gtts import gTTS
from pyttsx3 import engine


class person:
    name = ''
    def setName(self, name):
        self.name = name

class asis:
    name = 'Jarvis'
    def setName(self, name):
        self.name = name



def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def engine_speak(text):
    text = str(text)
    engine.say(text)
    engine.runAndWait()

person_obj = person()
asis_obj = asis()

r = sr.Recognizer()

def record_audio(ask = ""):
    with sr.Microphone() as source: 
        r.adjust_for_ambient_noise(source,duration=1) 
        if ask:
            engine_speak(ask)
        audio = r.listen(source) 
        print('Done Listening') 
        voice_data = ''
        try:
           voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:    
           engine_speak("I did not get that")
        except sr.RequestError:                
           engine_speak("Sorry, the Service Down")  
        print(">>", voice_data.lower())
        return voice_data

def engine_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='hi')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(asis_obj.name + ":", audio_string) # print what app said
    os.remove(audio_file)

def respond(voice_data):
    voice_data = voice_data.lower()
    exe = False
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = ["hey, how can I help you" + person_obj.name, "hey, what's up?" + person_obj.name, "I'm listening" + person_obj.name, "how can I help you?" + person_obj.name, "hello" + person_obj.name]
        greet = greetings[random.randint(0,len(greetings)-1)]
        engine_speak(greet)
        exe = True
    
    # 2; name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        exe = True
        if person_obj.name:
            engine_speak("My name is " + asis_obj.name + " But you can change that. ")
        else:
            engine_speak("my name is Jarvis . what's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        engine_speak("okay, i will remember that " + person_name)
        person_obj.setName(person_name) # remember name in person object
        exe = True
    
    if there_exists(["your name should be"]):
        asis_name = voice_data.split("be")[-1].strip()
        engine_speak("okay, i will remember that my name is " + asis_name)
        asis_obj.setName(asis_name) # remember name in asis object
        exe = True

    if 'what is my name' in voice_data:
        engine_speak('your name is ' + person_name)
        exe = True

     # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        engine_speak("I'm very well, thanks for asking " + person_obj.name)
        exe = True

    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it"]):
        exe = True
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = hours + " hours and " + minutes + "minutes"
        engine_speak(time)
    
    # 5: search google
    if "search on google" in voice_data:
        exe = True
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        engine_speak("Here is what I found for" + search + "on google")

    # 6: search youtube
    if "search on youtube" in voice_data:
        exe = True
        search_term = record_audio('What do you want to search for?')
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + search_term + "on youtube")
    
    # 7: to find location
    if 'find location'in voice_data:
        exe = True
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        engine_speak('Here is the location of '+location)

    # 8: weather
    if there_exists(["weather"]):
        exe = True
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        engine_speak("Here is what I found for on google")

    # 9: stone paper scisorrs
    if there_exists(["game"]):
        exe = True
        voice_data = record_audio("choose among rock paper or scissor")
        moves=["rock", "paper", "scissor"]

        condition = True
    
        while condition == True:
            cmove=random.choice(moves)
            pmove=voice_data
            condition = False
            if pmove not in moves:
                pmove = record_audio("you spoke wrong word. choose among rock paper or scissor")

            engine_speak("The computer chose " + cmove)
            engine_speak("You chose " + pmove)
            if pmove==cmove:
                engine_speak("the match is draw")
            elif pmove== "rock" and cmove== "scissor":
                engine_speak("Player wins")
            elif pmove== "rock" and cmove== "paper":
                engine_speak("Computer wins")
            elif pmove== "paper" and cmove== "rock":
                engine_speak("Player wins")
            elif pmove== "paper" and cmove== "scissor":
                engine_speak("Computer wins")
            elif pmove== "scissor" and cmove== "paper":
                engine_speak("Player wins")
            elif pmove== "scissor" and cmove== "rock":
                engine_speak("Computer wins")
            else:
                condition = record_audio("You spoke wrong word again. if you want to continue say true")
                condition = condition.title()
            if condition == False:
                engine_speak("Exiting Game")
            
    # 10: toss a coin
    if 'flip the coin' in voice_data:
        exe = True
        engine_speak("Flippping the coin")
        moves=["head", "tails"]   
        cmove=random.choice(moves)
        engine_speak("I get " + cmove)

    # 14: to search wikipedia for definition
    if there_exists(["definition of"]):
        exe = True
        definition=record_audio("what do you need the definition of")
        url='https://en.wikipedia.org/wiki/'+definition
        webbrowser.get().open(url)

    #  15: goodbye
    if there_exists(["exit", "quit", "goodbye"]):
        exe = True
        engine_speak('Have a great day ' + person_obj.name)
        exit()
    # 16: if you spoke something else which is not mentioned above  
    elif exe == False:
        engine_speak('I do not understand please say something else')

time.sleep(1)
engine_speak('How Can I help You??')

while 1:
    voice_data=''
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond
     