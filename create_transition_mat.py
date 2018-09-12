import markovify
import json
import re
import numpy as np

def comparestr(txtdat, modeltxt):
    inx = 0
    for line in txtdat:        
        if line == modeltxt:
            break
        else:
            inx = inx + 1
            
    if inx>=len(txtdat):
        print('no matched txt')
        inx = -1
        
    return inx
            
with open("kkma_POS_list.txt") as f:
    POS_List = f.read()
POS_List = POS_List.split()
nPOS = len(POS_List)
# Get raw text as string.
with open("POS_wiki_Text.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text,state_size=1)
model_json = text_model.chain.to_json()
modeldat = json.loads(model_json)

assmat = np.zeros((nPOS,nPOS))
with open('POS_wiki_edge_data.txt','w') as outfile:
    for item in modeldat:
        inputPOS = str(item[0])
        modelPOS = str(item[1])
    
        inputPOS = ''.join(c for c in inputPOS if c not in '[\'u\']')
        match_inx = comparestr(POS_List,inputPOS)
    
        modelPOS = ''.join(c for c in modelPOS if c not in '{}\'u\'')
        modelPOS = modelPOS.replace(',','\n')
        modelPOS = modelPOS.split('\n')
    
        if match_inx>-1:

            for tag in modelPOS:
                assdat = tag.split(':')
                assPOS = assdat[0]
                assPOS = assPOS.replace(' ','')
                assVal = int(assdat[1])

                match_assinx = comparestr(POS_List,assPOS)
                #print('[%d,%d]%s %d' % (match_inx,match_assinx, assPOS, assVal))
                outfile.write('%s (pp) %s = %d\n' % (inputPOS,assPOS,assVal))  
                  
                if match_assinx>-1:
                    position = int(nPOS*match_inx + match_assinx)
                    np.put(assmat,position,assVal)
                    #print(assmat[match_inx,match_assinx])
                #else:
                    #print('%s: found no match' % inputPOS)   
             
# print(assmat.shape)
# np.savetxt('assmat.txt',assmat,'%d')
