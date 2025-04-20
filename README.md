# scrabble

Find Scrabble letter distributions for a corpus

##  Library
```python
from elbbarcs import Estimator

e = Estimator()				# Create a new Estimator object
s = e.estimate('english.txt')		# Estimate the scores for the corpus
e.table(s) 				# Print out a table
```

```python
from elbbarcs import Estimator

e = Estimator(digraphs="ch c'h zh")	# Create a new Estimator object
s = e.estimate('brezhoneg.txt')		# Estimate the scores for the corpus
e.table(s) 				# Print out a table
```

The constructor takes the following arguments:
* `digraphs`: A string containing the space-separated digraphs in the language
* `tiles`: The number of tiles
* `buckets`: The number of buckets 

## Command line program

The library functionality is also exposed via the `elbbarcs` command-line utility.

```
$ elbbarcs brezhoneg.txt --digraph "ch zh c'h"
              ×1            ×2   ×3      ×4   ×5   ×6      ×7   ×12   ×14
0                      [blank]                                           
1                                              I    T   N O R     A     E
2                            G    S   D L U                              
3              H   B K M P V Z                                           
4   C'H W ZH Ñ Ù                                                         
5              F                                                         
6         C CH J                                                         
7              Y                                                         
9              É                            
```

This table indicates that for Breton, there should be 2 tiles for `K`, which will have a score of `3`.
