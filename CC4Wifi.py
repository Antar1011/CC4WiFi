#!/usr/bin/python

import random
import string
import sys
import json
from lookup import *

if len(sys.argv) == 1:
	folder=''
else:
	folder=sys.argv[1]

def statFormula(base,lv,nat,iv,ev):
	if nat == -1: #for HP
		return (iv+2*base+ev/4+100)*lv/100+10
	else:
		return ((iv+2*base+ev/4)*lv/100+5)*nat/10

#read in learnsets
file = open("learnsets.json")
raw = file.readline()
file.close()

movepool = json.loads(raw)

#read in level balance
file = open("level_balance.txt")
raw = file.readlines()
file.close()
levelbalance=[]
for line in raw:
	space=string.find(line,' ')
	levelbalance.append([line[0:space],int(line[space+1:len(line)-1])])

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
ab=0
for line in raw:
	space=string.find(line,' ')
	for i in range(len(abilities)):
		if line[0:space] == abilities[i][0]:
			ab = int(line[space+1:len(line)-1])
			if ab != 0:	
				abilities[i].append(ab)
			break
file = open("poke_ability3_5G.txt")
raw = file.readlines()
file.close()
ab=0
for line in raw:
	space=string.find(line,' ')
	for i in range(len(abilities)):
		if line[0:space] == abilities[i][0]:
			ab = int(line[space+1:len(line)-1])
			if ab != 0:	
				abilities[i].append(ab)
			break

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
		x=random.randint(1,649)
		if x not in team:
			break
	team.append(x)

count=0
for poke in team:
	#print species[poke]
	count = count+1
	#choose forme at random
	if poke == 201: #unown
		forme=random.randint(0,27)
	elif poke in [412,413]: #burmy/wormadam
		forme=random.randint(0,2)
	elif poke in [422,423,492,550]: #shellos/gastrodon/shaymin/basculin
		forme=random.randint(0,1)
	elif poke in [386,585,586]: #deoxys/deerling/sawsbuck
		forme=random.randint(0,3)
	elif poke == 479: #rotom
		forme=random.randint(0,5)
	elif poke in [641,642,645]: #tornadus/thundurus/landorus
		forme=random.randint(0,1)
	elif poke == 646: #kyurem
		forme=random.randint(0,2)
	else:
		forme = 0;	

	if poke in [201,412,413,422,423,386,585,586,479,647]: #formes with no stat diff
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
		gender = random.randint(1,2)

	#choose ability at random (include DW)
	#find line in abilities array
	for i in range(len(abilities)):
		if (abilities[i][0] == str(poke)+":"+str(fakeforme)):
			ab = abilities[i]
			break
	ability = ab[random.randint(1,len(ab)-1)]

	#choose nature at random
	nature = random.randint(0,24)
	
	#choose item at random
	item = items.keys()[random.randint(0,len(items)-1)]

	#change forme for Arceus/Giratina, if you need to
	if poke == 487 and item == 0x0070:
		forme=1
	if poke == 493 and item in range(0x012A,0x013A):
		forme = [9,10,12,11,14,1,3,4,2,13,6,5,7,15,16,8][item-0x012A]
	

	#choose IVs at random
	IVs = []
	for i in range(6):
		IVs.append(random.randint(0,31))

	#choose EVs at random
	EVs=[0]*6
	EVpool = 510
	while EVpool > 0:
		x=random.randint(0,5)
		y=random.randint(0,min(EVpool,255-EVs[x]))
		EVs[x]=EVs[x]+y
		EVpool=EVpool-y

	#calculate stats--special cases are Rotom, Giratina, Shaymin, Deoxys, Wormadam
	if species[poke] not in ['Rotom','Giratina','Shaymin','Deoxys','Wormadam','Landours','Tornadus','Thundurus','Kyurem'] or forme == 0:
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
		elif species[poke] == 'Tornadus':
			fakepoke=1009
		elif species[poke] == 'Thundurus':
			fakepoke=1010
		elif species[poke] == 'Kyruem':
			fakepoke=1010+forme
		elif species[poke] == 'Landorus':
			fakepoke=1013
			

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
	happiness = random.randint(0,255)

	#choose four moves at random from movepool--don't worry about illegal combos
	if species[poke] == 'Rotom':
		if forme == 1:
			fakename = 'Rotomheat'
		elif forme == 2:
			fakename = 'Rotomwash'
		elif forme == 3:
			fakename = 'Rotomfrost'
		elif forme == 4:
			fakename = 'Rotomfan'
		elif forme == 5:
			fakename = 'Rotommow'
		else:
			fakename = species[poke]
	elif species[poke] == 'Kyurem':
		if forme == 1:
			fakename = 'Kyuremwhite'
		elif forme == 2:
			fakename = 'Kyuremblack'
		else:
			fakename = species[poke]	
	elif species[poke] == 'Wormadam':
		if forme == 1:
			fakename = 'Wormadamtrash'
		if forme == 2:
			fakename = 'Wormadamsandy'
		else:
			fakename = species[poke]
	elif species[poke] == 'Mime Jr.':
		fakename = 'Mimejr'
	elif species[poke] == 'Mr. Mime':
		fakename = 'MrMime'
	elif species[poke] == "Farfetch'd":
		fakename = 'Farfetchd'
	else:
		fakename = species[poke]
	if fakename == 'Smeargle':
		pool = attacks.values()
	else:
		pool = movepool[fakename.lower()]["learnset"].keys()
	if len(pool)<5:
		moves = pool
	else:
		while True:
			moves = []
			for j in range(4):
				while True:
					x=random.randint(1,len(pool)-1)
					if pool[x] not in moves:
						break
				moves.append(pool[x])
			#at least one move must be "damaging"
			if moves[0] in damaging.values() or moves[1] in damaging.values() or moves[2] in damaging.values() or moves[3] in damaging.values():
				break

	#change keldeo's forme if you need to
	if (species[poke]=="Keldeo") and ("secretsword" in moves):
		forme = 1

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

	#nickname=name
	for i in range(len(species[poke])):
		p[72+2*i]=ord(species[poke][i])
	p[72+2*i+2] = p[72+2*i+3] = p[92] = p[93] = ord('\xff')

	#checksum
	checksum=0
	for i in range(8,137,2):
		checksum = (checksum+p[i]+p[i+1]*256)%65536
	p[0x06]=checksum%256
	p[0x07]=checksum/256

	#write .pkm file
	outfile=open(folder+"poke"+str(count)+".pkm",'wb')
	p.tofile(outfile)
	outfile.close()
	
	#print species[poke],forme,level,exp,gender,abilityLU[ability],items[item],IVs,EVs,happiness,[attacks[moves[i]] for i in range(len(moves))]
