# main_test.py: Testing modules and how they work together

# I was completly wrong, it's entirely possible to treat the induvidual files we have as modules
#         from filename import * 
# ^^^ above code imports all functions ^^^

# ~~~~~~~NOTE please read~~~~~~~
# apparently python runs *all* code in imported module when it reachs that particular line
# So be wary, it will call *everything* in your code, have no code in your main that will affect stuff

from path_mode import *

#path = [[1 , 2] ,[1, 4]]
path = [[1,2], [1,3], [2, 3], [3,3], [3,2], [3,4]]
path_mode(path)

