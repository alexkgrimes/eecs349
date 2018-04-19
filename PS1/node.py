class Node:
  def __init__(self):
    self.label = None
    self.attributeName = None
    self.children = {}
    self.exs = []

  # function so you can just write print tree
  def __str__(self, level=0):
		ret = "\t"*level+"Class: "+repr(self.label) + "\t"
		ret += "attributeName: "
		ret += str(self.attributeName)
		ret += "\n"
		for attribValue, child in self.children.iteritems():
			ret += "\t"*level
			ret += "value: " 
			ret += str(attribValue)
			ret += "\n"
			ret += child.__str__(level+1)
		return ret

	