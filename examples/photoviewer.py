# This is a quick and dirty photo viewer, created to test out pcista image drawing
# Requires a file named image.png to be in the local directory
from scene import *
from PIL import Image

class Button(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 80
        self.h = 80
        self.bounds = Rect(self.x, self.y, self.w, self.h)
    
    def hit_test(self, x, y):
        return Point(x, y) in self.bounds
    
    def draw(self):
        fill(1, 1, 0)
        rect(self.x, self.y, self.w, self.h)

class PhotoViewer(Scene):
    #_pgwindowsize = (800, 800)
    _pgwindowtitle = "Photo Viewer"
    def setup(self):
        self.img = Image.open("image.png")
        self.w, self.h = self.img.size
        self.x = self.size.w/2 - self.w/2
        self.y = self.size.h/2 - self.h/2
        self.iid = load_image_file("image.png")
        self.zoom = 1
        self.plusbutton = Button(self.size.w - 100, self.size.h - 100)
        self.minusbutton = Button(self.size.w - 100, self.size.h - 200)
        self.tx = self.ty = 0
        self.touch_id = None
    
    def draw(self):
        background(0, 0, 1)
        image(self.iid, self.x, self.y, self.w * self.zoom, self.h * self.zoom)
        self.plusbutton.draw()
        self.minusbutton.draw()
    
    def touch_began(self, touch):
        x, y = touch.location
        if self.plusbutton.hit_test(x, y):
            self.zoom += 1
        elif self.minusbutton.hit_test(x, y):
            if self.zoom != 0:
                self.zoom -= 1
        elif self.touch_id == None:
            self.touch_id = touch.touch_id
            self.tx, self.ty = x, y
    
    def touch_moved(self, touch):
        if touch.touch_id == self.touch_id:
            if self.w * self.zoom > self.size.w or self.h * self.zoom > self.size.h:
                x, y = touch.location
                px, py = touch.location
                self.x  += x - self.tx
                self.y  += y - self.ty
                self.tx, self.ty = x, y
    
    def touch_ended(self, touch):
        if touch.touch_id == self.touch_id:
            self.touch_id = None

run(PhotoViewer(), LANDSCAPE)
