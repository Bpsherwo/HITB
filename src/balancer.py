import tkinter as tk
import numpy as np
import itertools as it
import re
import os
from statistics import mean
from tkinter import *

root = tk.Tk()

zPLAYER_LIST = {}
zTEAM_SIZE = 4
best_iteration = {}
correctCheck = False
DECIMAL_PLACES = 2
PRINT_ALL_COMBINATIONS = False
PRINT_BEST_COMBINATION = True
NUMBER_OF_BEST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM = 1
NUMBER_OF_WORST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM = 1
icon_path = os.path.join("src", "observerteamico.ico")
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)

f = open("k.py", "r")
palette = f.readlines()

page_color = str(re.findall(r"'(#[A-Fa-f0-9]+)'", str(palette[0]))).replace("[","").replace("]","").replace("'","")
text_color = str(re.findall(r"'(#[A-Fa-f0-9]+)'", str(palette[1]))).replace("[","").replace("]","").replace("'","")
button_color = str(re.findall(r"'(#[A-Fa-f0-9]+)'", str(palette[2]))).replace("[","").replace("]","").replace("'","")
field_color = str(re.findall(r"'(#[A-Fa-f0-9]+)'", str(palette[3]))).replace("[","").replace("]","").replace("'","")

if page_color == "#FFFFFF":
    root.iconbitmap(default="eagleteamico.ico")
else:
    root.iconbitmap(default="cobrateamico.ico")

l_page_color = '#FFFFFF'
l_text_color = '#060607'
l_button_color = '#D7D9DC'
l_field_color = '#CECECE'

d_page_color = '#313338'
d_text_color = '#FFFCF9'
d_button_color = '#404249'
d_field_color = '#3C3D42'

player1name = tk.StringVar()
player2name = tk.StringVar()
player3name = tk.StringVar()
player4name = tk.StringVar()
player5name = tk.StringVar()
player6name = tk.StringVar()
player7name = tk.StringVar()
player8name = tk.StringVar()

player1csr = tk.IntVar()
player2csr = tk.IntVar()
player3csr = tk.IntVar()
player4csr = tk.IntVar()
player5csr = tk.IntVar()
player6csr = tk.IntVar()
player7csr = tk.IntVar()
player8csr = tk.IntVar()

def determine_team_combos():
    number_of_teams = int(len(zPLAYER_LIST) / zTEAM_SIZE)
    highest_players = determine_best_players(number_of_teams)
    lowest_players = determine_worst_players(number_of_teams)
    team_combos = [list(i) for i in it.combinations(zPLAYER_LIST, zTEAM_SIZE)
                   # Omit teams containing more than a certain number of the best players
                   if len(set(highest_players).intersection(i)) <=
                   NUMBER_OF_BEST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM
                   # Omit teams containing more than a certain number of the worst players
                   if len(set(lowest_players).intersection(i)) <=
                   NUMBER_OF_WORST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM]
    #print('Number of player combos for teams: ', str(len(team_combos)))
    return team_combos

def determine_combos_of_team_combos(team_combos):
    number_of_teams = int(len(zPLAYER_LIST) / zTEAM_SIZE)
    combos_of_team_combos = [i for i in it.combinations(team_combos, number_of_teams) if
                             len(set(it.chain(*i))) == len(list(it.chain(*i)))]
    return combos_of_team_combos

def determine_best_players(no_team):
    return sorted(zPLAYER_LIST, key=lambda k: sum(zPLAYER_LIST[k]) / len(zPLAYER_LIST[k]),
                  reverse=True)[-no_team:]

def determine_worst_players(no_team):
    return sorted(zPLAYER_LIST, key=lambda k: sum(zPLAYER_LIST[k]) / len(zPLAYER_LIST[k]),
                  reverse=False)[-no_team:]

def fast_round(number):
    p = 10 ** DECIMAL_PLACES
    try:
        p = int(number * p + 0.5) / p
    except ValueError: 
        print("Invalid CSR values.")
        p = 0
    return p

