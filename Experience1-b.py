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

# Paramètres de l'écran (Fond blanc comme dans la Fig 3a )
screen_width, screen_height = pyautogui.size()
scale = min(screen_width / 1024 * 0.9, screen_height / 768 * 0.9)

control.defaults.window_mode = True  # Mettre à False pour le plein écran
control.defaults.window_size = (screen_width * 0.9, screen_height * 0.9)  # Taille de la fenêtre
design.defaults.experiment_background_colour = (255, 255, 255)
design.defaults.experiment_foreground_colour = (0, 0, 0) # Texte noir

# Temps (en ms) [cite: 197, 568]
TIME_PRIME = 1000
TIME_ISI = 1000
TIME_TIMEOUT = 10000  # 10 secondes max

# Configuration des Stimuli
GRID_POSITIONS = [
    (-200 * scale, 150 * scale), (0, 150 * scale), (200 * scale, 150 * scale),  # Ligne haut
    (-200 * scale, -150 * scale), (0, -150 * scale), (200 * scale, -150 * scale) # Ligne bas
]
CIRCLE_RADIUS = 90 * scale # Taille des cercles placeholders

# Nombres d'essais [cite: 36]
N_SETS = 7      # 7 sets d'objets uniques
N_REPEATS = 2    # Chaque configuration vue 2 fois

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

# Création des blocks et essais
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
            # Création de l'objet Trial
            trial = design.Trial()
            
            # Stockage des variables (Facteurs)
            trial.set_factor("SetID", set_id)
            trial.set_factor("TrialType", t_def['type'])
            trial.set_factor("CorrectResp", t_def['resp'])
            trial.set_factor("Stim2Category", t_def['stim2_type'])
            
            # Pré-chargement des stimuli pour cet essai pour performance optimale
            # Stim 1 est TOUJOURS le 'default' 
            stim1 = draw_stimulus(set_id, 'default')
            stim2 = draw_stimulus(set_id, t_def['stim2_type'])
            
            # Choix des positions [cite: 204, 206]
            # Pos 1 aléatoire, Pos 2 aléatoire MAIS différente de Pos 1
            pos_indices = list(range(len(GRID_POSITIONS)))
            idx1 = random.choice(pos_indices)
            pos_indices.remove(idx1) # Enlever la position utilisée
            idx2 = random.choice(pos_indices)
            
            trial.set_factor("Pos1_Idx", idx1)
            trial.set_factor("Pos2_Idx", idx2)
            
            # Attacher les stimuli (extra) pour y accéder dans la boucle
            trial.add_stimulus(stim1)
            trial.add_stimulus(stim2)
            
            block.add_trial(trial)

block.shuffle_trials() # Randomisation totale [cite: 201]
exp.add_block(block)

# =============================================================================
# 4. DÉROULEMENT (TRIAL LOOP)
# =============================================================================

control.start(exp)

# Instructions
instr = stimuli.TextLine("Appuyez sur 's' pour PAREIL, 'd' pour DIFFÉRENT. Appuyez sur ESPACE pour commencer.", 
                         text_colour=(0,0,0))
instr.present()
exp.keyboard.wait(misc.constants.K_SPACE)

placeholders = get_placeholders()

# Boucle principale
for trial in exp.blocks[0].trials:
    
    # 1. Préparation
    stim1 = trial.stimuli[0]
    stim2 = trial.stimuli[1]
    
    # Positionner les stimuli
    stim1.position = GRID_POSITIONS[trial.get_factor("Pos1_Idx")]
    stim2.position = GRID_POSITIONS[trial.get_factor("Pos2_Idx")]
    
    # 2. Séquence temporelle de l'essai 
    
    # a. Fixation (Optionnel mais recommandé, ici juste les cercles vides)
    placeholders.present()
    exp.clock.wait(500)
    
    # b. Stimulus 1 (Prime) - 1000ms
    placeholders.present(clear=False)
    stim1.present(clear=False, update=True)
    exp.clock.wait(TIME_PRIME)
    
    # c. Délai (ISI) - 1000ms (On ré-affiche juste les cercles vides)
    placeholders.present() 
    exp.clock.wait(TIME_ISI)
    
    # d. Stimulus 2 (Target) - Jusqu'à réponse
    placeholders.present(clear=False)
    stim2.present(clear=False, update=True)
    
    # e. Enregistrement réponse [cite: 197, 568]
    # Touches: s (115) et d (100)
    start_time = exp.clock.time
    key, rt = exp.keyboard.wait_char(['s', 'd'], duration=TIME_TIMEOUT)
    
    # 3. Sauvegarde des données
    if key is None:
        response = "timeout"
        acc = 0
    else:
        response = key
        # Vérification précision
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