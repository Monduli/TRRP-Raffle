### Twitter Follower Picker Framework by @Monduli
# This is not for public use. This is just a small showcase of programming for my Github/Resume.
# It also won't function without information you would have to be a Twitter API Dev to know.
# 
# This program will accept a URL of a tweet and pick a random person that retweeted it, displaying it
# on the GUI. It requires a Twitter API key and secret to function. It will re-seed every time it picks
# someone based on the system clock, so the result is generally always random. 

import requests
from time import time
import tkinter as tk
from tkinter.ttk import *
import random

class Application(tk.Frame):
    """
    Class that spawns the window and also picks the winner based on the text inputs in the window.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self.counter = 0
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the buttons and input areas.
        Has 6 Labels (one per entry field and two at the bottom) and one button.
        """
        tk.Label(self._master, text="Twitter Follower Picker (Requires API Access!)").grid(row=0, columnspan=5)
                
        self.label1 = tk.Label(self._master, text="Key:")
        self.label1.grid(row=1, column=0)
        self.text1 = tk.Entry(self._master)
        self.text1.grid(row=1, column=1, columnspan=4)

        self.label2 = tk.Label(self._master, text="Secret:")
        self.label2.grid(row=2, column=0)
        self.text2 = tk.Entry(self._master)
        self.text2.grid(row=2, column=1, columnspan=4)
        
        self.label3 = tk.Label(self._master, text="URL:")
        self.label3.grid(row=3, column=0)
        self.text3 = tk.Entry(self._master)
        self.text3.grid(row=3, column=1, columnspan=4)

        self.label5 = tk.Label(self._master, text="The winner is: ")
        self.label5.grid(row=5, column=0)
        self.label6 = tk.Label(self._master, text="None.")
        self.label6.grid(row=5, column=1, columnspan=4)

        self.button = tk.Button(text='Pick Winner', command=lambda: self.select_random(self.text1.get(), self.text2.get(), self.text3.get()))
        self.button.grid(row=4, columnspan=5)

    def select_random(self, key, secret, url):
        """
        Selects a random retweeter of a tweet and returns it to the GUI.
        Note: You must have access to the Twitter Developer UI to use this!!
        I will not give you a key and a secret to use.
        As such, this is merely a framework to most people.
        """
        if key == "" or secret == "" or url == "":
            self.counter += 1
            self.label6['text'] = self.counter
        else:
            auth_url = 'https://api.twitter.com/oauth2/token'
            data = {'grant_type': 'client_credentials'}
            auth_resp = requests.post(auth_url, auth=(key, secret), data=data)
            token = auth_resp.json()['access_token']

            headers = {'Authorization': 'Bearer %s' % token}
            retweets_resp = requests.get(url, headers=headers)
            retweets = retweets_resp.json()
            retweeters = [r['user']['screen_name'] for r in retweets]

            ts = int(time())
            random.seed(ts)
            random_num = random.randint(0, len(retweeters))
            self.label6['text'] = retweeters[random_num]


# create the window
window = tk.Tk()
window.title("Retweet Picker")

# creates the application in the window
app = Application(window)
# run it
app.mainloop()
