import random
import math

class _Namespace(dict):
    """
    This is not default class of _scene_types; _scene module
    uses it to store information.
    """
    def __getattr__(self, attr):
        return self[attr]
    
    def __setattr__(self, attr, value):
        self[attr] = value
    
    def new_touch_id(self, scene):
        """
        Generate new touch id and make sure it is not taken.
        """
        id_length = 10
        return "0x1c876130" # We currently don't support multitouch

    def new_touch(self, scene, location, prev_location=None):
        """
        Create a new _scene_types.Touch object.
        """
        if not prev_location:
            prev_location = Point(0, 0)
        return Touch(location.x, location.y,
                       prev_location.x, prev_location.y,
                       self.new_touch_id(scene))
    
    def new_image_id(self, ids, letters):
        id_length = 10
        while True:
            iid = "".join([random.choice(letters) for _i in range(id_length)])
            if not iid in ids: return iid

# Color
def _color_as_tuple(color):
    return (color.r, color.g, color.b, color.a)

# Point

def _point_as_tuple(point):
    return (point.x, point.y)

def _point_distance(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx * dx + dy * dy)

# Rect

def _rect_contains(r1, other):
    if isinstance(other, Rect):
        return (r1.x <= other.x and
                    r1.y <= other.y and
                    r1.w + r1.x >= other.w + other.x and
                    r1.h + r1.y >= other.h + other.y)
    elif isinstance(other, Point):
        return (other.x >= r1.x and
                    other.y >= r1.y and
                    other.x <= r1.x + r1.w and
                    other.y <= r1.y + r1.h)
    
    else:
        return False

def _rect_as_tuple(rect):
    return (rect.x, rect.y, rect.w, rect.h)

def _rect_bottom(rect):
    return rect.y

def _rect_center(rect):
    return Point(rect.x + rect.w / 2, rect.y + rect.h / 2)

def _rect_intersects(r1, r2):
    for point in (Point(r1.x, r1.y),
                    Point(r1.x + r1.w, r1.y),
                    Point(r1.x, r1.y + r1.h),
                    Point(r1.x + r1.w, r1.y + r1.h)):
        if point in r2:
            return True
    for point in (Point(r2.x, r2.y),
                    Point(r2.x + r2.w, r2.y),
                    Point(r2.x, r2.y + r2.h),
                    Point(r2.x + r2.w, r2.y + r2.h)):
        if point in r1:
            return True
    return False

def _rect_left(rect):
    return rect.x

def _rect_origin(rect):
    return Point(rect.x, rect.y)

def _rect_right(rect):
    return rect.x + rect.w

def _rect_size(rect):
    return Size(rect.w, rect.h)

def _rect_top(rect):
    return rect.y + rect.h

# Size
def _size_as_tuple(size):
    return (size.w, size.h)
    

##############################################################################
# Classes
##############################################################################

class Color(object):
    def __eq__(self, other):
        if isinstance(other, Color):
            return self.as_tuple() == other.as_tuple()
        else:
            return False
    
    def __getitem__(self, index):
        return getattr(self, ("r", "g", "b", "a")[index])
    
    def __getstate__(self):
        return self.as_tuple()
    
    def __init__(self, r=1.0, g=1.0, b=1.0, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def __iter__(self):
        return (val for val in self.as_tuple())
    
    def __len__(self):
        return len(self.as_tuple())
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return "Color(r=%d, g=%d, b=%d, a=%d)" % self.as_tuple()
    
    def __setitem__(self, item, value):
        settattr(self, ("r", "g", "b", "a")[item], value)
    
    def __setstate__(self, state):
        self.r, self.g, self.b, self.a = state
    
    as_tuple   = _color_as_tuple
    
    def todict(self):
        """
        Return a new dict which maps field names to their values.
        """
        return {"r": self.r,
                    "g": self.g,
                    "b": self.b,
                    "a": self.a}
    
class Point(object):
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.as_tuple() == other.as_tuple()
        else:
            return False
    
    def __getitem__(self, index):
        return getattr(self, ("x", "y")[index])
    
    def __getstate__(self):
        return self.as_tuple()
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return (val for val in self.as_tuple())
    
    def __len__(self):
        return len(self.as_tuple())
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return "Point(x=%d, y=%d)" % self.as_tuple()
    
    def __setitem__(self, item, value):
        settattr(self, ("x", "y")[item], value)
    
    def __setstate__(self, state):
        self.x, self.y = state
    
    as_tuple   = _point_as_tuple
    distance   = _point_distance
    
    def todict(self):
        """
        Return a new dict which maps field names to their values.
        """
        return {"x": self.x,
                    "y": self.y}

class Rect(object):
    __contains__ = _rect_contains
    
    def __eq__(self, other):
        if isinstance(other, Rect):
            return self.as_tuple() == other.as_tuple()
        else:
            return False
    
    def __getitem__(self, index):
        return getattr(self, ("x", "y", "w", "h")[index])
    
    def __getstate__(self):
        return self.as_tuple()
    
    def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def __iter__(self):
        return (val for val in self.as_tuple())
    
    def __len__(self):
        return len(self.as_tuple())
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return "Rect(%.1f, %.1f, %.1f, %.1f)" % self.as_tuple()
    
    def __setitem__(self, item, value):
        settattr(self, ("x", "y", "w", "h")[item], value)
    
    def __setstate__(self, state):
        self.x, self.y, self.w, self.h = state
    
    as_tuple   = _rect_as_tuple
    bottom     = _rect_bottom
    center     = _rect_center
    intersects = _rect_intersects
    left       = _rect_left
    origin     = _rect_origin
    right      = _rect_right
    size       = _rect_size
    
    def todict(self):
        """
        Return a new dict which maps field names to their values.
        """
        return {"x": self.x,
                    "y": self.y,
                    "w": self.w,
                    "h": self.h}
    
    top        = _rect_top

class Size(object):
    def __eq__(self, other):
        if isinstance(other, Size):
            return (other.w == self.w and
                        other.h == self.h)
        else:
            return False
    
    def __getitem__(self, index):
        return getattr(self, ("w", "h")[index])
    
    def __getstate__(self):
        return self.as_tuple()
    
    def __init__(self, w=0.0, h=0.0):
        self.w = w
        self.h = h
    
    def __iter__(self):
        return (val for val in self.as_tuple())
    
    def __len__(self):
        return len(self.as_tuple())
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return "Size(%.1f, %.1f)" % self.as_tuple()
    
    def __setitem__(self, item, value):
        settattr(self, ("w", "h")[item], value)
    
    def __setstate__(self, state):
        self.w, self.h = state
    
    as_tuple   = _size_as_tuple
    
    def todict(self):
        """
        Return a new dict which maps field names to their values.
        """
        return {"w": self.w,
                    "h": self.h}
    
    top        = _rect_top

class Touch(object):
    """
    Represents a single touch on the screen. Each Touch object has a unique
    touch_id that is also used for hashing. The x, y, prev_x, and prev_y
    attributes define the touch's location in screen coordinates.
    """
    
    def __eq__(self, other_touch):
        if isinstance(other_touch, Touch):
            return self.touch_id == other_touch.touch_id
        else:
            return False
    
    def __hash__(self):
        raise NotImplementedError
    
    def __init__(self, x, y, prev_x, prev_y, touch_id):
        self.location = Point(x, y)
        self.prev_location = Point(prev_x, prev_y)
        self.touch_id = touch_id
        self.layer = None
