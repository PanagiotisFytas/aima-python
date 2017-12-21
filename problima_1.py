from csp import *
import time

def dimiourgia_nb_orizondia(list_,i):
    q=0
    str_=''
    w=0
    while (w <len(list_)):
        if(q==1):
            str_=str_+';'
        q=0
        for j in range(w,len(list_)):
            if (list_[j]== 0 and q==0):
                str_=str_+'['+str(i)+','+str(j)+']'+':'
                q=1
                w=j
            elif (list_[j]== 0 and q==1):
                str_=str_+'['+str(i)+','+str(j)+']'+' '
        w=w+1
    if(q==1):
        str_=str_+';'
        
    return str_
        
def dimiourgia_nb_katheta(list_,i):

    q=0
    str_=''
    w=0
    while (w <len(list_)):
        if(q==1):
            str_=str_+';'
        q=0
        for j in range(w,len(list_)):
            if (list_[j]== 0 and q==0):
                str_=str_+'['+str(j)+','+str(i)+']'+':'
                q=1
                w=j
            elif (list_[j]== 0 and q==1):
                str_=str_+'['+str(j)+','+str(i)+']'+' '
        w=w+1
    if(q==1):
        str_=str_+';'
    return str_

def katheth_lista(pinakas,j):
    list_=[]
    for i in range(len(pinakas)):
        list_.append(pinakas[i][j])
        
    return list_

def dimiourgia_str(p):



    str_=''
    for i in range(len(p)):
        str_ = str_ + dimiourgia_nb_orizondia(p[i],i)

    #print str_
    print
    strr=''
    for j in range(len(p[0])):
        l=katheth_lista(p,j)
        strr = strr + dimiourgia_nb_katheta(l,j)

   # print strr
    
    str_=str_+strr
    str_=str_[:-1] #bgazoume to telefteo ; gia
                    #na doulepsei sosta h parse_neighbors.
    #print str_
    return str_

def dimiourgia_str_periorismwn(pinakas):
    my_list=[]

#---Orizondia
    q=0
    w=0
    for i in range(len(pinakas)):
        my_list.append([])
        #print my_list
        q=0
        for j in range(len(pinakas[i])):
            if ( pinakas[i][j]!=0 and pinakas[i][j]!='X' ):
                if(pinakas[i][j][1]!=0):#Orizondios periorismos
                    if(q==1):
                        w=w+1
                        my_list[i+w].append(pinakas[i][j][1])
                    else:
                        my_list[i+w].append(pinakas[i][j][1])
                    q=1
            elif(q>0 and pinakas[i][j]==0):
                my_list[i+w].append("["+str(i)+","+str(j)+"]") 
                q=q+1

#---Katheta
    q=0
    w=0
    k=len(my_list)
    for i in range(len(pinakas[0])):
        my_list.append([])
        #print my_list
        q=0
        
        for j in range(len(pinakas)):
            if ( pinakas[j][i]!=0 and pinakas[j][i]!='X' ):
                if(pinakas[j][i][0]!=0):#Katheta periorismos
                    if(q==1):
                        w=w+1
                        my_list[k+i+w].append(pinakas[j][i][0])
                    else:
                        my_list[k+i].append(pinakas[j][i][0])
                    q=1
            elif(q>0 and pinakas[j][i]==0):
                 my_list[k+i+w].append("["+str(j)+","+str(i)+"]")
                 q=q+1

    #Diagrafi olwn twn kenw listwn apo tin my_list.  
    count=0
    for i in range(len(my_list)):
        if(my_list[i]==[]):
            count=count+1

    #print count
    for i in range(count):
        my_list.remove([])
        
    #print my_list
    return my_list