def member_elos(members):
    return [np.average(zPLAYER_LIST[member])
            for member in members]

def team_mean(members):
    return fast_round(np.average(member_elos(members)))

def team_stdev(members):
    return fast_round(np.std(member_elos(members)))

def iteration_mean_and_stdev(team_means):
    it_mean = fast_round(np.average(team_means))
    it_stdev = fast_round(np.std(team_means))
    return it_mean, it_stdev

def calculate_iteration_mean_stdev(combos):
    def calculate_team_mean_stdev(iteration):
        iteration_dict = {'Team ' + str(team + 1): {'Players': iteration[team],
                                                    'CSRs': member_elos(iteration[team]),
                                                    'Team Mean': team_mean(iteration[team]),
                                                    'Team StDev': team_stdev(iteration[team])}
                          for team in range(len(iteration))}

        iteration_mean, iteration_stdev = iteration_mean_and_stdev([iteration_dict[team_no]['Team Mean']
                                                                    for team_no in iteration_dict])

        iteration_dict['Iteration Team Elo Mean'] = iteration_mean
        iteration_dict['Iteration Team Elo StDev'] = iteration_stdev
        return iteration_dict

    return {'Iteration ' + str(iteration_no + 1): calculate_team_mean_stdev(combos[iteration_no])
            for iteration_no in range(len(combos))}

def find_best_iteration(data):
    #print('---------===========Best Iteration===========---------')
    min_iteration_elo_stdev = min([data[i]['Iteration Team Elo StDev'] for i in data])
    for i in data:
        if data[i]['Iteration Team Elo StDev'] == min_iteration_elo_stdev:
            return data[i]
        
def check_more_than_one_team():
    if len(zPLAYER_LIST) >= zTEAM_SIZE:
        return True
    else:
        return False

def check_player_number_multiple():
    if len(zPLAYER_LIST) % zTEAM_SIZE == 0:
        return True, 0
    else:
        return False, zTEAM_SIZE - len(zPLAYER_LIST) % zTEAM_SIZE

def initialize():
    global correctCheck
    if not check_more_than_one_team():
        print("You don't have enough players. Please add more.")

    player_multiple_check, players_remaining = check_player_number_multiple()
    if player_multiple_check:
        correctCheck = True
    else:
        if players_remaining == 1:
            print('You have to add ' + str(players_remaining) + ' more contestant to make equal teams of ' + str(
                zTEAM_SIZE) + '.')
        else:
            print('You have to add ' + str(players_remaining) + ' more contestants to make equal teams of ' + str(
                zTEAM_SIZE) + '.')
            
def DarkTheme():
    window_frame.config(background=d_page_color)
    form_frame.config(background=d_page_color)
    output_frame.config(background=d_page_color)
    title_label.config(background=d_page_color, foreground=d_text_color)
    subtitle_label.config(background=d_page_color, foreground=d_text_color)
    generate_teams_button.config(background=d_button_color, foreground=d_text_color)
    gamertags_label.config(background=d_page_color, foreground=d_text_color)
    csrs_label.config(background=d_page_color, foreground=d_text_color)
    entry_p1name.config(background=d_field_color, foreground=d_text_color)
    entry_p1csr.config(background=d_field_color, foreground=d_text_color)
    entry_p2name.config(background=d_field_color, foreground=d_text_color)
    entry_p2csr.config(background=d_field_color, foreground=d_text_color)
    entry_p3name.config(background=d_field_color, foreground=d_text_color)
    entry_p3csr.config(background=d_field_color, foreground=d_text_color)
    entry_p4name.config(background=d_field_color, foreground=d_text_color)
    entry_p4csr.config(background=d_field_color, foreground=d_text_color)
    entry_p5name.config(background=d_field_color, foreground=d_text_color)
    entry_p5csr.config(background=d_field_color, foreground=d_text_color)
    entry_p6name.config(background=d_field_color, foreground=d_text_color)
    entry_p6csr.config(background=d_field_color, foreground=d_text_color)
    entry_p7name.config(background=d_field_color, foreground=d_text_color)
    entry_p7csr.config(background=d_field_color, foreground=d_text_color)
    entry_p8name.config(background=d_field_color, foreground=d_text_color)
    entry_p8csr.config(background=d_field_color, foreground=d_text_color)
    eagle_team_label.config(background=d_page_color, foreground=d_text_color)
    cobra_team_label.config(background=d_page_color, foreground=d_text_color)
    eagleAvgCsr.config(background=d_page_color, foreground=d_text_color)
    cobraAvgCsr.config(background=d_page_color, foreground=d_text_color)
    eaglep1.config(background=d_page_color, foreground=d_text_color)
    eaglep2.config(background=d_page_color, foreground=d_text_color)
    eaglep3.config(background=d_page_color, foreground=d_text_color)
    eaglep4.config(background=d_page_color, foreground=d_text_color)
    cobrap1.config(background=d_page_color, foreground=d_text_color)
    cobrap2.config(background=d_page_color, foreground=d_text_color)
    cobrap3.config(background=d_page_color, foreground=d_text_color)
    cobrap4.config(background=d_page_color, foreground=d_text_color)
    root.iconbitmap(default="cobrateamico.ico")
    f = open('k.py', 'w')
    f.write("page_color = '#313338'\ntext_color = '#FFFCF9'\nbutton_color = '#404249'\nfield_color = '#3C3D42'")
    f.close()

