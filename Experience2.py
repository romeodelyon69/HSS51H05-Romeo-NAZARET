#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Réplication de l'Expérience 2 : Yousif & Brannon (2025)
Variante : Placement aléatoire CONTRAINT dans un carré central visible.
"""

import random
import math
from expyriment import design, control, stimuli, io, misc
import gen_stimuli
import pyautogui

# =============================================================================
# 1. PARAMÈTRES & CONFIGURATION
# =============================================================================

screen_width, screen_height = pyautogui.size()
scale = min(screen_width / 1024 * 0.8, screen_height / 768 * 0.8)

control.defaults.window_mode = True 
control.defaults.window_size = (screen_width * 0.9, screen_height * 0.9)
design.defaults.experiment_background_colour = (255, 255, 255)
design.defaults.experiment_foreground_colour = (0, 0, 0)

# Temps (en ms)
TIME_CUE = 2500
TIME_TIMEOUT = 10000 

# Configuration de la zone
N_ITEMS = 16
ITEM_SIZE_APPROX = 100 * scale 

# --- NOUVEAUX PARAMÈTRES DE ZONE ---
# Taille du carré central (ex: 700x700 px ajusté à l'échelle)
SQUARE_SIDE = 600 * scale 

# Distance min : un peu réduite pour que tout rentre dans le carré
# 1.2 x taille objet laisse un petit espace mais les "resserre"
MIN_DISTANCE = ITEM_SIZE_APPROX * 1.0

# Nombres d'essais
N_SETS = 7      
N_REPEATS = 1   

# =============================================================================
# 2. FONCTIONS UTILITAIRES
# =============================================================================

def get_random_positions_in_square(n, min_dist, square_side):
    """
    Génère n positions aléatoires (x, y) STRICTEMENT à l'intérieur 
    d'un carré de taille `square_side`.
    """
    positions = []
    max_attempts = 5000 
    
    # Limites pour le centre des objets
    # On soustrait une demi-taille d'objet pour qu'ils ne dépassent pas du cadre
    limit = (square_side / 2) - (ITEM_SIZE_APPROX / math.sqrt(2))

    for _ in range(n):
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts:
            # 1. Tirer une position au hasard DANS LE CARRÉ
            rx = random.uniform(-limit, limit)
            ry = random.uniform(-limit, limit)
            
            # 2. Vérifier collision
            collision = False
            for (px, py) in positions:
                dist = math.sqrt((rx - px)**2 + (ry - py)**2)
                if dist < min_dist:
                    collision = True
                    break 
            
            if not collision:
                positions.append((rx, ry))
                placed = True
            
            attempts += 1
            
        if not placed:
            print("Attention : Impossible de tout faire rentrer dans le carré. Réduisez MIN_DISTANCE ou augmentez SQUARE_SIDE.")
            
    return positions

def draw_stimulus_rotated(set_id, stimulus_type):
    # Génération via gen_stimuli
    if set_id == 0: canvas = gen_stimuli.gen_stimulus0(stimulus_type, scale)
    elif set_id == 1: canvas = gen_stimuli.gen_stimulus1(stimulus_type, scale)
    elif set_id == 2: canvas = gen_stimuli.gen_stimulus2(stimulus_type, scale)
    elif set_id == 3: canvas = gen_stimuli.gen_stimulus3(stimulus_type, scale)
    elif set_id == 4: canvas = gen_stimuli.gen_stimulus4(stimulus_type, scale)
    elif set_id == 5: canvas = gen_stimuli.gen_stimulus5(stimulus_type, scale)
    elif set_id == 6: canvas = gen_stimuli.gen_stimulus6(stimulus_type, scale)
    
    # Rotation aléatoire
    angle = random.randint(0, 359)
    canvas.rotate(angle)
    return canvas

def draw_cue(set_id, stimulus_type):
    if set_id == 0: canvas = gen_stimuli.gen_stimulus0(stimulus_type, scale)
    elif set_id == 1: canvas = gen_stimuli.gen_stimulus1(stimulus_type, scale)
    elif set_id == 2: canvas = gen_stimuli.gen_stimulus2(stimulus_type, scale)
    elif set_id == 3: canvas = gen_stimuli.gen_stimulus3(stimulus_type, scale)
    elif set_id == 4: canvas = gen_stimuli.gen_stimulus4(stimulus_type, scale)
    elif set_id == 5: canvas = gen_stimuli.gen_stimulus5(stimulus_type, scale)
    elif set_id == 6: canvas = gen_stimuli.gen_stimulus6(stimulus_type, scale)
    return canvas

# =============================================================================
# 3. CRÉATION DE L'EXPÉRIENCE
# =============================================================================

exp = design.Experiment(name="Exp 2: Visual Search (Square)")
control.initialize(exp)

block = design.Block(name="Main Block")

target_cats = ['default', 'same_topo'] 
distractor_rels = ['same_topo_rel', 'diff_topo_rel'] 
presence_conds = [True, False]

for repeat in range(N_REPEATS):
    for set_id in range(N_SETS):
        for t_cat in target_cats:
            for d_rel in distractor_rels:
                for is_present in presence_conds:
                    
                    trial = design.Trial()
                    
                    # --- Logique conditions ---
                    target_type_str = t_cat
                    distractor_type_str = ""
                    
                    if t_cat == 'default':
                        if d_rel == 'same_topo_rel':
                            distractor_type_str = 'same_topo'
                        else:
                            distractor_type_str = 'diff_topo'      
                    elif t_cat == 'same_topo':
                        if d_rel == 'same_topo_rel':
                            distractor_type_str = 'default'
                        else:
                            distractor_type_str = 'diff_topo'
                    
                    trial.set_factor("SetID", set_id)
                    trial.set_factor("TargetCategory", t_cat)
                    trial.set_factor("DistractorRelation", d_rel)
                    trial.set_factor("Present", is_present)
                    trial.set_factor("CorrectResp", 'y' if is_present else 'n')
                    
                    # --- Préparation Visuelle ---
                    
                    # 1. Indice (Cue)
                    cue_stim = draw_cue(set_id, target_type_str)
                    cue_container = stimuli.Canvas(size=(200*scale, 200*scale), colour=(255,255,255))
                    cue_text = stimuli.TextLine("Trouvez ceci :", position=(0, 80*scale), text_colour=(0,0,0))
                    cue_text.plot(cue_container)
                    cue_stim.plot(cue_container)
                    trial.add_stimulus(cue_container) 
                    
                    # 2. Tableau de recherche
                    search_array = stimuli.Canvas(size=(screen_width, screen_height), colour=(255,255,255))
                    
                    # A. Dessiner le CADRE (Le carré visible)
                    frame = stimuli.Rectangle(size=(SQUARE_SIDE, SQUARE_SIDE), 
                                              line_width=3, 
                                              colour=(0,0,0)) # Cadre noir
                    frame.plot(search_array)
                    
                    # B. Générer les positions DANS le carré
                    item_positions = get_random_positions_in_square(N_ITEMS, MIN_DISTANCE, SQUARE_SIDE)
                    
                    n_distractors = N_ITEMS
                    if is_present:
                        n_distractors -= 1
                        # Cible
                        target_in_array = draw_stimulus_rotated(set_id, target_type_str)
                        if item_positions:
                            t_pos = item_positions.pop() 
                            target_in_array.position = t_pos
                            target_in_array.plot(search_array)
                        
                    # Distracteurs
                    for i in range(n_distractors):
                        d_stim = draw_stimulus_rotated(set_id, distractor_type_str)
                        if item_positions: 
                            d_pos = item_positions.pop()
                            d_stim.position = d_pos
                            d_stim.plot(search_array)
                        
                    trial.add_stimulus(search_array) 
                    
                    block.add_trial(trial)

block.shuffle_trials()
exp.add_block(block)

# =============================================================================
# 4. DÉROULEMENT
# =============================================================================

control.start(exp)

instr_text = "Cherchez l'objet cible dans le carré.\n\n'y' = PRÉSENT\n'n' = ABSENT"
instr = stimuli.TextBox(instr_text, size=(600, 400), position=(0,0), text_colour=(0,0,0))
instr.present()
exp.keyboard.wait(misc.constants.K_SPACE)

for trial in exp.blocks[0].trials:
    cue = trial.stimuli[0]
    array = trial.stimuli[1]
    
    cue.present()
    exp.clock.wait(TIME_CUE)
    
    array.present()
    
    start_time = exp.clock.time
    key, rt = exp.keyboard.wait_char(['y', 'n'], duration=TIME_TIMEOUT)
    
    if key is None:
        response = "timeout"
        acc = 0
    else:
        response = key
        acc = 1 if response == trial.get_factor("CorrectResp") else 0
        
    exp.data.add([
        trial.get_factor("SetID"),
        trial.get_factor("TargetCategory"),
        trial.get_factor("DistractorRelation"),
        trial.get_factor("Present"),
        trial.get_factor("CorrectResp"),
        response,
        rt,
        acc
    ])

control.end()