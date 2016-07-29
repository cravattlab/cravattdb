"""Defines classes and global variables for mirage software.

mirage.py
Michael Lazear, 2016
All rights reserved
"""

import json


class Peptide(object):
    accession = ''
    sequence = ''

    def __init__(self, accession=accession, sequence=sequence, ratios=dict()):
        self.accession = accession
        self.sequence = sequence
        self.ratios = ratios

    def __contains__(self, key):
        if str(key) in self.sequence:
            return True
        if str(key) in self.accession:
            return True
        if str(key) in self.ratios:
            return True
        return False

    def addratio(self, key, value):
        self.ratios[key] = value

    def getratio(self, key):
        return self.ratios[key]

    def getallratios(self):
        return self.ratios

    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=2)

    def __len__(self):
        ''' used so we don't get a PDB object '''
        return 1


class Protein(object):
    accession = ''
    identifier = ''
    sequence = ''
    # ontology = []
    organism = ''
    mw = 0

    def __init__(self, accession=accession, identifier=identifier, sequence=sequence, organism=organism, mw=0):
        self.accession = accession
        self.identifier = identifier
        self.sequence = sequence
        self.organism = organism
        self.mw = 0

    def __contains__(self, x):
        """ Search protein for X occuring in any string field """
        if type(x) == str:
            if str(x) in self.accession:
                return True
            if str(x) in self.identifier:
                return True
            if str(x) in self.sequence:
                return True
        if type(x) == Peptide:
            return any(x == pep for pep in self.peptides)

    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=2)

    def load(self, dct):
        """Load from a JSON dictionary"""
        self.accession = dct['accession']
        self.identifier = dct['identifier']
        self.sequence = dct['sequence']
        self.mw = dct['mw']

    def __setattr__(self, name, value):
        self.__dict__[name] = value 

    def __len__(self):
        ''' used so we don't get a PDB object '''
        return 1


class ProteinDatabase(object):
    # data = []
    iter_index = 0

    @staticmethod
    def load(path):
        """ Wrapper for readJSON function, returns a ProteinDatabase object read from path"""
        return readJSON(path)

    def save(self, path):
        """ Wrapper for writeJSON function, saves the ProteinDatabase object to path"""
        writeJSON(path, self)

    def __init__(self):

        self.data = []
        self.iter_index = 0

        return

    def __add__(self, obj):
        self.data.append(obj)

    def __sub__(self, obj):
        self.data.remove(obj)

    def __iter__(self):
        return self

    def index(self, obj):
        return self.data.index(obj)

    def __getitem__(self, pos):
        """ If pos is an integer, return an array. If pos is a str, search the database """
        if type(pos) == int:
            return self.data[pos]
        if type(pos) == str:
            return self.search(pos)

    def __setitem__(self, pos, value):
        self.data[pos] = value

    def __missing__(self):
        return None

    # If there is one result, return the Protein object
    # If there is more than one result, return a ProteinDatabase object
    def search(self, key):
        """ Can search the entire data set for any keyword, returns a Protein or ProteinDatabase object of results """
        out = ProteinDatabase()
        for x in self.data:
            if key in x.accession or key in x.identifier:
                self.iter_index = 0
                return x

        if len(out) == 1:
            return out[0]
        return out

    def getSequence(self, ipi):
        for x in self.data:
            if ipi in x.accession:
                self.iter_index = 0
                return x.sequence
        return ""

    def __len__(self):
        return len(self.data)

    def __contains__(self, obj):
        """ obj can be either a Protein object or a string (accession, identifier, sequence)"""
        if self.data is None:
            raise TypeError("Not data")
        if type(obj) == Protein:
            return any(obj == x for x in self)
        if type(obj) == str:
            return any(obj in x.accession for x in self)

    # Compares two ProteinDatabase objects
    # A & B, if all of A is in B, then True
    def __and__(self, obj):
        """ Compare two ProteinDatabase Objects"""
        for x in self:
            if x not in obj:
                return False
        return True

    def __next__(self):
        if self.iter_index == len(self.data):
            self.iter_index = 0
            raise StopIteration
        s = self.data[self.iter_index]
        self.iter_index += 1
        return s

    def __repr__(self):
        # return '\n'.join(map(str, self.data))
        return "ProteinDatabase object with " + str(len(self.data)) + " proteins"


class PeptideContainer(object):
    accession = ''

    def __init__(self, accession=accession):
        self.peptides = []
        self.iter_index = 0
        self.accession = accession

    def __add__(self, obj):
        if type(obj) == Peptide:
            if obj.accession == self.accession:
                self.peptides.append(obj)
            else:
                raise ValueError("Trying to add a peptide with different accession code")
        else:
            raise TypeError("Type must be Peptide")

    def __len__(self):
        return len(self.peptides)

    def __repr__(self):
        return str(self.accession) + " containing " + str(len(self.peptides)) + " peptides"

    def __contains__(self, obj):
        """ obj can be either a Protein object or a string (accession, identifier, sequence)"""
        if self.peptides is None:
            raise TypeError("Not data")
        if type(obj) == Peptide:
            return any(obj == x for x in self)
        if type(obj) == str:
            return any(obj in x for x in self)

    # If there is one result, return the Protein object
    # If there is more than one result, return a ProteinDatabase object
    def search(self, key):
        """Search the entire data set for any keyword, returns a Protein or ProteinDatabase object of results."""
        out = PeptideContainer(accession=self.accession)
        for x in self.peptides:
            if key in x:
                out + x

        if len(out) == 1:
            return out[0]
        return out

    def __getitem__(self, pos):
        """ If pos is an integer, return an array. If pos is a str, search the database """
        if type(pos) == int:
            return self.peptides[pos]
        if type(pos) == str:
            return self.search(pos)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_index == len(self.peptides):
            self.iter_index = 0
            raise StopIteration
        s = self.peptides[self.iter_index]
        self.iter_index += 1
        return s


def out(d):
    """Output a dictionary in pretty format."""
    print(json.dumps(d, indent=2, sort_keys=True))


def writeJSON(f, data):
    """Write a mirage.ProteinDatabase object to JSON file."""
    file = open(f, 'w')
    for i in data:
        file.write(json.dumps(i.__dict__, sort_keys=True) + '\n')
    return


def readJSON(f):
    """Returns a mirage.ProteinDatabase object from JSON file"""
    file = open(f, 'r')
    db = ProteinDatabase()
    for line in file:
        new = Protein()
        json.loads(line, object_hook=new.load)
        db + new
    return db


def writeTab(f, data):
    """Writes an array to a tab-delimited file"""
    f_out = open(f, 'w')
    for item in data:
            f_out.write('\t'.join(map(str, item)) + '\n')


def readTab(f):
    """Reads a tab-delimited file to an array"""
    out = []
    file = open(f, 'r')
    for line in file:
        out.append(line.strip().split('\t'))
    return out
