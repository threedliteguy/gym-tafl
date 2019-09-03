import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from itertools import chain
from functools import partial
import math

class FFNet(nn.Module):

    def __init__(self, input_len, save_path):
        super(FFNet, self).__init__()
        self.save_path = save_path
        self.fc1 = nn.Linear(input_len, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 64)
        self.fc5 = nn.Linear(64, 32)
        self.fc6 = nn.Linear(32, 1)
 
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = self.fc6(x)
        return x

    def save(self):
        torch.save(self.state_dict(), self.save_path)

    def load(self):
        self.load_state_dict(torch.load(self.save_path))
        self.eval()



class Trainer():

    def __init__(self, input_length, save_path):
        self.model = FFNet(input_length,save_path)
        self.model.train()
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = 0.001)

    def learn(self, x_train, y_train):
        num_epoch = 10
        for epoch in range(num_epoch):    
            self.optimizer.zero_grad()
            y_pred = self.model(x_train)
            loss = self.criterion(y_pred.squeeze(), y_train)
            if (epoch+1)%10==0: print('Epoch {}  Loss {}'.format(epoch, loss.item()))
            loss.backward()
            self.optimizer.step()
        self.model.save()

class Loader():


    def encode_cat(self,cats,i):
        r = [0.] * len(cats)
        r[cats.index(int(i))]=1.
        return r

    def encode_cats(self,cats,x):
        #print(x)
        x = list(chain.from_iterable(map(partial(self.encode_cat,cats),x)))
        #print(x)
        return x
   
   
    def load_data(self,filename):
       
       # Read file 
       f = open(filename, "r")
       data = f.read() 
       f.close()
       
       # Parse
       data = data.split('\n')
       data = list(map(lambda x: x.split("|"), data))
       
       # Shift the recorded rewards to the line that contains the action that caused it
       for i in range(len(data)-1):
           data[i][0]=data[i+1][0]
       data = data[:-1] # remove trailing final reward line which has already been copied to previous line


       # Encode
       piece_cats = [-1,0,1,2]
       action_cats = []
       board_size=int(math.sqrt(len(data[0][1].split(' '))))
       #print('board_size=',board_size)
       for i in range(board_size): action_cats.append(i)

       for i in range(len(data)):
           data[i][0]=[float(data[i][0])]      
           data[i][1]=self.encode_cats(piece_cats,data[i][1].split(' '))       
           data[i][2]=[float(data[i][2])]      
           data[i][3]=self.encode_cats(action_cats,data[i][3].split(' '))       
       y_train = [row[0][0] for row in data]
       x_train = [row[1]+row[2]+row[3] for row in data]
       return x_train,y_train


if __name__ == '__main__':
    
    loader = Loader()

    for player in [1,2]:

        trainer = None

        from pathlib import Path
        pathlist = Path("../../../output").glob('**/player_'+str(player)+'-*.txt')
        for path in pathlist:
            
            spath = str(path)
            print("Processing file: "+spath)
            x_train, y_train = loader.load_data(spath)
            input_row_count=len(x_train)
            input_row_length=len(x_train[0])
            #print('input_row_count',input_row_count)
            #print('input_row_length',input_row_length)

            x_train = torch.tensor(x_train)
            y_train = torch.tensor(y_train)

            if trainer == None: trainer = Trainer(input_row_length,"models/model_"+str(player))
            trainer.learn(x_train,y_train)
        
        trainer.model.save()

