class Image:
    def __init__(self, w=None, h=None, c=None):
        self.w = w
        self.h = h
        self.c = c

    # Getters
    def get_width(self): return self.w
    def get_height(self): return self.h
    def get_color(self): return self.c

    # Setters
    def set_width(self, w): self.w = w
    def set_height(self, h): self.h = h
    def set_color(self, c): self.c = c

    def __str__(self):
        return f"Width: {self.w}, Height: {self.h}, Color: {self.c}"


# Objects
img1 = Image()
img2 = Image(1920, 1080, "#FFFFFF")

print("Image 1:", img1)
print("Image 2:", img2)
