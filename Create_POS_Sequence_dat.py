# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
#from konlpy.tag import Mecab
import unicodedata
import codecs

kkma = Kkma() # call kokoma POS tagger

fname = 'spk1_freedialogue_TF.txt' #merged_raw_text
with open('POS_spk1_TF.txt','w') as outfile:
	with open(fname) as infile: #,"r","utf-8"
		for line in infile:
			lines = line.decode('utf-8')

			intext = 'u' + '\'' + lines + '\''

			postag = kkma.pos(intext)
			#outfile.write(line)
			for pos in range(2,len(postag)):
				text = postag[pos][0]
				tagdat = postag[pos][1]
				dat = '%s/%s '% (text,tagdat)
				outfile.write(dat.encode("utf-8"))

			outfile.write('\n')
