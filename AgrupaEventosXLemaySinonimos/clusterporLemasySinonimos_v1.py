# -*- coding: utf-8 -*-

'''
Febrero 2016.

Toma una lista de verbos y los agrupa si tienen el mismo lema o si son sinónimos, es decir, comparten el mismo synset de WordNet.
Dependencia con NTLK - WordNet (http://www.nltk.org/install.html)

Borja Navarro Colorado
Universidad de Alicante
'''

import os
import nltk
from nltk.corpus import wordnet as wn
wnl = nltk.WordNetLemmatizer()

def agrupaPorSynset(words):
	'''Agrupa verbos que comparten al menos un synset. Son, con ello, sinónimos.
	La entrada debe ser una lista de verbos flexionados (con información extra).
	La salida un diccionario lema:verbo, verbo, etc.'''

	lemas = []
	for w in words:
		word = w.split('-')[2]
		lemas.append((w, wnl.lemmatize(word, pos='v')))
	lexicon = {}
	for l in lemas:
		evento = l[0] 
		#lexicon[evento] = 
		lema = l[1]
		synsets = wn.synsets(lema)
		lexicon[lema] = (evento, synsets)
		#out[lema] = [evento]
	#print len(lemas), len(lexicon)

	out = {}
	i=0
	for e1 in lexicon.items():
		evento=e1[0]
		out[evento]=[]
		j=i
		for e2 in lexicon.items():
			while j <=len(lexicon.items())-1:
				#print i, j
				#print lexicon.items()[i][0], lexicon.items()[j][0]
				a = lexicon.items()[i][1][1]
				b = lexicon.items()[j][1][1]
				if set(a) & set(b) != set([]):
					if lexicon.items()[i][0] != lexicon.items()[j][0]:
						#out[lexicon.items()[i][0]]=lexicon.items()[j][0]
						out[evento].append(lexicon.items()[j][1][0])
						#print 'correferentes', lexicon.items()[i][0], lexicon.items()[j][0]
				#else:
				#	if lexicon.items()[i][0] not in out['NoCorreferentes']:
				#		out['NoCorreferentes'].append((lexicon.items()[i][0]))
				j+=1
		i+=1

	#print out

	return out
	

def agrupaPorLema(words):
	'''Agrupa verbos con el mismo lema. Lematiza con WodNet.
	La entrada debe ser una lista de verbos flexionados (con información extra).
	La salida un diccionario lema:verbo, verbo, etc.'''
	#words = ['3065-9-involve', '3065-9-plans', '3065-3-impact', '3065-3-released', '3065-9-involve', '3065-9-founded', '3065-9-plans']
	lemas = []
	for w in words:
		word = w.split('-')[2]
		lemas.append((w, wnl.lemmatize(word, pos='v')))
	out = {}
	for lema in lemas:
		if lema[1] not in out.keys():
			out[lema[1]] = []
			out[lema[1]].append(lema[0])
		elif lema[1] in out.keys():
			out[lema[1]].append(lema[0])
	return out

#Principal
##########

#Rutas:
corpus_path = 'data_in/corpus1/'
corpus_path_out = 'data_out/corpus1/'


for base, directorios, ficheros in os.walk(corpus_path):
	for fichero in ficheros:
		fch = corpus_path+fichero
		print 'Agrupando eventos fichero '+fichero
		f = open(fch, 'rU').read()


		entidad = f.split('\n')[0]
		eventos = f.split('\n')[1:]

		eventos_set = []
		for item in eventos:
			if item != '' and item != '\t':
				#print item
				fecha = item.split()[1]+'#'+item.split()[0]
				#fecha = item.split()[1]
				verbos = item.split()[2:]
				#eventos_set = []
				#for e in verbos:
				eventos_set.append((fecha, verbos))
				   	#eventos_set[item.split()[1]].append(e)
			
			#print eventos_set
		
		salida = []
		for fecha, verbs in eventos_set:
			#print verbs
			#1. AGRUPACIÓN POR LEMAS
			agrupacion_verbos = agrupaPorLema(verbs)
			#print agrupacion_verbos
			#2. AGRUPACIÓN POR SINÓNIMOS:
			agrupacion_verbos_sinonimos = agrupaPorSynset(verbs)
			#agrupacion_verbos.update(agrupacion_verbos2)

			#Unimos ambos diccionarios:
			for item1 in agrupacion_verbos:
				for item2 in agrupacion_verbos_sinonimos:
					if item1 == item2:
						if agrupacion_verbos_sinonimos[item2] not in agrupacion_verbos[item1]:
							agrupacion_verbos[item1]+=agrupacion_verbos_sinonimos[item2]

			#print agrupacion_verbos

			#Elimina los eventos que ya están agrupados y se han quedado sueltos. Hay que eliminarlos porque si no aparecen repetidos: en una línea sueltos, y en otra línea como correferentes a otro evento.
			for item in agrupacion_verbos.values():
				if len(item) > 1:
					for i in item:
						word = i.split('-')[2]
						lema = wnl.lemmatize(word, pos='v')
						#print word, lema
						#print lema, agrupacion_verbos[lema]
						#print agrupacion_verbos
						if lema in agrupacion_verbos.keys():
							if agrupacion_verbos[lema] == [i]:
								del agrupacion_verbos[lema]


			for l in agrupacion_verbos.values():
				#print l
				linea = fecha
				for v in l:
					linea += '\t'+v
				#linea += '\n'
				salida.append(linea)

		salida.sort()
		out = entidad+'\n'
		for item in salida:
			ID = item.split('\t')[0].split('#')[1]
			fecha_def = item.split('\t')[0].split('#')[0]
			out+=ID+'\t'+fecha_def
			resto = item.split('\t')[1:]
			for item in resto:
				out+='\t'+item
			out+='\n'
		out = out[:-1]
		#print out

		cluster = open(corpus_path_out+fichero, 'w')
		cluster.write(out)
		cluster.close()


print 'Hecho'
