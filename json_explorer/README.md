This is a simple tool for exploration of json files and visualisation of their structure.

Intended use:

 1. Load json file with load_json
 2. Use any of the other functions on the result to make sense of it
 
It's implemented with recursion, so don't use it on json structures deeper than the maximal recursion depth.

I reccomend to use pprint to print any results.
