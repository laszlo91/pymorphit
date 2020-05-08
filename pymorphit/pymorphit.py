import os, json, copy, re, pickle

class Morphit:
    
    
    consonants = ('b', 'c', 'd', 'f', 'g', 'l','m', 'n', 'p', 'q', 'r', 's', 't', 'v', 'z')
    vowels = ('a','e','o','u','h') + tuple(('i' + i for i in list(consonants)))
    spurious = ('gn', 'ps', 'z', 'x', 'y', 'i') + tuple(('s' + i for i in list(consonants)))
    exceptions = {
                  1: ['bello', 'quello'], 
                  2:['nessuno', 'nessun', 'nessuna', 'ciascuno', 'ciascuna', 'ciascun', 'ognun', 'ognuno', 'ognuna'],
                  3:['questo']
                  }
    exceptions_list = [i for j in [v for k,v in exceptions.items()] for i in j]
    
    
    
    verbs = ['VER', 'AUX', 'CAU', 'ASP']
    attributes = ['ADJ', 'DET-POSS', 'DET-WH', 'TALE', 'DET-INDEF']
    substantives = ['NOUN', 'PRO-PERS', 'CLI']
    parts_of_speech = verbs + attributes + substantives
    modes = ['cond', 'ger', 'impr', 'ind', 'inf', 'part', 'sub']
    genders = ['m', 'f']
    numbers = ['s', 'p']
    persons = [1, 2, 3]
    
    
    path_dir = os.path.dirname(os.path.abspath(__file__))
    path2morphit = os.path.join(path_dir, "morphit/morphit.pkl")
    with open(path2morphit, 'rb') as f:
        morphit = pickle.load(f) 
    
    
    def __init__(self, word, *args):
        
        self.word = word
        
        args = self._argument_check(args)
        a = self._pick_forms(word, args)
        
        if len(a) == 1:
            self.features = a[0]
            self._collect_attributes()
        else:
            raise ValueError(f'''The word corresponds to several forms:
            {a}
            . Please disambiguate using pos, modes, gender, number or person as arguments.''')
            
            
    def _argument_check(self, args):
        
        args = set([arg for arg in args])
        for i in args:
            if i not in self.parts_of_speech + self.modes + self.genders + self.numbers:
                raise ValueError(f'''Here the allowed arguments:
                Parts of speech: {self.parts_of_speech}
                Verbal modes: {self.modes}
                Person of the verbs: {self.persons}
                Gender: {self.genders}
                Number: {self.numbers}''')

        return args
        
        
        

    def _pick_forms(self, word, args):

        all_compatible_forms=[]
       
        for form in self.morphit:
            if word == form.split('_')[0]:
                ftrs = [v for k,v in self.morphit[form].items()]
                if args.intersection(ftrs) == args:
                    all_compatible_forms.append(self.morphit[form])
       
        return all_compatible_forms


    def _collect_attributes(self):
        
        self.lemma = self.features['lemma']
        self.pos = self.features['pos']
        self.number = self.features['number']
        
        if self.pos in ['ADJ'] + self.verbs:
            self.mode = self.features['mode']
            
        if self.pos in ['ADJ', 'NOUN', 'DET-POSS', 'DET-WH', 'TALE', 'DET-INDEF', 'PRO-PERS', 'CLI']:
            self.gender = self.features['gender']
        
        if self.pos in self.verbs and self.mode == 'part':
            self.gender = self.features['gender']
        
        if self.pos in ['PRO-PERS', 'CLI']:
            self.person = self.features['person']
        
        if self.pos in self.verbs and self.mode not in ['inf', 'ger', 'part']:
            self.person = self.features['person']
            
            
    def article(self, form='definite'):
         
        if form is 'indefinite':
            if self.gender == 'f':
                if self.number == "s":
                    if self.is_vocalic():
                        return "un'"
                    if not self.is_vocalic():
                        return "una"
        
            elif self.gender == 'm':
                if not self.is_spurious():
                    return "un"    
                elif self.is_spurious():
                    return "uno"
                    
        if form is 'definite':
        
            if self.gender == 'f':
            
                if self.number == 's':
                    return self._elision()
                elif self.number == 'p':
                    return "le"
        
            elif self.gender == 'm':
                
                if self.number == "s":
                    if not self.is_spurious():
                        return "il"    
                    elif self.is_spurious():
                        return self._elision()
            
                elif self.number == "p":
                    if not self.is_spurious():
                        return "i"
                    elif self.is_spurious():
                        return "gli"
        else:
            raise ValueError("use form='indefinite' if you want to get indefinite article. The article is 'definite' by default")
            
            
    def _elision(self):
        if self.is_vocalic():
            return "l'"
        elif not self.is_vocalic():
            if self.gender == 'f':
                return "la"
            elif self.gender == 'f':
                return "lo"
    
    
    
    def this(self):
    
        if self.number == 's':
            if self.is_vocalic():
                return "quest'"
            if not self.is_vocalic():
                if self.gender == 'm':
                    return "questo"
                elif self.gender == 'f':
                    return "questa"
                    
    
        elif self.number == 'p':
            if self.gender == 'm':
                return "questi"    
            elif self.gender == 'f':
                return "queste"
                
                
    def preposition(self, prep):
        
        prepositions = {'in':"ne", "di":"de", 'da':"da", 'a':"a", "su":"su"}
        isomorphisms = {'bello':'be', 'quello':'que'}
            
        def_art = self.article()
        
        try:
            prep = prepositions[prep]
        except KeyError:
            prep = isomorphisms[prep]
            
        if def_art in ["le", "lo", "la", "l'"]:
            return str(prep) + "l" + str(def_art)
        elif def_art in  ["i", "gli"]:
            return str(prep) + str(def_art)
        elif def_art in  ["il"]:
            return str(prep) + 'l'
        
        
    def _indefinite_compound(self, root):
        root = re.sub('uno$|una$|un$', '', root)
        art = self.article(form='indefinite')
        return root + art
        
                
    def get_plural(self):
        return self._get_new_features('number', 'p')
        
                
    def get_singular(self):
        return self._get_new_features('number', 's')


    def get_male(self):
        return self._get_new_features('gender', 'm')

    
    def get_female(self):
        return self._get_new_features('gender', 'f')

        
    def _get_new_features(self, x, value):    
        new_features = copy.deepcopy(self.features)
        new_features[x] = value
        for i in self.morphit:
            if self.morphit[i] == new_features:
                return i.split('_')[0]


    def get_related_forms(self):
        return {k:v for k,v in self.morphit.items() if v['lemma'] == self.lemma}
    
    
    def is_vocalic(self):
        if self.word.startswith(self.vowels):
            return True
        else:
            return False
            
            
    def is_spurious(self):
        if self.word.startswith(self.spurious + self.vowels):
            return True
        else:
            return False
     
     
    def agr(self, child, *args):
        '''
        concord NOUN with ADJ (et similia), VER // PRO-PERS with VER and ADJ (et similia)
        '''
        args = self._argument_check(args)
        
        child = self._pick_one(child, args)
        
        if child['lemma'] in self.exceptions_list:
            return self._exception(child['lemma'])
        
        
        if self.pos in ['PRO-PERS','NOUN']:
                
            child = copy.deepcopy(child)
            child['number'] = self.number
            
            if child['pos'] not in self.verbs or child['mode'] == 'part':  # or child['pos'] != 'CLI':
                child['gender'] = self.gender
                return self._morphologize(child)
         
            child['person'] = '3'
            if self.pos == 'PRO-PERS':
                child['person'] = self.person
            
            if child['mode'] in ["impr", 'inf']:
                child['mode'] = 'ind'
            
            return self._morphologize(child)


    def _pick_one(self, child, args):
        try:
            all_compatible_forms = [i for i in self._pick_forms(child, args) if i['pos'] not in ['NOUN', 'PRO-PERS']]
            return all_compatible_forms[0]
        except IndexError:
            raise ValueError("the word you're trying to concord is not present in the Morphit dictionary, or is a NOUN, or a non clitic PRO-PERS")
        
        
    def _morphologize(self, child):
        return [j.split('_')[0] for j in self.morphit if self.morphit[j] == child][-1]

         
    def _exception(self, child):
        
        if child in self.exceptions[1]:
            return self.preposition(child)    
            
        elif child in self.exceptions[2]:
            return self._indefinite_compound(child)
        
        elif child in self.exceptions[3]:
            return self.this()