import cairocffi as cairo
import sys, copy, math, random
import imageio
from io import BytesIO
from IPython.display import Image, display

def draw(width, height, colors):
    images = []
    
    post = -1
    for i in range(len(colors)):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(surface)
        cr.scale(width, height)
        cr.set_line_width(0.01)           
        pattern = cairo.LinearGradient(0, 0, 1, 1)

        # assign pre and post pointers
        if i == len(colors)-1:
            post = -1
        else:
            post = i+1
            
        if colors[i] != colors[post] and post != -1:
            pattern.add_color_stop_rgb(0, 1, .3, .3) 
            pattern.add_color_stop_rgb(1, .3, .3, 1)
            
        if colors[i] == 0: # blue
            pattern.add_color_stop_rgb(0, 1, 1, 1) 
            pattern.add_color_stop_rgb(1, 0, 0, 1)
            
        else: # red
            pattern.add_color_stop_rgb(0, 1, 0, 0) 
            pattern.add_color_stop_rgb(1, 1, 1, 1)
        
        
        mask = cairo.RadialGradient(0.5, 0.5, 0.25, 0.5, 0.5, 0.5)
        mask.add_color_stop_rgba(0, 0, 0, 0, 1)
        mask.add_color_stop_rgba(0.5, 0, 0, 0, 0)

        cr.set_source(pattern)
        cr.mask(mask)

        surface.write_to_png(f'gradient{i}.png')
        images.append(imageio.imread(f'gradient{i}.png'))

    imageio.mimsave('gradient.gif', images)
