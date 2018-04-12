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

  # print "Examples: ", examples

  firstLabel = examples[0].get("Class")
  allSameClass = False
  isTrivialSplit = checkTrivialSplit(examples)

  if not examples: # examples is empty
    return Node(default)

  if all(ex.get("Class") == firstLabel for ex in examples):
    allSameClass = True

  if allSameClass or isTrivialSplit:
    return Node(mode(examples))
  else:
    best, bestValues = chooseAttribute(examples)
    print "Attrib to split on: ", best
    print "Best values: ", bestValues
    t = Node(None)
    t.attribute = best
    newExamples = []
    for value in bestValues.keys():
      for ex in examples:
        if ex[best] == value:
          newExamples.append(ex)
      subtree = ID3(newExamples,mode(examples))
      t.children[best] = Node(None) # FIX THIS
    print "tree: ", t
    return t

''' ----------------HELPERS--------------- '''

''' 
Check for only trivial split from examples 
'''
def checkTrivialSplit(examples):
  isTrivial = True
  toMatch = examples[0]
  for ex in examples:
    for attrib, value in ex.iteritems():
      ''' TODO : add robustness for missing attributes '''
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

''' 
Find the attribute that maximizes information gain
'''
def chooseAttribute(examples):
  print "running function chooseAttribute"
  bestAttrib = None # want the attrib with minimum informationGain
  bestIG = float('inf')
  bestValues = None
  for attrib in examples[0].keys():
    if attrib == "Class":
      continue
    currIG, values = infoGain(examples,attrib)
    if currIG < bestIG:
      bestIG = currIG
      bestAttrib = attrib
      bestValues = values
  return bestAttrib, bestValues

def infoGain(examples, attribute):
  frequencies = {} # value -> class -> count
  totals = {} # value -> total count
  numExamples = len(examples)
  ig = [] # add all the values to sum to this array then use numpy to do summation
  for ex in examples:
    val = ex.get(attribute) # yes, no, ?
    currClass = ex.get("Class")
    if val in frequencies:
      totals[val] += 1
      if currClass in frequencies[val]:
        frequencies[val][currClass] += 1
      else:
        frequencies[val][currClass] = 1
    else:
      totals[val] = 1
      frequencies[val] = {currClass:1}

  for v in frequencies:
    probVal = totals[v]/numExamples
    e = []
    for c in frequencies[v]: # for each class
      prob = float(frequencies[v][c])/totals[v]
      e.append(prob*math.log(prob,2))
    entropy = -sum(e)
    ig.append(probVal*entropy)

  informationGain = sum(ig)
  return informationGain, totals

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

