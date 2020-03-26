'''This is the'analyse.py' module and it provides one function called analyse.
It can tell you the average of a list that may or may not include nested
lists and other items.It will first tell you the average about nested lists.'''
def analyse(the_list):
    average=0
    lenth=0
    m=1
    for each_item in the_list:
        if isinstance(each_item,list):
            analyse(each_item)
            m=m+1
        elif isinstance(each_item,int):
            average=average+each_item
            lenth=lenth+1
        else:
            pass
    average=average/lenth
    print('average:NO.',m,'\n',average)
 
    
    
        
