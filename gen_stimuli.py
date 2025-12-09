import random
from expyriment import design, control, stimuli, io, misc
import numpy as np

def gen_stimulus0(stimulus_type , scale):
    
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de base pour une forme en T
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    h_line = stimuli.Line((-30 * scale, 0), (30 * scale , 0), line_width=line_thick, colour=color)
    h_line.plot(canvas)
    
    x_offset = 0
    if stimulus_type == 'default':
        x_offset = 0 
    elif stimulus_type == 'diff_topo':
        x_offset = 30 * scale # Touche le bord (Devient un L)
    elif stimulus_type == 'same_topo':
        x_offset = 15 * scale # Décalé, mais reste un T (T asymétrique)

    v_line = stimuli.Line((x_offset, 0), (x_offset, -line_len * scale), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus1(stimulus_type, scale):
    
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((-20 * scale, -30 * scale), (0, -30 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    base_line2 = stimuli.Line((-10 * scale, -30 * scale), (-10 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line2.plot(canvas)

    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = 40 * scale 
    elif stimulus_type == 'same_topo':
        offset = 20 * scale

    v_line = stimuli.Line((-10 * scale, -10 * scale + offset), (20 * scale, -10 * scale + offset), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus2(stimulus_type, scale):
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((10 * scale, 30 * scale), (10 * scale, -30 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    base_line2 = stimuli.Line((10 * scale, -10 * scale), (30 * scale, -10 * scale), line_width=line_thick, colour=color)
    base_line2.plot(canvas)

    base_line3 = stimuli.Line((30 * scale, -10 * scale), (30 * scale, -30 * scale), line_width=line_thick, colour=color)
    base_line3.plot(canvas)
    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = 30 * scale
    elif stimulus_type == 'same_topo':
        offset = 60 * scale

    v_line = stimuli.Line((-30 * scale, 30 * scale - offset), (10 * scale, 30 * scale - offset), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus3(stimulus_type, scale):
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((-30 * scale, -10 * scale), (30 * scale, -10 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    base_line2 = stimuli.Line((-10 * scale, -10 * scale), (-10 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line2.plot(canvas)

    base_line3 = stimuli.Line((-10 * scale, 10 * scale), (20 * scale, 10 * scale), line_width=line_thick, colour=color)
    base_line3.plot(canvas)

    base_line4 = stimuli.Line((20 * scale, 10 * scale), (20 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line4.plot(canvas)
    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = 30 * scale
    elif stimulus_type == 'same_topo':
        offset = 60 * scale

    v_line = stimuli.Line((-30 * scale + offset, -10 * scale), (-30 * scale + offset, -30 * scale), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus4(stimulus_type, scale):
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((-30 * scale, 30 * scale), (-30 * scale, 10 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    base_line2 = stimuli.Line((-30 * scale, 10 * scale), (30 * scale, 10 * scale), line_width=line_thick, colour=color)
    base_line2.plot(canvas)

    base_line3 = stimuli.Line((0, 30 * scale), (0, -30 * scale), line_width=line_thick, colour=color)
    base_line3.plot(canvas)

    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = 30 * scale
    elif stimulus_type == 'same_topo':
        offset = 60 * scale

    v_line = stimuli.Line((0, -30 * scale + offset), (30 * scale, -30 * scale + offset), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus5(stimulus_type, scale):
    canvas = stimuli.Canvas(size=(100 * scale, 100 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((-30 * scale, 10 * scale), (-30 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    base_line2 = stimuli.Line((-30 * scale, 30 * scale), (30 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line2.plot(canvas)

    base_line3 = stimuli.Line((-30 * scale, -30 * scale), (30 * scale, -30 * scale), line_width=line_thick, colour=color)
    base_line3.plot(canvas)

    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = 30 * scale
    elif stimulus_type == 'same_topo':
        offset = 15 * scale

    v_line = stimuli.Line((0 + offset, -30 * scale), (0 + offset, 30 * scale), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas

def gen_stimulus6(stimulus_type, scale):
    canvas = stimuli.Canvas(size=(120 * scale, 120 * scale), colour=None)
    
    # Paramètres de la forme de base
    line_len = 60
    line_thick = 5
    color = (0, 0, 0)
    
    # Barre horizontale (fixe)
    base_line = stimuli.Line((-30 * scale, -30 * scale), (30 * scale, 30 * scale), line_width=line_thick, colour=color)
    base_line.plot(canvas)

    
    offset = 0
    if stimulus_type == 'default':
        offset = 0 
    elif stimulus_type == 'diff_topo':
        offset = np.sqrt(2) * 30 * scale
    elif stimulus_type == 'same_topo':
        offset = np.sqrt(2) * 15 * scale

    v_line = stimuli.Line((-30 * scale + offset/np.sqrt(2) , 30 * scale + offset/np.sqrt(2)), (30 * scale + offset/np.sqrt(2), -30 * scale + offset/np.sqrt(2)), line_width=line_thick, colour=color)
    v_line.plot(canvas)
    
    return canvas
    