#-*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON
import time, random

# testes
NOW=time.time()
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Love> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para consultar a dbpedia"%(time.time()-NOW,))

for result in results["results"]["bindings"]:
    print(result["label"]["value"]+", "+result["label"]["xml:lang"])

PREFIX="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ops: <http://purl.org/socialparticipation/ops#>
PREFIX opa: <http://purl.org/socialparticipation/opa#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX tsioc: <http://rdfs.org/sioc/types#>
PREFIX schema: <http://schema.org/>
"""

q2="SELECT ?nome WHERE {?s rdf:type ops:Participant . ?s foaf:name ?nome .}"
NOW=time.time()
sparql3 = SPARQLWrapper("http://localhost:82/participabr/query")
#sparql3 = SPARQLWrapper("http://200.144.255.210:8082/participabr/query")
sparql3.setQuery(PREFIX+q2)
sparql3.setReturnFormat(JSON)
results3 = sparql3.query().convert()
print("%.2f segundos para puxar todos os nomes dos participantes do Participa.br"%(time.time()-NOW,))

for i in results3["results"]["bindings"][-10:]: print(u"participante: " +i["nome"]["value"])

NOW=time.time()
q="SELECT ?comentario ?titulo ?texto WHERE {?comentario dc:type tsioc:Comment. OPTIONAL {?comentario dc:title ?titulo . } OPTIONAL {?comentario schema:text ?texto .}}"
sparql3.setQuery(PREFIX+q)
sparql3.setReturnFormat(JSON)
results4 = sparql3.query().convert()
print("%.2f segundos para puxar todos os comentários do Participa.br"%(time.time()-NOW,))

NOW=time.time()
print("dados lidos, processando")
import string, nltk as k
# histograma com as palavras
palavras=string.join([i["texto"]["value"].lower() for i in results4["results"]["bindings"]])
exclude = set(string.punctuation)
palavras = ''.join(ch for ch in palavras if ch not in exclude)
palavras_=palavras.split()
#fdist=k.FreqDist(palavras_)
print("feita primeira freq dist em %.2f"%(time.time()-NOW,))

NOW=time.time()
stopwords = set(k.corpus.stopwords.words('portuguese'))
palavras__=[pp for pp in palavras_ if pp not in stopwords]
fdist_=k.FreqDist(palavras__)
print("feita segunda freq dist (retiradas stopwords) em %.2f"%(time.time()-NOW,))

#NOW=time.time()
#stemmer = k.stem.RSLPStemmer()
#palavras___=[stemmer.stem(pp) for pp in palavras__]
#fdist__=k.FreqDist(palavras___)
#print("feita terceira freq dist (radicalizada) em %.2f"%(time.time()-NOW,))

##################
# bebe comentarios do endpoint sparql.
# guarda 10 e os classifica na mão

# faz histograma de todas as palavras
# escolhe as mais frequentes ou com offset
# ou as menos frequentes
# faz feture vector com elas.
# escolhendo as 200 palavras mais frequentes
palavras_escolhidas=fdist_.keys()[:200]
# outras features que podemos escolher é:
# *) número de palavras terminadas em a, o, e ou s
# *) tamanho médio das palavras utilizadas
# *) uso das stopwords

# é necessário um conjunto maior de classificações na mão
# para julgar qual parte do histograma
# é melhor de ser considerada.

#########
def document_features(documento):
    features={}
    for palavra in palavras_escolhidas:
        features["contains(%s)"%(palavra,)]=(palavra in documento)
    return features
# fazendo com classes dummy
msgs= [(rr["texto"]["value"],"pos") for rr in results4["results"]["bindings"][:1000]]
msgs2=[(rr["texto"]["value"],"neg") for rr in results4["results"]["bindings"][1000:2000]]
msgs_=msgs+msgs2
random.shuffle(msgs_)
feature_sets=[(document_features(msg[0]),msg[1]) for msg in msgs_]
train_set, test_set = feature_sets[1000:], feature_sets[:1000]
classifier = k.NaiveBayesClassifier.train(train_set)

########
# As mais frequentes podem ser úteis já que os comentários
# são pequenos e queremos que o vetor de atributos tenha informação

# As menos frequentes são as palavras mais incomuns, informativas
# para detecção de nichos do autor

# As de incidência intermediária são consideradas as mais representativas
# do assunto