def LightTheme():
    window_frame.config(background=l_page_color)
    form_frame.config(background=l_page_color)
    output_frame.config(background=l_page_color)
    title_label.config(background=l_page_color, foreground=l_text_color)
    subtitle_label.config(background=l_page_color, foreground=l_text_color)
    generate_teams_button.config(background=l_button_color, foreground=l_text_color)
    gamertags_label.config(background=l_page_color, foreground=l_text_color)
    csrs_label.config(background=l_page_color, foreground=l_text_color)
    entry_p1name.config(background=l_field_color, foreground=l_text_color)
    entry_p1csr.config(background=l_field_color, foreground=l_text_color)
    entry_p2name.config(background=l_field_color, foreground=l_text_color)
    entry_p2csr.config(background=l_field_color, foreground=l_text_color)
    entry_p3name.config(background=l_field_color, foreground=l_text_color)
    entry_p3csr.config(background=l_field_color, foreground=l_text_color)
    entry_p4name.config(background=l_field_color, foreground=l_text_color)
    entry_p4csr.config(background=l_field_color, foreground=l_text_color)
    entry_p5name.config(background=l_field_color, foreground=l_text_color)
    entry_p5csr.config(background=l_field_color, foreground=l_text_color)
    entry_p6name.config(background=l_field_color, foreground=l_text_color)
    entry_p6csr.config(background=l_field_color, foreground=l_text_color)
    entry_p7name.config(background=l_field_color, foreground=l_text_color)
    entry_p7csr.config(background=l_field_color, foreground=l_text_color)
    entry_p8name.config(background=l_field_color, foreground=l_text_color)
    entry_p8csr.config(background=l_field_color, foreground=l_text_color)
    eagle_team_label.config(background=l_page_color, foreground=l_text_color)
    cobra_team_label.config(background=l_page_color, foreground=l_text_color)
    eagleAvgCsr.config(background=l_page_color, foreground=l_text_color)
    cobraAvgCsr.config(background=l_page_color, foreground=l_text_color)
    eaglep1.config(background=l_page_color, foreground=l_text_color)
    eaglep2.config(background=l_page_color, foreground=l_text_color)
    eaglep3.config(background=l_page_color, foreground=l_text_color)
    eaglep4.config(background=l_page_color, foreground=l_text_color)
    cobrap1.config(background=l_page_color, foreground=l_text_color)
    cobrap2.config(background=l_page_color, foreground=l_text_color)
    cobrap3.config(background=l_page_color, foreground=l_text_color)
    cobrap4.config(background=l_page_color, foreground=l_text_color)
    root.iconbitmap(default="eagleteamico.ico")
    f = open('k.py', 'w')
    f.write("page_color = '#FFFFFF'\ntext_color = '#060607'\nbutton_color = '#D7D9DC'\nfield_color = '#CECECE'")
    f.close()
            
