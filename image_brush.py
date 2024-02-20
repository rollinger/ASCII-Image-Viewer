import numpy

class RectangularBrush():
    TYPE = "rectangular"
    X_FACTOR = 2
    Y_FACTOR = 2
    TRANSPARENT_PX = '-'
    BRUSH_PX = '#'
    CENTER_PX = 'X'

    def __init__(self, x=0, y=0):
        # (0,0) is a point brush, (-1,-1) disables the brush
        self.set_dimensions(x,y)

    def set_dimensions(self, x=0, y=0):
        if x <= -1 or y <= -1:
            self.width, self.height = -1, -1
        else:
            self.width, self.height = self.X_FACTOR * x + 1, self.Y_FACTOR * y + 1
        self.bitmask = self.make_bitmask()
        self.sprite = self.style_bitmask()
        return self.width, self.height

    def set_width(self, w):
        return self.set_dimensions(w, self.half_height)

    def set_height(self, h):
        return self.set_dimensions(self.half_width, h)

    @property
    def half_width(self):
        return int(self.width/2)

    @property
    def half_height(self):
        return int(self.height/2)

    @property
    def disabled(self):
        # Disabled if bitmask is empty []
        return not bool(self.bitmask)

    def is_transparent_px(self, char):
        return char == self.TRANSPARENT_PX

    def is_brush_px(self, char):
        return char == self.BRUSH_PX

    def is_center_px(self, char):
        return char == self.CENTER_PX

    def make_bitmask(self):
        bm = [[1 for _ in range(self.width)] for _ in range(self.height)]
        return bm

    def __repr__(self):
        return f"{self.__class__.__name__} W:{self.width} H:{self.height}"

    def style_bitmask(self, c=CENTER_PX, b=BRUSH_PX, t=TRANSPARENT_PX):
        bitmask = self.bitmask[:]
        # Style brush and transparent bits
        for x in range(self.width):
            for y in range(self.height):
                if self.bitmask[y][x] == 1:
                    bitmask[y][x] = b
                else:
                    bitmask[y][x] = t
        # Set center bit
        if not self.disabled:
            bitmask[int(self.height/2)][int(self.width/2)] = c
        return bitmask

    def render(self):
        sprite = ""
        for line in self.sprite:
            sprite += "".join(line) + "\n"
        return sprite

class CircularBrush(RectangularBrush):
    TYPE = "circular"

    def __init__(self, radius=0):
        # 0 is a point brush, -1 disables the brush
        self.set_radius(radius)

    def set_radius(self, radius):
        if radius >= -1:
            self.radius = radius
            self.set_dimensions(radius,radius)
        return self.radius

    def make_bitmask(self):
        aspect_ratio = 1
        bm = []
        for y in range(-self.radius, self.radius + 1):
            row = []
            for x in range(-self.radius * aspect_ratio, self.radius * aspect_ratio + 1, aspect_ratio):
                # Calculate if the current (x, y) is inside the circle
                if x ** 2 / aspect_ratio ** 2 + y ** 2 <= self.radius ** 2:
                    row.append(1)  # Inside the circle
                else:
                    row.append(0)  # Outside the circle
            bm.append(row)
        return bm

if __name__ == "__main__":
    brush = CircularBrush()
    for r in range(-1,10):
        brush.set_radius(r)
        print(brush)
        print(brush.render())

    """for x in range(-1, 3):
        for y in range(-1, 3):
            brush.set_dimensions(x,y)
            print(brush)
            print(brush.render())"""