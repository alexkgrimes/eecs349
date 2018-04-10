from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  print "Running ID3...\n"

  if len(examples) == 0:
    return Node(default)

  ''' Same classification or only trivial splits'''
  allSameClass = True
  classification = examples[0]['Class']
  for ex in examples:
    if ex['Class'] != classification:
      allSameClass = False 
      break

  isTrivial = checkTrivialSplit(examples)

  ''' return the mode Class from the examples '''
  if allSameClass or isTrivial:
    return Node(mode(examples))
  
  else:
    best = chooseAttribute(examples)

''' ----------------HELPERS--------------- '''

''' 
Check for only trivial split from examples 
'''
def checkTrivialSplit(examples):
  isTrivial = True
  toMatch = examples[0]
  for ex in examples:
    for attrib, value in ex.iteritems():
      ''' TODO : add robustness for missing attibutes '''
      if value != toMatch[attrib]:
        isTrivial = False
        break
  return isTrivial

''' 
Find the mode Class value from examples 
'''
def mode(examples):
  counts = {}
  for ex in examples:
    c = ex['Class']
    if c in counts:
      counts[c] += 1
    else:
      counts[c] = 1
  return max(counts, key=counts.get)

''' TODO : pick best attribute from examples '''
def chooseAttribute(examples):
  return examples.keys()[0]


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  print "Running prune...\n"

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  print "Running test...\n"


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  print "Running evaluate...\n"