def runBalancer():
    global zPLAYER_LIST
    global best_iteration
    zPLAYER_LIST = {}
    zPLAYER_LIST[player1name.get()] = [player1csr.get()]
    zPLAYER_LIST[player2name.get()] = [player2csr.get()]
    zPLAYER_LIST[player3name.get()] = [player3csr.get()]
    zPLAYER_LIST[player4name.get()] = [player4csr.get()]
    zPLAYER_LIST[player5name.get()] = [player5csr.get()]
    zPLAYER_LIST[player6name.get()] = [player6csr.get()]
    zPLAYER_LIST[player7name.get()] = [player7csr.get()]
    zPLAYER_LIST[player8name.get()] = [player8csr.get()]
    initialize()
    combo_teams = determine_team_combos()
    combo_iterations = determine_combos_of_team_combos(combo_teams)
    final_data = calculate_iteration_mean_stdev(combo_iterations)
    if PRINT_BEST_COMBINATION:
        best_iteration = str(find_best_iteration(final_data))
        best_iteration = re.findall(r'\[.*?\]', best_iteration)
        best_iteration = str(best_iteration).replace('[','').replace(']','').replace('"','').replace("'", '')
        best_iteration = best_iteration.split(", ")
        final_eagle_team_players = best_iteration[0:4]
        final_eagle_team_csrs = best_iteration[4:8]
        final_eagle_team_csrs = list(map(float, final_eagle_team_csrs))
        final_cobra_team_players = best_iteration[8:12]
        final_cobra_team_csrs = best_iteration[12:16]
        final_cobra_team_csrs = list(map(float, final_cobra_team_csrs))
        try:
            eaglep1.config(text=final_eagle_team_players[0])
            eaglep2.config(text=final_eagle_team_players[1])
            eaglep3.config(text=final_eagle_team_players[2])
            eaglep4.config(text=final_eagle_team_players[3])
            cobrap1.config(text=final_cobra_team_players[0])
            cobrap2.config(text=final_cobra_team_players[1])
            cobrap3.config(text=final_cobra_team_players[2])
            cobrap4.config(text=final_cobra_team_players[3])
            eagleAvgCsr.config(text="Team Avg. CSR: {}".format(mean(final_eagle_team_csrs)))
            cobraAvgCsr.config(text="Team Avg. CSR: {}".format(mean(final_cobra_team_csrs)))
        except IndexError:
            print("Not enough players.")

window_frame = tk.Frame(width=500, height=50, background=page_color)
window_frame.pack(side="top", fill='x', padx=0, pady=0)
form_frame = tk.Frame(width=500, height=150, background=page_color)
form_frame.pack(side="top", fill='both', padx=0, pady=0)
output_frame = tk.Frame(width=500, height=200,background=page_color)
output_frame.pack(side="top", fill='both', padx=0, pady=0, expand=True)

main_menu = Menu(window_frame)
root.config(menu=main_menu)
options_menu = Menu(main_menu)
main_menu.add_cascade(label="Themes", menu=options_menu)
options_menu.add_command(label="Dark Mode", command=DarkTheme)
options_menu.add_command(label="Light Mode", command=LightTheme)

root.geometry("500x500")
root.title("HITB v1.0")
root.resizable(False, False)

title_label = tk.Label(window_frame, background=page_color, foreground=text_color, text="Halo Infinite Team Balancer", font=(('Segoe UI'), 20))
title_label.pack(side="top", fill='both', padx=0, pady=0)

subtitle_label = tk.Label(window_frame, background=page_color, foreground=text_color, text="Please enter names into the left columns, and CSRs into the right columns.", font=(('Segoe UI'), 8))
subtitle_label.pack(side="top", fill='both', padx=0, pady=0)

