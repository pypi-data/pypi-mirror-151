import numpy as np 
from scipy.sparse.csgraph import minimum_spanning_tree 


d=np.array([ [0, 8, 0, 3], [0, 0, 2, 5], [0, 0, 0, 6], [0, 0, 0, 0] ]) 

tree=minimum_spanning_tree(d)

print( tree.toarray() )