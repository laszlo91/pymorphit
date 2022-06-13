from Levenshtein import distance
import sys,os,pickle,json,re,copy, readline

            
def doublePrint(user_input):
    print()
    print(user_input)
    print()
    return user_input


def default_text(defaultext): 
    readline.set_startup_hook(lambda: readline.insert_text(defaultext))
    
    
def pick_forms(morphit, PoS, lemma):
    return {form:ftrs for form,ftrs in morphit.items() if ftrs["lemma"] == lemma and ftrs["pos"] == PoS}
    

def _long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and _is_substr(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr


def _is_substr(find, data):
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True
    

def _use_root(data):
    
    data = copy.deepcopy(data)
    
    root_toReplace = _long_substr(list(data))
    root = doublePrint(input('''La radice '%s' sarà sostituita dalla radice del nuovo lemma, e verrà così introdotta una nuova voce in Morphit. Scrivi la radice del nuovo lemma: 

-''' % root_toReplace))
    
    newlemma = {re.sub(root_toReplace, root, k):v for k,v in data.items()}
    for form, ftrs in newlemma.items():
        ftrs['lemma'] = lemma
    return newlemma
    
    
def add2morphit(data, lemma):
    
    newlemma = _use_root(data)
    
    print(json.dumps(newlemma, indent=4, sort_keys=True))
    return newlemma
    
    
def yes_dump(morphit, new_word):
   
    Y_N = doublePrint(input('''Questa voce verrà inserita in Morphit. Proseguire? Y/N 

-'''))
    if Y_N == "Y":
        morphit.update(new_word)
            
        with open('morphit.pkl', 'wb') as handle:
            pickle.dump(morphit, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
        #with open('morphit.json', "w") as jsonFile:
        #    json.dump(morphit, jsonFile)

    elif Y_N == "N":
        start_again()
    else:
        print("Only Y/N are acceptable")
        start_again()
    
    
def start_again():
    python = sys.executable
    os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    
    path_dir = os.path.dirname(os.path.abspath(__file__))
    path2morphit = os.path.join(path_dir, "morphit.pkl")


    with open(path2morphit, 'rb') as f:
        morphit = pickle.load(f)

    
    lemma = sys.argv[1]

    PoS = input(lemma +''' :: Questa parola è un ADJ, un NOUN o un VER ?

    -''')
    
    if PoS not in ['ADJ','NOUN','VER']:
        raise ValueError("Valore non accettabile.")


    a = pick_forms(morphit, PoS, lemma)

    if len(a) > 0:
        for i in a:
            print([i, a[i]])
       
        
    else:
    
        lev = {}
        for form,ftrs in morphit.items():
            if ftrs['pos'] == PoS:
                lev[ftrs['lemma']] = distance(lemma, ftrs['lemma'])
        
        five_most_similar = sorted(lev.items(), key=lambda x:x[1])[:5]
        

        for ix,it in enumerate(five_most_similar):
            ix += 1
            print(ix, it[0])
        print('\*6', 'nessuno di questi')
        chosen = doublePrint(int(input('''sono i 5 lemmi più simili presenti in Morphit. Su quale di questi vuoi calcare la nuova parola? Scegli uno fra gli indici 1,2,3,4,5 o 6 se nessuno di questi va bene.

-''')))

        if chosen in range(1,6):
            chosen = five_most_similar[chosen - 1][0]
            levensthein = pick_forms(morphit, PoS, chosen)
            print(json.dumps(levensthein, indent=4, sort_keys=True))
            new_word = add2morphit(levensthein, lemma)
            yes_dump(morphit, new_word)
                
        elif chosen == 6:
            print()
            tmp = input("""Vuoi:
1) inserire un'altra parola come calco? 
2) inserire il nuovo lemma a mano?
3) ricominciare daccapo?

-""")

            if tmp == "1":
                chosen = input("Inserisci il lemma: ")
                chosen = pick_forms(morphit, PoS, chosen)
                print(json.dumps(chosen, indent=4, sort_keys=True))
                new_word = add2morphit(chosen, lemma)
                yes_dump(morphit, new_word)
                
                
            elif tmp == "2":
                newlemma = pick_forms(morphit, PoS, five_most_similar[0][0])
                default_text(str(newlemma))
                res = input('MODIFICA LA VOCE : ')
                new_word = json.loads(res.replace("\'", "\""))
                default_text("")
                yes_dump(morphit, new_word)
            
            elif tmp == "3":
                start_again()
    
            else:
                raise ValueError("Valore non accettabile.")
  
  
        else:
            raise ValueError("Valore non accettabile.")