generate_teams_button = tk.Button(window_frame, background=button_color, foreground=text_color, text="Generate Teams", command=runBalancer, relief='raised', border=2, width=30)
generate_teams_button.pack(side="top", fill='y', padx=0, pady=10)

gamertags_label = tk.Label(form_frame, background=page_color, foreground=text_color, text="Gamertags:", font=(('Segoe UI'), 8))
gamertags_label.grid(row=0,column=0, pady=3, padx=75)

csrs_label = tk.Label(form_frame, background=page_color, foreground=text_color, text="CSRs:", font=(('Segoe UI'), 8))
csrs_label.grid(row=0,column=1, pady=3, padx=30)

entry_p1name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player1name)
entry_p1name.grid(row=1,column=0, pady=3, padx=80)

entry_p1csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player1csr)
entry_p1csr.grid(row=1,column=1, pady=3, padx=0)

entry_p2name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player2name)
entry_p2name.grid(row=2,column=0, pady=3, padx=80)

entry_p2csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player2csr)
entry_p2csr.grid(row=2,column=1, pady=3, padx=0)

entry_p3name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player3name)
entry_p3name.grid(row=3,column=0, pady=3, padx=80)

entry_p3csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player3csr)
entry_p3csr.grid(row=3,column=1, pady=3, padx=0)

entry_p4name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player4name)
entry_p4name.grid(row=4,column=0, pady=3, padx=80)

entry_p4csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player4csr)
entry_p4csr.grid(row=4,column=1, pady=3, padx=0)

entry_p5name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player5name)
entry_p5name.grid(row=5,column=0, pady=3, padx=80)

entry_p5csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player5csr)
entry_p5csr.grid(row=5,column=1, pady=3, padx=0)

entry_p6name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player6name)
entry_p6name.grid(row=6,column=0, pady=3, padx=80)

entry_p6csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player6csr)
entry_p6csr.grid(row=6,column=1, pady=3, padx=0)

entry_p7name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player7name)
entry_p7name.grid(row=7,column=0, pady=3, padx=80)

entry_p7csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player7csr)
entry_p7csr.grid(row=7,column=1, pady=3, padx=0)

entry_p8name = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player8name)
entry_p8name.grid(row=8,column=0, pady=3, padx=80)

entry_p8csr = tk.Entry(form_frame, background=field_color, foreground=text_color, textvariable=player8csr)
entry_p8csr.grid(row=8,column=1, pady=3, padx=0)

eagle_team_label = tk.Label(output_frame, background=page_color, foreground=text_color, text="Eagle Team:", font=(('Segoe UI'), 12))
eagle_team_label.grid(row=0,column=0, pady=5, padx=100)

cobra_team_label = tk.Label(output_frame, background=page_color, foreground=text_color, text="Cobra Team:", font=(('Segoe UI'), 12))
cobra_team_label.grid(row=0,column=1, pady=5, padx=12)

eaglep1 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
eaglep1.grid(row=1,column=0, pady=0, padx=0)

eaglep2 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
eaglep2.grid(row=2,column=0, pady=0, padx=0)

eaglep3 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
eaglep3.grid(row=3,column=0, pady=0, padx=0)

eaglep4 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
eaglep4.grid(row=4,column=0, pady=0, padx=0)

eagleAvgCsr = tk.Label(output_frame, background=page_color, foreground=text_color, text="Team Avg. CSR: N/A")
eagleAvgCsr.grid(row=5,column=0, pady=0, padx=0)

cobrap1 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
cobrap1.grid(row=1,column=1, pady=0, padx=0)

cobrap2 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
cobrap2.grid(row=2,column=1, pady=0, padx=0)

cobrap3 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
cobrap3.grid(row=3,column=1, pady=0, padx=0)

cobrap4 = tk.Label(output_frame, background=page_color, foreground=text_color, text='')
cobrap4.grid(row=4,column=1, pady=0, padx=0)

cobraAvgCsr = tk.Label(output_frame, background=page_color, foreground=text_color, text="Team Avg. CSR: N/A")
cobraAvgCsr.grid(row=5,column=1, pady=0, padx=0)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()