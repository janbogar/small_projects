"""
This is a simple tool for exploration of json files and visualisation of their structure.

Intended use:

 1. Load json file with load_json
 2. Use any of the other functions on the result to make sense of it
 
It's implemented with recursion, so don't use it on json structures deeper than the maximal recursion depth.

I reccomend to use pprint to print any results.
"""

import json

def load_json(path):
    """Loads and parses json file from the path.
Returns python representation of the file consisting of nested dictionaries and lists."""
    return json.load(open(path))


def find_key(jd, key, previous=[]):
    """Looks for a key in the dictionaries of the json tree.
Returns list of tuples (path,jd[path[0]][path[1]]...[key])."""
    result=[]
    if type(jd)==dict:
        for i in jd.keys():
            if i==key:
                result.append((previous+[i],jd[i]))
            else:
                result+=find_key(jd[i],key,previous+[i])
    if type(jd)==list:
        for n,item in enumerate(jd):
            result+=find_key(item,key,previous+[n])
    return result


def find_value(jd, value, previous=[]):
    """Looks for a value in the json tree.
Returns list of tuples (path,value)."""
    result=[]
    if jd==value:
        result.append((previous,jd))
    elif type(jd)==dict:
        for i in jd.keys():
            if value==jd[i]:
                result.append((previous+[i],value))
            else:
                result+=find_value(jd[i],value,previous+[i])
    elif type(jd)==list:
        for n,item in enumerate(jd):
            result+=find_value(item,value,previous+[n])

    return result


def find_level(jd, level, previous=[]):
    """Returns list of paths to a given level of the json tree."""
    result=[]
    if len(previous)==level:
        if type(jd)==dict:
            result+=[previous+[i] for i in jd.keys()]
        if type(jd)==list:
            result+=[previous+[i] for i in range(len(jd))]
            
    elif type(jd)==dict:
        for i in jd.keys():
                result+=find_level(jd[i],level,previous+[i])
                
    elif type(jd)==list:
        for n,item in enumerate(jd):
            result+=find_level(item,level,previous+[n])
            
    return result


def walk_path(jd,path):
    """Walks the path trough the json tree."""
    for i in path:
        jd=jd[i]
    return jd

def get_paths(jd,previous=()):
    """Gets all possible unique paths trough the json tree.
Returns them as a set of tuples, with list indices replaced by 'list' type"""
    result=set()

    if type(jd)==dict:
        for i in jd.keys():
            result=result.union(get_paths(jd[i],previous+(i,)))
    elif type(jd)==list:
        for n,item in enumerate(jd):
            result=result.union(get_paths(item,previous+(list,)))
    else:
        result.add(previous)

    return result

def get_structure(jd):
    """Gets structure of the document. This structure is the original json tree with two changes:
1.) All values are replaced with their python type (Str, Float, None,...)
2.) In any list, only unique elements are kept

"""
    if type(jd)==dict:
        result={}
        for i in jd.keys():
            result[i]=get_structure(jd[i])
            
    elif type(jd)==list:
        result=[]
        for n,item in enumerate(jd):
            res_item=get_structure(item)
            if not res_item in result:
                result.append(res_item)
    else:
        result=type(jd)
        
    return result

