#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Réplication de l'Expérience 1b : Yousif & Brannon (2025) - Perceiving Topological Relations
Protocol: Speeded Comparison Task
Framework: Expyriment
"""

import random
from expyriment import design, control, stimuli, io, misc
import gen_stimuli
import pyautogui

# =============================================================================
# 1. PARAMÈTRES & CONFIGURATION
# =============================================================================

screen_width, screen_height = pyautogui.size()
scale = min(screen_width / 1024 * 0.9, screen_height / 768 * 0.9)

control.defaults.window_mode = True  
control.defaults.window_size = (screen_width * 0.9, screen_height * 0.9)  
design.defaults.experiment_background_colour = (255, 255, 255)
design.defaults.experiment_foreground_colour = (0, 0, 0) 

TIME_PRIME = 1000
TIME_ISI = 1000
TIME_TIMEOUT = 10000  

GRID_POSITIONS = [
    (-200 * scale, 150 * scale), (0, 150 * scale), (200 * scale, 150 * scale),  
    (-200 * scale, -150 * scale), (0, -150 * scale), (200 * scale, -150 * scale) 
]
CIRCLE_RADIUS = 90 * scale

N_SETS = 7
N_REPEATS = 2    

# =============================================================================
# 2. GÉNÉRATION DES STIMULI (PROCÉDURALE)
# =============================================================================

def draw_stimulus(set_id, stimulus_type):
    """
    Génère un stimulus visuel basé sur l'ID du set et le type.
    
    Args:
        set_id (int): L'identifiant du set (0-5) - permettrait de varier les formes.
        stimulus_type (str): 'default', 'same_topo', 'diff_topo'
    """
    if set_id == 0:
        canvas = gen_stimuli.gen_stimulus0(stimulus_type, scale)
    elif set_id == 1:
        canvas = gen_stimuli.gen_stimulus1(stimulus_type, scale)
    elif set_id == 2:
        canvas = gen_stimuli.gen_stimulus2(stimulus_type, scale)
    elif set_id == 3:
        canvas = gen_stimuli.gen_stimulus3(stimulus_type, scale)
    elif set_id == 4:
        canvas = gen_stimuli.gen_stimulus4(stimulus_type, scale)
    elif set_id == 5:
        canvas = gen_stimuli.gen_stimulus5(stimulus_type, scale)
    elif set_id == 6:
        canvas = gen_stimuli.gen_stimulus6(stimulus_type, scale)
    
    return canvas


def get_placeholders():
    """Crée les 6 cercles de la grille """
    circles = stimuli.Canvas(size=(800 * scale, 600 * scale), colour=(255,255,255))
    for pos in GRID_POSITIONS:
        c = stimuli.Circle(radius=CIRCLE_RADIUS, position=pos, line_width=2, colour=(0,0,0))
        c.plot(circles)
    return circles

# =============================================================================
# 3. CRÉATION DE L'EXPÉRIENCE
# =============================================================================

exp = design.Experiment(name="Exp 1b: Topological Perception")
control.initialize(exp)
block = design.Block(name="Main Block")

# Types d'essais 
# 1. Default -> Default (Réponse: SAME)
# 2. Default -> Same Topo (Réponse: DIFFERENT)
# 3. Default -> Diff Topo (Réponse: DIFFERENT)
trial_definitions = [
    {'type': 'same',       'resp': 's', 'stim2_type': 'default'},
    {'type': 'same_topo',  'resp': 'd', 'stim2_type': 'same_topo'},
    {'type': 'diff_topo',  'resp': 'd', 'stim2_type': 'diff_topo'}
]

# 7 sets * 3 types * 2 répétitions = 42 essais
all_trials = []

for repeat in range(N_REPEATS):
    for set_id in range(N_SETS):
        for t_def in trial_definitions:
            trial = design.Trial()
            
            trial.set_factor("SetID", set_id)
            trial.set_factor("TrialType", t_def['type'])
            trial.set_factor("CorrectResp", t_def['resp'])
            trial.set_factor("Stim2Category", t_def['stim2_type'])
             
            stim1 = draw_stimulus(set_id, 'default')
            stim2 = draw_stimulus(set_id, t_def['stim2_type'])
            
            pos_indices = list(range(len(GRID_POSITIONS)))
            idx1 = random.choice(pos_indices)
            pos_indices.remove(idx1) 
            idx2 = random.choice(pos_indices)
            
            trial.set_factor("Pos1_Idx", idx1)
            trial.set_factor("Pos2_Idx", idx2)
            
            trial.add_stimulus(stim1)
            trial.add_stimulus(stim2)
            
            block.add_trial(trial)

block.shuffle_trials() 
exp.add_block(block)

# =============================================================================
# 4. DÉROULEMENT (TRIAL LOOP)
# =============================================================================

control.start(exp)

instr = stimuli.TextBox("Des formes vont vous être présentées. Une première va s'afficher puis disparaître, et une seconde va alors apparaître.\n\nAppuyez sur 's' pour SAME, 'd' pour DIFFÉRENT. Appuyez sur ESPACE pour commencer.", 
                         size = (600, 400),position=(0,0), text_colour=(0,0,0))
instr.present()
exp.keyboard.wait(misc.constants.K_SPACE)

placeholders = get_placeholders()

for trial in exp.blocks[0].trials:
    stim1 = trial.stimuli[0]
    stim2 = trial.stimuli[1]
    
    stim1.position = GRID_POSITIONS[trial.get_factor("Pos1_Idx")]
    stim2.position = GRID_POSITIONS[trial.get_factor("Pos2_Idx")]
    
    placeholders.present()
    exp.clock.wait(500)
    
    placeholders.present(clear=False)
    stim1.present(clear=False, update=True)
    exp.clock.wait(TIME_PRIME)
    
    placeholders.present() 
    exp.clock.wait(TIME_ISI)
    
    placeholders.present(clear=False)
    stim2.present(clear=False, update=True)

    start_time = exp.clock.time
    key, rt = exp.keyboard.wait_char(['s', 'd'], duration=TIME_TIMEOUT)
    
    if key is None:
        response = "timeout"
        acc = 0
    else:
        response = key
        acc = 1 if response == trial.get_factor("CorrectResp") else 0

    exp.data.add([
        trial.get_factor("SetID"),
        trial.get_factor("TrialType"),
        trial.get_factor("Stim2Category"),
        trial.get_factor("Pos1_Idx"),
        trial.get_factor("Pos2_Idx"),
        trial.get_factor("CorrectResp"),
        response,
        rt,
        acc
    ])

# Fin
control.end()