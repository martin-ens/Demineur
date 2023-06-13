from random import *
import os
os.chdir('Chemin') # CHEMIN D'ACCES AU DOSSIER GRAPHICS A MODIFIER
def prox(n,p,a,b):
    L=[]
    for i in range(3):
        l=a-1+i
        for j in range(3):
            m=b-1+j
            if 0<=l<n and 0<=m<p and (l,m)!=(a,b):
                L.append((l,m))
    return L
def generate(n,p,a,b):
    m=n*p//5
    Mines=[]
    while m>0:
        i,j=randint(0,n-1),randint(0,p-1)
        if not((i,j) in Mines or (i,j) in prox(n,p,a,b) or (i,j)==(a,b)):
            Mines.append((i,j))
            m-=1
    return Mines
def ask(m):
    if m<2:
        c=input(str(m)+' mine restante. Que faire ? ')
    else:
        c=input(str(m)+' mines restantes. Que faire ? ')
    action=(c.split(' '))[0]
    i=int(c.split(' ')[1])
    j=int(c.split(' ')[2])
    return (action,i,j)
def show(M):
    n,p=len(M),len(M[0])
    s='   '
    for k in range(p):
        if k>9:
            s+=' '+str(k)+'  '
        else:
            s+='  '+str(k)+'  '
    print(s)
    for k in range(n):
        if k>9:
            print(k,M[k])
        else:
            print(k,'',M[k])
def mine(Main,M,i,j):
    if Main[i][j]!='✘':
        if M[i][j]==-1:
            return False
        else:
            count=0
            nb=0
            isNum=False
            if Main[i][j]=='█':
                Main[i][j]='0'
            else:
                isNum=True
            for x in prox(len(M),len(M[0]),i,j):
                if M[x[0]][x[1]]==-1:
                    count+=1
            Main[i][j]=str(count)
            for x in prox(len(M),len(M[0]),i,j):
                if Main[x[0]][x[1]]=='✘':
                    nb+=1
                if Main[x[0]][x[1]]=='█' and Main[i][j]=='0':
                    mine(Main,M,x[0],x[1])
            if nb==count and isNum:
                for x in prox(len(M),len(M[0]),i,j):
                    if M[x[0]][x[1]]==-1 and Main[x[0]][x[1]]!='✘':
                        return False
                    elif Main[x[0]][x[1]]=='█':
                        mine(Main,M,x[0],x[1])
    return True
def flag(Main,i,j,m):
    if Main[i][j]=='✘':
        Main[i][j]='█'
        m+=1
    elif Main[i][j] == '█':
        Main[i][j]='✘'
        m-=1
    return m

def olddemineur(n,p):
    m=n*p//5
    M=[[0 for _ in range(p)] for _ in range(n)]
    Main=[['█' for _ in range(p)] for _ in range(n)]
    show(Main)
    print('')
    c=input(str(m)+' mines. Où commencer ? Entrer `ligne colonne`. Par la suite entrer `action ligne colonne`. ')
    i=int(c.split(' ')[0])
    j=int(c.split(' ')[1])
    Mines=generate(n,p,i,j)
    for x in Mines:
        M[x[0]][x[1]]=-1 #Marque toutes les mines de M
    bool=mine(Main,M,i,j)
    while bool and (('█' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0]) or ('✘' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0])):
        show(Main)
        action,i,j=ask(m) #Demande la case à miner
        if action=='Mine' or action == 'mine':
            bool=mine(Main,M,i,j)
        elif action=='flag' or action == 'flag':
            m=flag(Main,i,j,m)
        else:
            print('Renvoyer `action ligne colonne`, action peut être `mine` ou `flag`')
    if bool:
        show(Main)
        return 'Bravo!'
    else:
        return 'BOUM'
import pygame
from sys import exit
def demineur(n,p):
    m=n*p//5
    M=[[0 for _ in range(p)] for _ in range(n)]
    Mines=[]
    Main=[['█' for _ in range(p)] for _ in range(n)]
    bool=True
    cooldown = 0

    pygame.init()
    screen = pygame.display.set_mode((16*p,16*n))
    pygame.display.set_caption('Démineur')
    logosurf=pygame.image.load('graphics/logo.png')
    unopsurf=pygame.image.load('graphics/unopened.png')
    flagsurf=pygame.image.load('graphics/flag.png')
    sminesurf=pygame.image.load('graphics/safemine.png')
    eminesurf=pygame.image.load('graphics/emine.png')
    Numbers=[]
    for i in range(9):
        Numbers.append(pygame.image.load('graphics/ms'+str(i)+'.png'))
    pygame.display.set_icon(logosurf)
    clock = pygame.time.Clock()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type==pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]==True and bool and (('█' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0]) or ('✘' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0])):
                    x,y=pygame.mouse.get_pos()
                    if Mines == []:
                        Mines = generate(n,p,y//16,x//16)
                        for s in Mines:
                            M[s[0]][s[1]]=-1
                        bool = mine(Main,M,y//16,x//16)
                    else:
                        bool = mine(Main,M,y//16,x//16)
                elif pygame.mouse.get_pressed()[2]==True and bool and (('█' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0]) or ('✘' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0])):
                    x,y=pygame.mouse.get_pos()
                    if Mines != []:
                        m=flag(Main,y//16,x//16,m)
        if not(bool) or not(('█' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0]) or ('✘' in [Main[i][j] for i in range(n) for j in range(p) if M[i][j]==0])):
            if bool:
                for i in range(n):
                    for j in range(p):
                        if M[i][j]==-1:
                            screen.blit(sminesurf,(16*j,16*i))
                        if Main[i][j]=='█':
                            pass
                        elif Main[i][j]=='✘':
                            pass
                        else:
                            screen.blit(Numbers[int(Main[i][j])],(16*j,16*i))
            else:
                for i in range(n):
                    for j in range(p):
                        if M[i][j]==-1:
                            screen.blit(sminesurf,(16*j,16*i))
                if M[y//16][x//16]==-1:
                    screen.blit(eminesurf,(16*(x//16),16*(y//16)))
                else:
                    for autour in prox(n,p,y//16,x//16):
                        if M[autour[0]][autour[1]]==-1 and Main[autour[0]][autour[1]] != '✘':
                            screen.blit(eminesurf,(16*autour[1],16*autour[0]))
        else:
            for i in range(n):
                for j in range(p):
                    if Main[i][j]=='█':
                        screen.blit(unopsurf,(16*j,16*i))
                    elif Main[i][j]=='✘':
                        screen.blit(flagsurf,(16*j,16*i))
                    else:
                        screen.blit(Numbers[int(Main[i][j])],(16*j,16*i))
        pygame.display.update()
        clock.tick(60)













