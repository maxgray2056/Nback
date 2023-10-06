# -*- coding: utf-8 -*-
"""
Created on Fri May 26 01:33:25 2023

@author: MaxGr
"""



from flask import Flask, render_template, jsonify
import random
import time
from flask import Flask, render_template, jsonify
import random
import time



app = Flask(__name__)

# Game parameters
N = 2  # Number of steps back
score = 0
incorrects = 0
letter_count = 0
current_letter = None
prev_letters = []
game_paused = False



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_letter')
def get_letter():
    global current_letter, prev_letters
    new_letter = generate_letter()
    prev_letters.append(new_letter)
    current_letter = new_letter
    return jsonify({'letter': current_letter})


@app.route('/check_match/<clicked_letter>')
def check_match(clicked_letter):
    global score, incorrects, current_letter, prev_letters

    if game_paused:
        return jsonify({})  # If the game is paused, do not process the click

    if len(prev_letters) >= N + 1 and prev_letters[-N - 1] == current_letter:
        if clicked_letter == 'yes':
            score += 1
    else:
        if clicked_letter == 'no':
            score += 1
        else:
            incorrects += 1

    return jsonify({'score': score, 'incorrects': incorrects})


def generate_letter():
    letters = [chr(i) for i in range(65, 91)]  # A to Z
    return random.choice(letters)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port = 8080)
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    