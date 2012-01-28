#!/usr/bin/python

from numpy import random
import string
import sys
from lookup import *

def statFormula(base,lv,nat,iv,ev):
	if nat == -1: #for HP
		return (iv+2*base+ev/4+100)*lv/100+10
	else:
		return ((iv+2*base+ev/4)*lv/100+5)*nat/10

#read in learnsets
file = open("learnsets.txt")
raw = file.readline()
file.close()

movepool = []

start = 28
x=0
while True:
	i=string.find(raw,':{"learnset"',start,len(raw))
	if i==-1:
		break
	n=string.find(raw,':{"learnset"',i+1,len(raw))
	if n==-1:
		n=len(raw)
	moves=[raw[start:i-1]]
	#print name
	s=i+13
	while True:
		j=string.find(raw,':',s,n)
		if j==-1:
			break
		moves.append(raw[string.rfind(raw,'"',0,j-2)+1:j-1])
		s=j+1
	#print moves
	movepool.append(moves)
	start=string.find(raw,'}}',i,len(raw))+4

#fix Shedinja movepool
movepool[291][0]='Shedinja'
for move in movepool[663][1:len(movepool[663])]:
	if move not in movepool[291]:
		movepool[291].append(move)
del movepool[663]

#fix various entries
del movepool[554][14]
del movepool[555][15]
del movepool[556][16]
del movepool[75][17]
del movepool[234][535]

#for i in range(len(movepool)):
#	for j in range(len(movepool[i])):
#		if movepool[i][j] == '],"':
#			print i,j
#sys.exit()

#read in level balance
file = open("level_balance.txt")
raw = file.readlines()
file.close()
levelbalance=[]
for line in raw:
	levelbalance.append([line[0:len(line)-4],int(line[len(line)-3:len(line)-1])])

#read in abilities
file = open("poke_ability1_5G.txt")
raw = file.readlines()
file.close()
abilities=[]
for line in raw:
	space=string.find(line,' ')
	abilities.append([line[0:space],int(line[space+1:len(line)-1])])
file = open("poke_ability2_5G.txt")
raw = file.readlines()
file.close()
for i in range(len(raw)):
	line=raw[i]
	space=string.find(line,' ')
	abilities[i].append(int(line[space+1:len(line)-1]))
file = open("poke_ability3_5G.txt")
raw = file.readlines()
file.close()
for i in range(len(raw)):
	line=raw[i]
	space=string.find(line,' ')
	abilities[i].append(int(line[space+1:len(line)-1]))

#read in PP
file = open("pp.txt")
raw=file.readlines()
file.close()
pp=[]
for line in raw:
	pp.append(int(line[0:len(line)-1])*8/5)

inv_attacks = dict((v,k) for k, v in attacks.iteritems())

#select six pokemon at random (no repeats!)
team = []
for i in range(6):
	while True:
		x=random.randint(1,650)
		if x not in team:
			break
	team.append(x)
