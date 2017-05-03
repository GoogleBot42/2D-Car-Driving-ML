class Terrain:
    class Tile:
        def __init__(self,x,y,w,h,game):
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def __init__(self,startx,starty,tileWidth,tileHeight,length):
        self.t = []
        self.x = startx
        self.y = starty
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        for i in range(length):
            self.add()

    def add():
        self.t.append(Tile(self.x,self.y,self.tileWidth,self.tileHeight))
