import sys

class GameState:

   render_chars = {
             "-1": "X",
              "0": " ",
              "1": "O",
              "2": "+",
             "10": "#",
             "12": "0",
             "20": "_",
             "22": "-",
        }


   def __init__(self, g):
      self.size=g.size 
      self.width=g.size
      self.height=g.size
      self.board=g.board #[x,y,type]
      self.pieces=g.pieces #[x,y,type]
      self.time=0
      self.done=0
      self.quiet=False

   def isLegalMove(self,pieceno,x2,y2):
      try:

         if x2 < 0 or y2 < 0 or x2 >= self.width or y2 > self.height: return -2000
         
         piece = self.pieces[pieceno]
         x1=piece[0]
         y1=piece[1]
         if x1<0: return -2 #piece was captured
         if x1 != x2 and y1 != y2: return -3000 #must move in straight line
         if x1 == x2 and y1 == y2: return -4000 #no move

         piecetype = piece[2]
         if (piecetype == -1 and self.time%2 == 0) or (piecetype != -1 and self.time%2 == 1): return -5000 #wrong player

         for item in self.board:
            if item[0] == x2 and item[1] == y2 and item[2] > 0:
                if piecetype != 2: return -6000 #forbidden space
         for apiece in self.pieces:
            if y1==y2 and y1 == apiece[1] and ((x1 < apiece[0] and x2 >= apiece[0]) or (x1 > apiece[0] and x2 <= apiece[0])): return -7000 #interposing piece
            if x1==x2 and x1 == apiece[0] and ((y1 < apiece[1] and y2 >= apiece[1]) or (y1 > apiece[1] and y2 <= apiece[1])): return -7000 #interposing piece

         return 0 # legal move
      except Exception as ex:
         print("error in islegalmove ",ex,pieceno,x2,y2)
         raise

   
   def getCaptures(self,pieceno,x2,y2):
       #Assumes was already checked for legal move
       captures=[]
       piece=self.pieces[pieceno]
       piecetype = piece[2]
       for apiece in self.pieces:
          if piecetype*apiece[2] < 0:
             d1 = apiece[0]-x2 
             d2 = apiece[1]-y2
             if (abs(d1)==1 and d2==0) or (abs(d2)==1 and d1==0): 
                 for bpiece in self.pieces:
                    if piecetype*bpiece[2] > 0 and not(piece[0]==bpiece[0] and piece[1]==bpiece[1]):
                       e1 = bpiece[0]-apiece[0]
                       e2 = bpiece[1]-apiece[1]
                       if d1==e1 and d2==e2:
                          captures.extend([apiece])
       return captures

   # returns code for invalid mode (<0) or number of pieces captured
   def moveByPieceNo(self,pieceno,x2,y2):
      
      legal = self.isLegalMove(pieceno,x2,y2)
      if legal != 0: return legal

      self.time = self.time + 1

      piece=self.pieces[pieceno]
      piece[0]=x2
      piece[1]=y2
      caps = self.getCaptures(pieceno,x2,y2)
      if not self.quiet: print("Captures = ",caps)
      for c in caps:
          c[0]=-99

      self.done = self.getWinLose()
      
      return len(caps)
        


   def getWinLose(self):
       if self.time > 1000: return -1
       # time counter has advanced after move to the next player's turn
       player = 1 if self.time%2==0 else -1
       nomoves = len(self.getValidMoves(player))==0
       for apiece in self.pieces:
           if apiece[2]==2 and apiece[0] > -1:
               for item in self.board:
                 if item[0]==apiece[0] and item[1]==apiece[1] and item[2]==1:
                     return 1 #white won
               return -player if nomoves else 0  # either no winner yet, or next player lost due to no moves available
       return -1  #white lost
   
   def getPieceNo(self,x,y):
       for pieceno in range(len(self.pieces)):
           piece=self.pieces[pieceno]
           if piece[0]==x and piece[1]==y: return pieceno
       return -1    
   
   def move(self,x1,y1,x2,y2):
       pieceno = self.getPieceNo(x1,y1)
       #print("Pieceno =",pieceno)
       if not self.quiet: print("Move:",x1,y1,x2,y2)
       return self.moveByPieceNo(pieceno,x2,y2)
   
   def getValidMoves(self,player):
       moves=[]
       for pieceno in range(len(self.pieces)):
           piece=self.pieces[pieceno]
           if piece[2]*player > 0:
              for x in range(0,self.width):
                  if self.isLegalMove(pieceno,x,piece[1])>=0:moves.extend([[piece[0],piece[1],x,piece[1]]])
              for y in range(0,self.height):
                  if self.isLegalMove(pieceno,piece[0],y)>=0:moves.extend([[piece[0],piece[1],piece[0],y]])
       return moves

   def getImage(self):
     image = [[0 for col in range(self.width)] for row in range(self.height)]
     for item in self.board:
         image[item[1]][item[0]] = item[2]*10
     for piece in self.pieces:
         if piece[0] >= 0: image[piece[1]][piece[0]] = piece[2] + image[piece[1]][piece[0]]
     return image

   def render(self):
       print("Time: ",self.time)    
       image=self.getImage()
       for i in range(len(image)-1,-1,-1):
           row=image[i]
           for col in row:
               c = self.render_chars[str(col)]
               sys.stdout.write(c)
           print(" ") 
       if (self.done!=0): print("***** Done: ",self.done)  
       print("---------------------")


