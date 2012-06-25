#!/usr/bin/python

import json

file = open("learnsets.json")
raw = file.readline()
file.close()

array = json.loads(raw[1:len(raw)-2])
fakename = "RotomFrost"
print array[fakename.lower()]["learnset"].keys()

