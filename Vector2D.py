class Vector2D:
    def __init__(self, xx, yy):
        self.x=xx
        self.y=yy

    def __add__(self, o):
        return Vector2D(self.x+o.x, self.y+o.y)
    
    def __sub__(self, o):
        return Vector2D(self.x-o.x, self.y-o.y)

    def imprimeVector2D(self):
        print("x=",self.x,' y=',self.y)
    

    