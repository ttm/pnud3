#-*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON

# testes

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Love> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

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
#sparql3 = SPARQLWrapper("http://localhost:82/participabr/query")
sparql3 = SPARQLWrapper("http://200.144.255.210:8082/participabr/query")
sparql3.setQuery(PREFIX+q2)
sparql3.setReturnFormat(JSON)
results3 = sparql3.query().convert()

for i in results3["results"]["bindings"][-10:]: print(u"participante: " +i["nome"]["value"])

q="SELECT ?comentario ?titulo ?texto WHERE {?comentario dc:type tsioc:Comment. ?comentario dc:title ?titulo . ?comentario schema:text ?texto}"
sparql3.setQuery(PREFIX+q)
sparql3.setReturnFormat(JSON)
results4 = sparql3.query().convert()
##################
# bebe comentarios do endpoint sparql.
# guarda 10 e os classifica na mão

# faz histograma de todas as palavras
# escolhe as mais frequentes ou com offset
# ou as menos frequentes
# faz feture vector com elas.

# é necessário um conjunto maior de classificações na mão
# para julgar qual parte do histograma
# é melhor de ser considerada.

########
# As mais frequentes podem ser úteis já que os comentários
# são pequenos e queremos que o vetor de atributos tenha informação

# As menos frequentes são as palavras mais incomuns, informativas
# para detecção de nichos do autor

# As de incidência intermediária são consideradas as mais representativas
# do assunto

