# This is a quick and dirty photo viewer, created to test out pcista image drawing
# Requires a file named image.png to be in the local directory
import scene
from PIL import Image # I need to import Image from PIL to make it work on computer

class Button(object):
    def __init__(self, x, y):
        self.bounds = scene.Rect(x, y, 80, 80)

    def hit_test(self, x, y):
        return scene.Point(x, y) in self.bounds

    def draw(self):
        scene.fill(1, 1, 0)
        scene.rect(*self.bounds)

class PhotoViewer(scene.Scene):
    #_pgwindowsize = (800, 800)
    _pgwindowtitle = "Photo Viewer"
    def __init__(self):
        scene.run(self, scene.LANDSCAPE)

    def setup(self):
        self.img = Image.open("image.png")
        self.w, self.h = self.img.size
        self.x = self.size.w/2 - self.w/2
        self.y = self.size.h/2 - self.h/2
        self.iid = scene.load_image_file("image.png")
        self.zoom = 1
        self.plusbutton = Button(self.size.w - 100, self.size.h - 100)
        self.minusbutton = Button(self.size.w - 100, self.size.h - 200)
        self.tx = self.ty = 0
        self.touch_id = None

    def draw(self):
        scene.background(0, 0, 1)
        scene.image(self.iid, self.x, self.y, self.w * self.zoom, self.h * self.zoom)
        self.plusbutton.draw()
        self.minusbutton.draw()

    def touch_began(self, touch):
        x, y = touch.location
        if self.plusbutton.hit_test(x, y):
            self.zoom += 1
        elif self.minusbutton.hit_test(x, y):
            if self.zoom:
                self.zoom -= 1
        elif not self.touch_id:
            self.touch_id = touch.touch_id
            self.tx, self.ty = x, y

    def touch_moved(self, touch):
        if touch.touch_id == self.touch_id:
            if self.w * self.zoom > self.size.w or self.h * self.zoom > self.size.h:
                x, y = touch.location
                #px, py = touch.location
                self.x  += x - self.tx
                self.y  += y - self.ty
                self.tx, self.ty = x, y

    def touch_ended(self, touch):
        if touch.touch_id == self.touch_id:
            self.touch_id = None

PhotoViewer()
