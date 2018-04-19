from node import Node
import math
import random

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

  # print "Running ID3...\n"

  firstLabel = examples[0].get("Class")
  allSameClass = False
  isTrivialSplit = checkTrivialSplit(examples)

  if not examples: # examples is empty
    node = Node()
    node.label = default
    return node

  if all(ex.get("Class") == firstLabel for ex in examples): # or len(examples) == 1?
    allSameClass = True

  if allSameClass or isTrivialSplit:
    node = Node()
    node.label = mode(examples)
    node.exs = examples
    return node
  else:
    best, bestValues = chooseAttribute(examples)
    t = Node()
    t.attributeName = best
    for value in bestValues.keys():
      newExamples = []
      for ex in examples:
        if ex.get(best) == value:
          newExamples.append(ex)
      subTree = ID3(newExamples,mode(examples)) # subtree <- ID3(examplesi,MODE(examples))
      subTree.exs = newExamples
      t.exs = newExamples
      t.children[value] = subTree
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
  # want the attrib with minimum informationGain
  # confusing var names.. just go with it
  bestAttrib = None 
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

'''
Calculate the information gain for a given attribute
'''
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
  for child in node.children.values():
    prune(child, examples)

  tempChildren = node.children
  tempLabel = node.label

  withoutPruning = test(node, examples)

  node.children = {}
  node.label = mode(node.exs)
  withPruning = test(node, examples)

  # if original is actually better, set node back to original
  if withPruning < withoutPruning:
    node.children = tempChildren
    node.label = tempLabel
  

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  numSuccesses = 0.0
  for ex in examples:
    c = evaluate(node, ex)
    if c == ex.get("Class"):
      numSuccesses += 1.0
  return numSuccesses / float(len(examples))

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  # if it's a leaf node
  if not node.children:
    return node.label
  else:
    attrib = node.attributeName
    key = example.get(attrib)
    if key not in node.children.keys():
      r = random.randint(0, len(node.children) - 1)
      newNode = node.children.values()[r]
    else:
      newNode = node.children[key]
    return evaluate(newNode, example) # evaluate the child
