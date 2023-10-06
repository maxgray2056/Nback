# -*- coding: utf-8 -*-
"""
Created on Fri May 26 01:33:25 2023

@author: MaxGr
"""



from flask import Flask, render_template, jsonify, request
import random
import time
import numpy as np
import datetime



app = Flask(__name__)

# Game parameters
N = 2  # Number of steps back
score = 0
incorrects = 0
letter_count = 0
current_letter = None
letter_list = []
prev_letters = []
game_paused = False
prev2_letter = None

test_index = 0


letters = [chr(i) for i in range(65, 91)]  # A to Z



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nback')
def nback():
    global start_time
    start_time = datetime.datetime.now()

    return render_template('nback.html')


@app.route('/end')
def end():
    global test_index, score, incorrects, letter_count
    
    if score + incorrects == 0:
        correctness = 0
    else:
        correctness = score / (score + incorrects) * 100

    
    # Game ended, collect the required information
    end_time = datetime.datetime.now()
    total_time_cost = end_time - start_time
    total_seconds = total_time_cost.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    
    # Format the output
    output = f"Time: {end_time}\n"
    output += f"Test ID: {test_index}\n"
    output += f"Total Score: {score}\n"
    output += f"Total Incorrects: {incorrects}\n"
    output += f"Total Letters: {letter_count}\n"
    output += f"Correctness: {correctness:.2f}%\n"
    output += f"Total Time Cost: {minutes}:{seconds} \n\n\n"

    print(output)
    
    output_path = 'output.txt'  # Specify the output file path
    with open(output_path, 'a') as file:
        np.savetxt(file, [output], fmt='%s', delimiter=' ')
        
    test_index += 1
    # return render_template('end.html')
    return render_template('end.html', 
                           minutes=minutes,
                           seconds=seconds,
                           score=score, 
                           incorrects=incorrects, 
                           correctness=correctness)





@app.route('/update_score', methods=['POST'])
def update_score():
    global score, incorrects, letter_count
    data = request.get_json()
    score = data.get('score', 0)
    incorrects = data.get('incorrects', 0)
    letter_count = data.get('letterCount', 0)
    return jsonify({'message': 'Score and incorrects updated'})



@app.route('/get_letter')
def get_letter():
    global current_letter, prev_letters
    new_letter, nback = generate_letter()
    prev_letters.append(new_letter)
    current_letter = new_letter
    return jsonify({'letter': current_letter, 'nback': nback})


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



# def generate_letter():
#     letters = [chr(i) for i in range(65, 91)]  # A to Z
#     return random.choice(letters)



def generate_letter():
    global letter_count, score, incorrects


    if len(letter_list) > 2 and random.random() <= 0.5:
        letter = letter_list[-2]
        nback = 1
    else:
        letter = random.choice(letters)
        nback = 0

    while len(letter_list) > 2 and letter == letter_list[-1]:
        letter = random.choice(letters)
        nback = 0
    
    letter_list.append(letter)
    print(letter, score, incorrects)
    
    letter_count += 1

    return letter, nback



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080)
    # app.run()
    
    
# http://99.96.79.236:8080/    
    
    
    
    
    
    
    
    
    
    
    
    
    