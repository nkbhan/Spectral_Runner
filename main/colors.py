"""
Colors.py contains colors as rgb values
"""
class Colors(object):
    black = (0, 0, 0)
    white = (255, 255, 255)
    teal = (25, 148, 126)
    yellow = (241, 196, 15)
    pink = (255, 113, 206)
    blue = (1, 205, 254)
    green = (5, 255, 161)
    purple = (185, 103, 255)
    yellow2 = (255, 251, 150)
    magenta = (255, 0, 129)
    neonBlue = (66, 198, 255)
    neonPink = (244, 34, 90)
    neonYellow = (244, 184, 12)
    neonPurple = (143, 42, 163)
    neonTeal = (13, 255, 215)

    @staticmethod
    def addAlpha(color, alpha):
        r, g, b = color
        return (r, g, b, alpha)
