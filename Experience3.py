#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Réplication de l'Expérience 3: Yousif & Brannon (2025)
Protocol: Number Comparison (Topology)
Framework: Expyriment
Mise à jour : Utilisation de gen_stimuli pour varier les topologies (Sets 0, 1, 5)
"""

import random
import math
import pyautogui
from expyriment import design, control, stimuli, io, misc
import gen_stimuli  # Import du module de génération

# =============================================================================
# 1. CONFIGURATION ET PARAMÈTRES
# =============================================================================

# --- CHOIX DU MODE (3a ou 3b) ---
# 'lines' = Exp 3a (Compter les segments totaux)
# 'objects' = Exp 3b (Compter les objets totaux)
TASK_MODE = 'lines' 

# Récupération taille écran
screen_width, screen_height = pyautogui.size()
scale = min(screen_width / 1024 * 0.9, screen_height / 768 * 0.9)

# Configuration Expyriment
control.defaults.window_mode = True 
control.defaults.window_size = (int(screen_width * 0.9), int(screen_height * 0.9))
design.defaults.experiment_background_colour = (255, 255, 255) # Blanc
design.defaults.experiment_foreground_colour = (0, 0, 0)       # Noir

TIME_STIMULUS = 1000   
TIME_ISI = 1000        

# Paramètres des objets
ITEM_SIZE = 60 * scale 
LINE_WIDTH = 4
COLOR_BLACK = (0, 0, 0)

# Paramètres des boîtes
BOX_SIZE = 550 * scale         
BOX_OFFSET_X = screen_width * 0.22 

NUMEROSITY_PAIRS = [
    (10, 16), (16, 10),
    (22, 16), (16, 22),
    (16, 16), (16, 16), (16, 16) 
]

N_REPEATS = 4 


USED_SETS = [0, 1, 5] 

# =============================================================================
# 2. INITIALISATION
# =============================================================================

exp = design.Experiment(name=f"Exp 3: Number Comparison ({TASK_MODE})")
control.initialize(exp)

# =============================================================================
# 3. FONCTIONS UTILITAIRES
# =============================================================================

def get_stimulus_from_lib(set_id, topo_type):
    """
    Récupère le stimulus depuis gen_stimuli.py
    topo_type: 'default' (Complexe/T-Junction) ou 'diff_topo' (Simple/L-Junction)
    """
    if set_id == 0:
        return gen_stimuli.gen_stimulus0(topo_type, scale)
    elif set_id == 1:
        return gen_stimuli.gen_stimulus1(topo_type, scale)
    elif set_id == 5:
        return gen_stimuli.gen_stimulus5(topo_type, scale)
    return None

def draw_instruction_shape(shape_type):
    """
    Dessin simplifié UNIQUEMENT pour la phase d'instruction (Segments et Croix).
    On garde cela séparé pour ne pas mélanger avec les stimuli complexes du test.
    """
    canvas = stimuli.Canvas(size=(ITEM_SIZE*1.5, ITEM_SIZE*1.5), colour=None)
    length = ITEM_SIZE
    
    if shape_type == 'segment': 
        stimuli.Line((0, -length/2), (0, length/2), line_width=LINE_WIDTH, colour=COLOR_BLACK).plot(canvas)
    elif shape_type == 'X': 
        stimuli.Line((-length/2, -length/2), (length/2, length/2), line_width=LINE_WIDTH, colour=COLOR_BLACK).plot(canvas)
        stimuli.Line((-length/2, length/2), (length/2, -length/2), line_width=LINE_WIDTH, colour=COLOR_BLACK).plot(canvas)
    return canvas

def draw_box_outline(canvas, center_x, center_y, size):
    """Dessine un cadre carré vide"""
    half = size / 2
    # Haut
    stimuli.Line((center_x - half, center_y + half), (center_x + half, center_y + half), line_width=3, colour=COLOR_BLACK).plot(canvas)
    # Bas
    stimuli.Line((center_x - half, center_y - half), (center_x + half, center_y - half), line_width=3, colour=COLOR_BLACK).plot(canvas)
    # Gauche
    stimuli.Line((center_x - half, center_y - half), (center_x - half, center_y + half), line_width=3, colour=COLOR_BLACK).plot(canvas)
    # Droite
    stimuli.Line((center_x + half, center_y - half), (center_x + half, center_y + half), line_width=3, colour=COLOR_BLACK).plot(canvas)

def get_random_positions_in_rect(n, rect_w, rect_h, x_offset, min_dist):
    """Placement aléatoire sans chevauchement"""
    positions = []
    max_attempts = 3000
    
    x_min = x_offset - (rect_w / 2) + (ITEM_SIZE/1.2)
    x_max = x_offset + (rect_w / 2) - (ITEM_SIZE/1.2)
    y_min = -(rect_h / 2) + (ITEM_SIZE/1.2)
    y_max = (rect_h / 2) - (ITEM_SIZE/1.2)

    for _ in range(n):
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts:
            rx = random.uniform(x_min, x_max)
            ry = random.uniform(y_min, y_max)
            
            collision = False
            for (px, py) in positions:
                if math.sqrt((rx - px)**2 + (ry - py)**2) < min_dist:
                    collision = True
                    break
            
            if not collision:
                positions.append((rx, ry))
                placed = True
            attempts += 1
            
    return positions

# =============================================================================
# 4. PRÉPARATION
# =============================================================================


# --- CRÉATION DES BLOCS ---
block = design.Block(name="Main Block")

for repeat in range(N_REPEATS):
    for pair in NUMEROSITY_PAIRS:
        
        # 1. Choix aléatoire du Set pour cet essai (0, 1 ou 5)
        # Cela introduit la variété demandée (T, F, H vs L, Ligne, U)
        current_set = random.choice(USED_SETS)
        
        # 2. Assignation des côtés
        # 0 = Gauche a la topo COMPLEXE (Default), Droite a la topo SIMPLE (Diff)
        side_assignment = random.choice([0, 1])
        
        trial = design.Trial()
        
        # 'default' = Topologie Complexe (ex: T, F, H)
        # 'diff_topo' = Topologie Simple (ex: L, ligne pliée, U)
        if side_assignment == 0:
            n_left, n_right = pair[0], pair[1]
            type_left, type_right = 'default', 'diff_topo'
            more_t_side = 'left'
        else:
            n_left, n_right = pair[1], pair[0]
            type_left, type_right = 'diff_topo', 'default'
            more_t_side = 'right'
            
        trial.set_factor("SetID", current_set)
        trial.set_factor("N_Left", n_left)
        trial.set_factor("N_Right", n_right)
        trial.set_factor("Type_Left", type_left)
        trial.set_factor("Type_Right", type_right)
        trial.set_factor("More_T_Side", more_t_side)
        
        scene = stimuli.Canvas(size=(screen_width, screen_height), colour=(255,255,255))
        
        # Dessiner les boîtes
        draw_box_outline(scene, -BOX_OFFSET_X, 0, BOX_SIZE)
        draw_box_outline(scene, BOX_OFFSET_X, 0, BOX_SIZE)
        
        min_dist = ITEM_SIZE * 1.5 # Distance pour éviter les superpositions
        
        # --- GÉNÉRATION GAUCHE ---
        pos_left = get_random_positions_in_rect(n_left, BOX_SIZE, BOX_SIZE, -BOX_OFFSET_X, min_dist)
        for p in pos_left:
            # Appel à gen_stimuli via notre fonction helper
            s = get_stimulus_from_lib(current_set, type_left)
            # Rotation aléatoire pour que la topologie prime sur l'orientation
            s.rotate(random.randint(0, 359)) 
            s.position = p
            s.plot(scene)
            
        # --- GÉNÉRATION DROITE ---
        pos_right = get_random_positions_in_rect(n_right, BOX_SIZE, BOX_SIZE, BOX_OFFSET_X, min_dist)
        for p in pos_right:
            s = get_stimulus_from_lib(current_set, type_right)
            s.rotate(random.randint(0, 359)) 
            s.position = p
            s.plot(scene)
            
        trial.add_stimulus(scene)
        block.add_trial(trial)

block.shuffle_trials()
exp.add_block(block)

# =============================================================================
# 5. DÉROULEMENT
# =============================================================================

control.start(exp)

lbl_left = stimuli.TextLine("'G' pour GAUCHE", position=(-300, -350), text_colour=(100,100,100))
lbl_right = stimuli.TextLine("'D' pour DROITE", position=(300, -350), text_colour=(100,100,100))

for trial in exp.blocks[0].trials:
    
    scene = trial.stimuli[0]
    
    lbl_left.present(clear=False)
    lbl_right.present(clear=False)
    scene.present(clear=False)
    
    # --- ATTENTE DE LA RÉPONSE ---
    # Attendre la réponse sans limite de temps
    key, rt = exp.keyboard.wait_char(['g', 'd', misc.constants.K_ESCAPE])
    
    # Vérifier si l'utilisateur veut quitter
    if key == misc.constants.K_ESCAPE:
        break
    
    # Effacer l'écran après la réponse
    exp.screen.clear()
    exp.screen.update()
    
    # Données
    resp_side = 'left' if key == 'g' else 'right'
    # "More T Side" signifie ici le côté avec la topologie complexe (Set Default)
    chose_complex_topo = 1 if resp_side == trial.get_factor("More_T_Side") else 0
    
    correct_numerosity = 0
    if trial.get_factor("N_Left") > trial.get_factor("N_Right") and resp_side == 'left':
        correct_numerosity = 1
    elif trial.get_factor("N_Right") > trial.get_factor("N_Left") and resp_side == 'right':
        correct_numerosity = 1
    elif trial.get_factor("N_Right") == trial.get_factor("N_Left"):
        correct_numerosity = -1 

    exp.data.add([
        TASK_MODE,
        trial.get_factor("SetID"),
        trial.get_factor("N_Left"),
        trial.get_factor("N_Right"),
        trial.get_factor("Type_Left"),
        trial.get_factor("Type_Right"),
        key,
        rt,
        chose_complex_topo,      
        correct_numerosity 
    ])
    
    exp.clock.wait(TIME_ISI)

control.end()