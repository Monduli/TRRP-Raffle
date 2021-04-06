### doesn't quite work yet

import requests
from time import time
import os
import tkinter as tk
from tkinter.ttk import *
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self.result_text = ""
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the buttons and input areas.
        """
        # the display has 2 entry fields with 2 labels
        # and a button that generates the random number
        tk.Label(self._master, text="Tweet ID").grid(row=0)
        self.to_set = tk.Label(self._master, text=self.result_text)
        self.to_set.grid(row=2, column=1)
        self.text1 = tk.Entry(self._master)
        self.text1.grid(row=0, column=1)
        self.button = tk.Button(text='Pick Winner', command=self.select_random(self.text1.get())).grid(row=2, column=0)

    def select_random(tweet_id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print('running from', dir_path)

        key = 'cbKZBYMzrzJfWxHdmjBch3Y7N'
        secret = 'onx9HAFIsXB11bDZCpT1FCoXvfRkBPY4qSZYYTQ0C7XlfG1MSe'

        auth_url = 'https://api.twitter.com/oauth2/token'
        data = {'grant_type': 'client_credentials'}
        auth_resp = requests.post(auth_url, auth=(key, secret), data=data)
        token = auth_resp.json()['access_token']

        tweet_id = '1371593697687711746'
        url = 'https://api.twitter.com/1.1/statuses/retweets/%s.json?count=100' % tweet_id
        headers = {'Authorization': 'Bearer %s' % token}
        retweets_resp = requests.get(url, headers=headers)
        retweets = retweets_resp.json()
        retweeters = [r['user']['screen_name'] for r in retweets]

        ts = int(time())
        with open('%s/results/retweets.txt' % (dir_path), 'w') as f_out:
            for r in retweeters:
                f_out.write(r)
                f_out.write('\n')
        print('done')


# create the window
window = tk.Tk()
window.title("Retweet Picker")

# experimental - need to fix
canvas = tk.Canvas(window, width=400, height=300)

# creates the application in the window
app = Application(window)
# run it
app.mainloop()