count=0
for poke in team:
	#print species[poke]
	count = count+1
	#choose forme at random
	if poke == 201: #unown
		forme=random.randint(0,28)
	elif poke in [412,413]: #burmy/wormadam
		forme=random.randint(0,3)
	elif poke in [422,423,492,550]: #shellos/gastrodon/shaymin/basculin
		forme=random.randint(0,2)
	elif poke in [386,585,586]: #deoxys/deeling/sawsbuck
		forme=random.randint(0,4)
	elif poke == 479: #rotom
		forme=random.randint(0,6)
	else:
		forme = 0;	

	if poke in [201,412,413,422,423,386,585,586,479]:
		fakeforme=0
	else:
		fakeforme=forme
		
	for i in range(len(levelbalance)):
		if (levelbalance[i][0] == str(poke)+":"+str(fakeforme)):
			level = levelbalance[i][1]
			break
	#set EXP--needed for level
	exp = lvlexp[level][pokestats[poke][0]]

	#choose gender at random
	if species[poke] in ['Arceus','Articuno','Azelf','Baltoy','Beldum','Bronzong','Bronzor','Celebi','Claydol','Cobalion','Cryogonal','Darkrai','Deoxys','Dialga','Ditto','Electrode','Entei','Genesect','Giratina','Golett','Golurk','Groudon','Ho-Oh','Jirachi','Keldeo','Klang','Klink','Kinklang','Kyogre','Kyurem','Lugia','Lunatone','Magnemite','Magneton','Magnezone','Manaphy','Meloteeta','Mespirit','Metagross','Metang','Mew','Mewtwo','Moltres','Palkia','Phione','Poryon','Porygon-Z','Porygon2','Raikou','Rayquaza','Regice','Regigigas','Regirock','Registeel','Reshiram','Rotom','Shaymin','Shedinja','Solrock','Starmie','Staryu','Suicune','Terrakion','Unown','Uxie','Victini','Virizion','Voltorb','Zapdos','Zekrom']:
		gender = 0
	elif species[poke] in ['Braviary','Gallade','Hitmonchan','Hitmonlee','Hitmontop','Landorus','Latios','Mothim','Nidoking','Nidoran (M)','Nidorino','Rufflet','Sawk','Tauros','Throh','Thundurus','Tornadus','Tyrogue','Volbeat']:
		gender = 1
	elif species[poke] in ['Blissey','Chansey','Cresselia','Froslass','Happiny','Illumise','Jynx','Kangaskhan','Latias','Lilligant','Mandibuzz','Miltank','Nidoqueen','Nidoran (F)','Nidorina','Petilil','Smoochum','Vespiquen','Vullaby','Wormadam']:
		gender = 2
	else:
		gender = random.randint(1,3)

	#choose ability at random (include DW)
	#find line in abilities array
	for i in range(len(abilities)):
		if (abilities[i][0] == str(poke)+":"+str(fakeforme)):
			ab = abilities[i]
			break
	while True:
		ability = ab[random.randint(1,3)]
		if ability != 0:
			break

	#choose nature at random
	nature = random.randint(0,25)
	
	#choose item at random
	item = items.keys()[random.randint(0,len(items))]

	#change forme for Arceus/Giratina, if you need to
	if poke == 487 and item == 0x0070:
		forme=1
	if poke == 493 and item in range(0x012A,0x013A):
		forme = [9,10,12,11,14,1,3,4,2,13,6,5,7,15,16,8][item-0x012A]
	

	#choose IVs at random
	IVs = []
	for i in range(6):
		IVs.append(random.randint(0,32))

	#choose EVs at random
	EVs=[0]*6
	EVpool = 510
	while EVpool > 0:
		x=random.randint(0,6)
		y=random.randint(0,min(EVpool,255-EVs[x])+1)
		EVs[x]=EVs[x]+y
		EVpool=EVpool-y

	#calculate stats--special cases are Rotom, Giratina, Shaymin, Deoxys, Wormadam
	if species[poke] not in ['Rotom','Giratina','Shaymin','Deoxys','Wormadam'] or forme == 0:
		fakepoke=poke
	else:
		if species[poke] == 'Rotom':
			fakepoke=1001
		elif species[poke] == 'Giraina':
			fakepoke=1002
		elif species[poke] == 'Shaymin':
			fakepoke=1003
		elif species[poke] == 'Deoxys':
			fakepoke=1003+forme
		elif species[poke] == 'Wormadam':
			fakepoke=1006+forme
			

	stats=[0]*6
	if species[poke]=='Shedinja':
		stats[0]=1
	else:
		stats[0]=statFormula(pokestats[fakepoke][1],level,-1,IVs[0],EVs[0])
	stats[1]=statFormula(pokestats[fakepoke][2],level,nmod[nature][1-1],IVs[1],EVs[1])
	stats[2]=statFormula(pokestats[fakepoke][3],level,nmod[nature][2-1],IVs[2],EVs[2])
	stats[3]=statFormula(pokestats[fakepoke][6],level,nmod[nature][3-1],IVs[3],EVs[3])
	stats[4]=statFormula(pokestats[fakepoke][4],level,nmod[nature][4-1],IVs[4],EVs[4])
	stats[5]=statFormula(pokestats[fakepoke][5],level,nmod[nature][5-1],IVs[5],EVs[5])
	
	#choose happiness at random
	happiness = random.randint(0,256)

	#choose four moves at random from movepool--don't worry about illegal combos
	if species[poke] == 'Rotom':
		if forme == 1:
			fakename = 'Rotom-H'
		elif forme == 2:
			fakename = 'Rotom-W'
		elif forme == 3:
			fakename = 'Rotom-F'
		elif forme == 4:
			fakename = 'Rotom-S'
		elif forme == 5:
			fakename = 'Rotom-C'
		else:
			fakename = species[poke]
	elif species[poke] == 'Wormadam':
		if forme == 1:
			fakename = 'Wormadam-G'
		if forme == 2:
			fakename = 'Wormadam-S'
		else:
			fakename = species[poke]
	elif species[poke] == 'Nidoran (M)':
		fakename = 'Nidoran-M'
	elif species[poke] == 'Nidoran (F)':
		fakename = 'Nidoran-F'
	elif species[poke] == 'Mime Jr.':
		fakename = 'MimeJr.'
	elif species[poke] == 'Mr. Mime':
		fakename = 'Mr.Mime'
	else:
		fakename = species[poke]

	found=False
	for i in range(len(movepool)):
		if (movepool[i][0] == fakename):
			found = True
			if len(movepool[i])<5:
				moves = movepool[i][1:len(movepool[i])]
			else:
				moves = []
				for j in range(4):
					while True:
						x=random.randint(1,len(movepool[i]))
						if movepool[i][x] not in moves:
							break
					moves.append(movepool[i][x])
			break

	for i in range(len(moves)):
		moves[i] = inv_attacks[moves[i]]

	#load template sav file
	pkm = open("template.pkm","rb").read()
	p = array('B')
    	p.fromstring(pkm)

	#modify the values listed above

	#species
	p[0x08]=poke%256
	p[0x09]=poke/256	

	#gender & forme
	p[0x40]=[0x00,0x08,0x10,0x18,0x20,0x28,0x30,0x38,0x40,0x48,0x50,0x58,0x60,0x68,0x70,0x78,0x80,0x99,0x90,0x98,0xA0,0xA8,0xB0,0xB8,0xC0,0xC8,0xD0,0xD8][forme]
	if gender == 0:
		p[0x40]=p[0x40]+4
	elif gender == 2:
		p[0x40]=p[0x40]+2
	#gender must also be set in the PID
	if gender == 1:
		p[0x00]=255
	#disable shiny
	p[0x01]=1	

	#level & exp
	p[0x8c]=level
	e=exp
	for i in range(16,19):
		p[i]=e%256
		e=e/256

	#ability
	p[0x15] = ability

	#nature
	p[0x41] = nature

	#item
	p[0x0a]=item%256
	p[0x0b]=item/256

	#IVs
	ivcomb=0
	for i in range(0,6):
		ivcomb = ivcomb + (IVs[i] << 5*i)
	for i in range(56,60):
		p[i]=ivcomb%256
		ivcomb=ivcomb/256

	#EVs
	for i in range(0,6):
		p[24+i]=EVs[i]

	#stats
	for i in range(0,6):
		p[144+2*i]=stats[i]%256
		p[145+2*i]=stats[i]/256
	p[142]=p[144]
	p[143]=p[145]

	#happiness
	p[0x14] = happiness

	#moves
	for i in range(len(moves)):
		p[40+2*i]=moves[i]%256
		p[41+2*i]=moves[i]/256

	#pp
	for i in range(len(moves)):
		p[48+i]=pp[moves[i]]

	#nickname
	for i in range(len(species[poke])):
		p[72+2*i]=ord(species[poke][i])
	p[72+2*i+2] = p[72+2*i+3] = p[92] = p[93] = ord('\xff')



	

	outfile=open("poke"+str(count)+".pkm",'w')
	p.tofile(outfile)
	outfile.close()
	

	#write .pkm file
	#print species[poke],forme,level,exp,gender,abilityLU[ability],items[item],IVs,EVs,happiness,[attacks[moves[i]] for i in range(len(moves))]