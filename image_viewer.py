import re
import subprocess
from random import randint
from PIL import Image


def rgb_to_char(r,g,b):
    c = chr(int((r + g + b) / 3))
    return re.sub(r'[^\x20-\x7E]', '-', c)

def rgb_to_hex(r,g,b):
    c = chr(int((r + g + b) / 3))
    return c.encode('utf-8').hex()

def rgb_to_10rgb(r,g,b):
    factor = 256/10
    return f"{int(r/factor)}{int(g/factor)}{int(b/factor)}"

def rgb_to_ascii_grayscale(r,g,b):
    ascii_chars = ' .`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    # Convert RGB to grayscale using the luminance formula
    grayscale = int(0.299 * r + 0.587 * g + 0.114 * b)
    # Map the grayscale value to the range of the ASCII characters
    num_chars = len(ascii_chars)
    # Scale the grayscale value to the index range
    index = int((grayscale / 255.0) * (num_chars - 1))
    # Return the corresponding ASCII character
    return ascii_chars[index]

def rgb_to_ansi_color_ascii(r,g,b):
    """Returns a string with the ASCII char and ANSI escape codes for coloring according to the RGB value."""
    char = rgb_to_ascii_grayscale(r,g,b)
    return f'\x1b[38;2;{r};{g};{b}m{char}\x1b[0m'

class ASCIIImageViewer():
    WIDTH = 80
    HEIGHT = 40

    def __init__(self, filepath):
        self.filepath = filepath
        self.x = 0
        self.y = 0
        self._reticule_radius = -1
        self._move_factor = 1
        self.reset_buffer()

    def __repr__(self):
        return f"{self.filepath} [{self.x}, {self.y} | {self.reticule_radius}, {self.move_factor}] {self.pixel()}"

    def load_image(self):
        self.image = Image.open(self.filepath)
        self.image = self.image.convert("RGB")
        self.width, self.height = self.image.size
        self.update_buffer()

    def center(self):
        # Moves the viewer to the center of the image
        self.x = int(self.width/2)
        self.y = int(self.height/2)

    def set(self, x, y):
        # Set the coordinates
        self.x = x
        self.y = y

    def set_random(self):
        self.set(randint(0,self.width),randint(0,self.height))

    def pixel(self, x=None, y=None):
        if not x:
            x = self.x
        if not y:
            y = self.y
        return self.image.getpixel((x, y))

    def move(self, direction):
        if direction == "left":
            self.x -= self._move_factor
        elif direction == "right":
            self.x += self._move_factor
        elif direction == "up":
            self.y -= self._move_factor
        elif direction == "down":
            self.y += self._move_factor

    @property
    def viewport(self):
        # Returns a tuple (width, height) as the viewport dimensions
        return (self.WIDTH, self.HEIGHT)

    @property
    def reticule_radius(self):
        return self._reticule_radius

    @reticule_radius.setter
    def reticule_radius(self, value):
        self.reticule = None
        if isinstance(value, int) and value >= -1:
            self._reticule_radius = value
        # Make the reticule
        if self._reticule_radius >= 0:
            vp_x, vp_y = self.viewport
            self.reticule = (
                (int(vp_x / 2) - self._reticule_radius, int(vp_x / 2) + self._reticule_radius + 1),
                (int(vp_y / 2) - self._reticule_radius, int(vp_y / 2) + self._reticule_radius + 1)
            )
        return self.reticule

    @property
    def move_factor(self):
        return self._move_factor

    @move_factor.setter
    def move_factor(self, value):
        if isinstance(value, int) and value >= 1:
            self._move_factor = value

    def reset_buffer(self, default=(0,0,0)):
        # Updates the buffer with default pixel values
        self.buffer = [[default for _ in range(self.viewport[0])] for _ in range(self.viewport[1])]

    def update_buffer(self, default=(0,0,0)):
        # Updates the buffer with pixel values around self.x and self.y
        size = self.viewport
        start_x = self.x - size[0]/2
        start_y = self.y - size[1]/2
        for y in range(size[1]):
            for x in range(size[0]):
                self.buffer[y][x] = self.image.getpixel((start_x + x, start_y + y))

    def prepare_display_buffer(self, transform=rgb_to_char):
        # Copies the pixel buffer and transforms it into colored ascii chars in the display buffer
        self.display_buffer = list(self.buffer)
        size = self.viewport
        for y, line in enumerate(self.display_buffer):
            for x, pixel in enumerate(line):
                if transform:
                    self.display_buffer[y][x] = transform(*pixel)
                if self.reticule and x in range(*self.reticule[0]) and y in range(*self.reticule[1]):
                    if x == int(size[0]/2) and y == int(size[1]/2):
                        self.display_buffer[y][x] = "X"
                    else:
                        self.display_buffer[y][x] = f"\033[5m{self.display_buffer[y][x]}\033[0m"

    def print_display_buffer(self, transform=rgb_to_char):
        self.prepare_display_buffer(transform)
        # Prints out the display buffer line by line
        for line in self.display_buffer:
            print("".join(line))

if __name__ == "__main__":
    viewer = ASCIIImageViewer(filepath="data/Aventurien_Master_5125x8200.png")
    viewer.load_image()
    viewer.center()
    viewer.reticule_radius = 3
    viewer.update_buffer()
    viewer.print_display_buffer(transform=rgb_to_ansi_color_ascii)
    print(viewer)
    subprocess.run('stty sane', shell=True)