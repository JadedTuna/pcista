# Some imports
import _scene_types
import pygame
import string
import time
import os

# No more evil global variables!
_data = _scene_types._Namespace()
_data.touch         = None
_data.stroke_weight = 0
_data.SIZE_IPHONE   = (320, 480)
_data.SIZE_IPHONE4  = (320, 480)
_data.SIZE_IPHONE5  = (320, 568)

_data.SIZE_IPAD3    = (748, 1024)
_data.DEFSIZE       = _data.SIZE_IPAD3
_data.letters       = string.uppercase + string.lowercase

_data.BG_COLOUR     = (  0,   0,   0)
_data.STROKE_COLOUR = (  0,   0,   0)
_data.FILL_COLOUR   = (255, 255, 255)
_data.TINT_COLOUR   = (255, 255, 255)

_data.LOADED_IMGS   = {}

"""
DRAWING FUNCTIONS
"""

def stroke_weight(weight):
    _data.stroke_weight = weight

def no_stroke():
    stroke_weight(0)

def no_fill():
    fill(0, 0, 0)

def no_tint():
    tint(0, 0, 0)

def load_image(name):
    load_image_file(get_image_path(name))

def image(name, x, y, w=0, h=0):
    if not name in _data.LOADED_IMGS.keys():
        load_image(name)
    _img = _data.LOADED_IMGS[name]
    if w > 0 and h > 0:
        img = pygame.transform.scale(_img, (int(w), int(h)))
    else:
        img = _img
    if h == 0:
        h = img.get_size()[1]
    y = _data.DEFSIZE[1] - (y + h)
    _data.screen.blit(img, (x, y))

def background(r, g, b, a=1.0):
    _data.BG_COLOUR = (r*255., g*255., b*255.)
    
    _data.screen.fill(_data.BG_COLOUR)

def rect(x, y, w, h):
    x, y, w, h = [int(i) for i in (x, y, w, h)]
    y = _data.DEFSIZE[1] - (y + h)
    if _data.stroke_weight > 0:
        pygame.draw.rect(_data.screen, _data.STROKE_COLOUR, (x, y, w, h))
        y += _data.stroke_weight
        x += _data.stroke_weight
        w -= _data.stroke_weight * 2
        h -= _data.stroke_weight * 2
    
    pygame.draw.rect(_data.screen, _data.FILL_COLOUR, (x, y, w, h))

def ellipse(x, y, w, h):
    x, y, w, h = [int(i) for i in (x, y, w, h)]
    y = _data.DEFSIZE[1] - (y + h)
    if _data.stroke_weight > 0:
        pygame.draw.ellipse(_data.screen, _data.STROKE_COLOUR, (x, y, w, h))
        y += _data.stroke_weight
        x += _data.stroke_weight
        w -= _data.stroke_weight * 2
        h -= _data.stroke_weight * 2
    
    pygame.draw.ellipse(_data.screen, _data.FILL_COLOUR, (x, y, w, h))
    
def fill(r, g, b, a=1.0):
    _data.FILL_COLOUR = (r*255., g*255., b*255.)

def stroke(r, g, b, a=1.0):
    _data.STROKE_COLOUR = (r*255., g*255., b*255.)

def tint(r, g, b, a=1.0):
    _data.TINT_COLOUR = (r*255., g*255., b*255.)

def get_image_path(image_name):
    path = os.path.join("Textures", image_name + ".png")
    if os.path.isfile(path):
        return path
    return None

def load_image_file(name):
    if name in _data.LOADED_IMGS.keys():
        unload_image(name)
    img = pygame.image.load(name).convert_alpha()
    _data.LOADED_IMGS[name] = img
    return name

def unload_image(name):
    del _data.LOADED_IMGS[name]

def load_raw_image_data(data, mode, w, h):
    img = pygame.image.fromstring(data, (w, h), mode).convert()
    iid = _data.new_image_id(_data.LOADED_IMGS.keys(), _data.letters)
    _data.LOADED_IMGS[iid] = img
    return iid

def render_text(txt, font_name, font_size, _unknown):
    renderfont = pygame.font.SysFont(font_name, int(font_size))
    img = renderfont.render(txt, _data.anti_alias, _data.TINT_COLOUR)
    
    iid = _data.new_image_id(_data.LOADED_IMGS.keys(), _data.letters)
    _data.LOADED_IMGS[iid] = img
    
    sx, sy = img.get_size()
    return iid, sx, sy

"""
DRAWING FUNCTIONS
"""

def run(scene, orientation, frame_inverval, anti_alias):
    _run(scene, orientation, frame_inverval, anti_alias)
    
    scene._stop()

def _run(scene, orientation, frame_interval, anti_alias):
    if orientation == 2: # LANDSCAPE
        _data.DEFSIZE = _data.DEFSIZE[::-1]
    
    _data.DEFSIZE = getattr(scene,
                            "_pgwindowsize",
                            _data.DEFSIZE)
    pygame.init()
    
    _data.anti_alias = 1#anti_alias
    _data.screen  = pygame.display.set_mode(_data.DEFSIZE)
    pygame.display.set_caption(getattr(scene,
                                        "_pgwindowtitle",
                                        "PyGame scene"))
    clock         = pygame.time.Clock()
    _data.FPS     = 60./frame_interval
    last_time     = time.time()
    
    scene._setup_scene(*_data.DEFSIZE)
     
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                # touch_began
                mouse_pos     = _scene_types.Point(*pygame.mouse.get_pos())
                mouse_pos.y   = _data.DEFSIZE[1] - mouse_pos.y
                _data.touch = _data.new_touch(scene, mouse_pos)
                scene._touch_began(_data.touch.location.x,
                                    _data.touch.location.y,
                                    _data.touch.touch_id)

            elif evt.type == pygame.MOUSEMOTION:
                # touch_moved
                if _data.touch:
                    prev_location = _data.touch.location
                    mouse_pos     = _scene_types.Point(*pygame.mouse.get_pos())
                    mouse_pos.y   = _data.DEFSIZE[1] - mouse_pos.y
                    _data.touch = _data.new_touch(_data.screen,
                                                mouse_pos,
                                                prev_location)
                                                
                    scene._touch_moved(_data.touch.location.x,
                                        _data.touch.location.y,
                                        _data.touch.prev_location.x,
                                        _data.touch.prev_location.y,
                                        _data.touch.touch_id)
            
            elif evt.type == pygame.MOUSEBUTTONUP:
                # touch_ended
                if _data.touch:
                    scene._touch_ended(_data.touch.location.x,
                                        _data.touch.location.y,
                                        _data.touch.touch_id)
                    _data.touch = None
        
        ntime = time.time()
        dt = ntime - last_time
        
        last_time = ntime
        
        scene._draw(dt)
        pygame.display.flip()
        clock.tick(_data.FPS)
    scene._stop()
