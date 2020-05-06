import json
import pprint
import re
import os
    
path_dir = os.path.dirname(os.path.abspath(__file__))
path2morphit = os.path.join(path_dir, "morphit.txt")

lzta = []
for line in open(path2morphit):
    lzta.append(re.split("\s|\:|\+", line.rstrip()))

    
dik = {}


def numera(forma, n=0, dik=dik):

    forma_n = forma + "_" + str(n)
    
    if forma_n not in dik:
        return forma_n
    else:
        n += 1
        return numera(forma, n)
    

for ix,entry in enumerate(lzta):
    f = numera(entry[0])
    try:
        if entry[2] in ['ADJ']:
            
            dik[f] = {'gender':entry[-2].lower(), 'number':entry[-1], 'mode':entry[-3], "pos":entry[2], 'lemma':entry[1]}

        elif entry[2] in ['NOUN', 'DET-POSS', 'DET-WH', 'TALE', 'DET-INDEF', 'DET-DEMO']:
            
            dik[f] = {'gender':entry[-2].lower(), 'number':entry[-1].lower(), "pos":entry[2], 'lemma':entry[1]}
            
        elif entry[2] in ['VER', 'AUX', 'CAU', 'ASP']:

            if entry[3] in ["ind", "sub", "cond"]:
             
                dik[f] = {'mode':entry[3], 'time':entry[-3], 'person':entry[-2], 'number':entry[-1], "pos":entry[2], 'lemma':entry[1]}
        
            elif entry[3] in ["inf", "ger"]:
                if len(entry) == 5:
                    
                    dik[f] = {'mode':entry[3], 'time':entry[-1], "pos":entry[2], 'lemma':entry[1], 'number':'Undefined'}
                elif len(entry) == 6:
               
                    dik[f] = {'mode':entry[3], 'time':entry[-2], 'suffix':entry[-1], "pos":entry[2], 'lemma':entry[1], 'number':'Undefined'}
        
            elif entry[3] in ["part"]:
                
                dik[f] = {'mode':entry[3], 'time':entry[-3], 'gender':entry[-1].lower(), 'number':entry[-2], "pos":entry[2], 'lemma':entry[1]}
            
            elif entry[3] in ["impr"]:
                if len(entry) == 7:
                 
                    dik[f] = {'mode':entry[3], 'time':entry[-3], 'person':entry[-2], 'number':entry[-1], "pos":entry[2], 'lemma':entry[1]}
                elif len(entry) == 8:
                    
                    dik[f] = {'mode':entry[3], 'time':entry[4], 'person':entry[5], 'number':entry[6], 'suffix':entry[-1], "pos":entry[2], 'lemma':entry[1]}
                    
                    
        elif entry[2] in ['PRO-PERS']:
            
            if len(entry) == 7:
                
                dik[f] = {"pos":"CLI", 'gender':entry[-2].lower(), 'number':entry[-1].lower(), "person":entry[-3], 'lemma':entry[1]}
                
            elif len(entry) == 6:
                
                dik[f] = {"pos":"PRO-PERS", 'gender':entry[-2].lower(), 'number':entry[-1].lower(), "person":entry[-3], 'lemma':entry[1]}
            
            elif len(entry) == 5:
                
                dik[f] = {"pos":"CLI-COM", 'lemma':entry[1], 'number':'Undefined', 'gender':'Undefined', 'person': 'Undefined'}


    except IndexError as e:
        print(ix)
        raise(e)



with open(os.path.join(path_dir, 'morphit_dictionary.json'), 'w', encoding='utf8') as outfile:
    json.dump(dik, outfile, ensure_ascii=False)