class KakuroCSP(CSP):
    
    def __init__(self, dom, neighbors,periorismoi):
        if isinstance(neighbors, str):
           neighbors = parse_neighbors(neighbors)

        domains  = DefaultDict([])
        for var in neighbors.keys():
            domains [var] = dom 
        self.periorismoi=periorismoi
        self.num_conflicts=0
        CSP.__init__(self, neighbors.keys(), domains  , neighbors, self.has_constraint)

    def parse_neighbors(neighbors, vars=[]):
        """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
        regions to neighbors.  The syntax is a region name followed by a ':'
        followed by zero or more region names, followed by ';', repeated for
        each region name.  If you say 'X: Y' you don't need 'Y: X'.
        >>> parse_neighbors('X: Y Z; Y: Z')
        {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
        """
        dict = DefaultDict([])
        for var in vars:
            dict[var] = []
        specs = [spec.split(':') for spec in neighbors.split(';')]
        for (A, Aneighbors) in specs:
            A = A.strip()
            dict.setdefault(A, [])
            for B in Aneighbors.split():
                dict[A].append(B)
                dict[B].append(A)
        return dict



    def has_constraint(self,var,val,var_2,val_2,assignment,cmd):
        self.num_conflicts=0
        if (cmd==0):#Apli litourgia
            
            if(val==val_2):
                self.num_conflicts=self.num_conflicts+1 #Afxanw ta conflicts kata 1
                return False #Yparxei conflict.
            
        else:#sintheti litourgia
            
            flag = True #Den brethikan conflicts.
            #################-Elenxos gramwn kai stilwn-######################
            for i in range(len(self.neighbors[var])):
                nb=self.neighbors[var][i]
                if (nb in assignment):
                    if(assignment[nb]==val):
                        self.num_conflicts=self.num_conflicts+1 #Afxanw ta conflicts kata 1
                        flag = False

            
            ######################-Elenxos periorismwn athrismotos-#######################
            per=self.periorismoi
            
            for i in range( len(per) ):
                sum_=0
                q=0
                for j in range( 1, len(per[i]) ):
                    if (per[i][j] in assignment):
                        sum_= sum_+ assignment[per[i][j]]
                    elif ( per[i][j] == var ):
                        sum_= sum_+ val
                    else:
                        q=1
                        break
                if(q!=1 and sum_!=per[i][0]):
                    flag = False
                    self.num_conflicts=self.num_conflicts+1 #Afxanw ta conflicts kata 1
                   
            return flag 
            


    def nconflicts(self, var, val, assignment):
        
        flag=self.has_constraint(var,val,0,0,assignment,1)
        if(flag==False):#An yparxei conflict kita posa exei katagrapsei i has_constraint.
            return self.num_conflicts
        else:   #Alios epestrepse 0
            return 0

        
        #######################---MAIN---#######################################################
"""
pinakas=[['X','X',[4,0],[10,0],'X','X','X'],
         ['X',[0,4],0,0,'X',[3,0],[4,0]],
         ['X',[0,3],0,0,[11,4],0,0],
         ['X',[3,0],[4,10],0,0,0,0],
         [[0,11],0,0,0,0,[4,0],'X'],
         [[0,4],0,0,[0,4],0,0,'X'],
         ['X','X','X',[0,3],0,0,'X']]

"""
"""
pinakas=[['X','X',[9,0],[14,0],'X','X','X'],
         ['X',[0,8],0,0,'X',[10,0],[5,0]],
         ['X',[4,5],0,0,[3,12],0,0],
         ['X',0,0,0,0,0,0]]
      
"""
pinakas=[['X',[3,2],0],['X',0,[3,0]],[[0,4],0,0]]


#-------------------------------------------------------------------------------
str_= dimiourgia_str(pinakas)
#print str_
per= dimiourgia_str_periorismwn(pinakas)
#print per
"""
per=[[4, '[1,2]', '[1,3]'],
    [3, '[2,2]', '[2,3]'],
    [4, '[2,5]', '[2,6]'],
    [10, '[3,3]', '[3,4]', '[3,5]', '[3,6]'],
    [11, '[4,1]', '[4,2]', '[4,3]', '[4,4]'],
    [4, '[5,1]', '[5,2]'],
    [4, '[5,4]', '[5,5]'],
    [3, '[6,4]', '[6,5]'],
    [3, '[4,1]', '[5,1]'],
    [4, '[1,2]', '[2,2]'],
    [4, '[4,2]', '[5,2]'],
    [10, '[1,3]', '[2,3]', '[3,3]', '[4,3]'],
    [11, '[3,4]', '[4,4]', '[5,4]', '[6,4]'],
    [3, '[2,5]', '[3,5]'],
    [4, '[5,5]', '[6,5]'],
    [4, '[2,6]', '[3,6]']]
    """
"""
per=[[8, '[1,2]', '[1,3]'],
     [5, '[2,2]', '[2,3]'],
      [12, '[2,5]', '[2,6]'],
     [4, '[3,1]'],
     [9, '[1,2]', '[2,2]', '[3,2]'],
     [14, '[1,3]', '[2,3]', '[3,3]'],
     [3, '[3,4]'],
     [10, '[2,5]', '[3,5]'],
     [5, '[2,6]', '[3,6]']]
"""
p=KakuroCSP([i+1 for i in range(9)],str_,per)
#print p.vars
print
#print p.domains
print
#print p.neighbors
print p.periorismoi
#print p.constraints
print "Parakalo perimenete..."

s1=time.clock()


##############################################
#sol = backtracking_search(p)
#sol=backtracking_search(p,select_unassigned_variable=mrv)
sol=backtracking_search(p, inference=forward_checking)
#sol=backtracking_search(p,select_unassigned_variable=mrv, inference=forward_checking)
##############################################


s2=time.clock()

print "########################################################"
print "Xronos ektelesis(sec): ",s2-s1
print sol



# BT, BT + MRV, FC, FC + MRV
"""
backtracking_search(australia)
backtracking_search(australia, select_unassigned_variable=mrv) 
backtracking_search(australia, order_domain_values=lcv)
backtracking_search(australia, select_unassigned_variable=mrv, order_domain_values=lcv) 
backtracking_search(australia, inference=forward_checking)
sol2_backtracking_search(australia, inference=mac)
backtracking_search(usa, select_unassigned_variable=mrv, order_domain_values=lcv, inference=mac) 
"""





