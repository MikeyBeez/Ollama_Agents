# src/modules/helper_causal.py

import networkx as nx
from typing import List, Dict, Any
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Spacy model 'en_core_web_sm' not found. Using a basic tokenizer instead.")
    nlp = spacy.blank("en")

def extract_entities(context: str) -> List[str]:
    doc = nlp(context)
    entities = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] or (token.dep_ in ['nsubj', 'dobj', 'pobj']):
            entities.append(token.text)
    return list(set(entities))

def extract_relationships(context: str, entities: List[str]) -> List[Dict[str, str]]:
    doc = nlp(context)
    relationships = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ["nsubj", "dobj", "pobj", "attr", "compound", "amod"]:
                source = token.text
                target = token.head.text

                # Check for compound words
                for child in token.children:
                    if child.dep_ == "compound":
                        source = f"{child.text} {source}"

                for child in token.head.children:
                    if child.dep_ == "compound":
                        target = f"{child.text} {target}"

                if any(entity.lower() in source.lower() for entity in entities) or \
                   any(entity.lower() in target.lower() for entity in entities):
                    relationships.append({
                        "source": source,
                        "target": target,
                        "relationship": token.dep_
                    })
    return relationships

def build_causal_graph(relationships: List[Dict[str, str]]) -> nx.DiGraph:
    G = nx.DiGraph()
    for rel in relationships:
        G.add_edge(rel['source'], rel['target'], relationship=rel['relationship'])
    return G

def infer_causal_relationships(causal_graph: nx.DiGraph) -> List[Dict[str, Any]]:
    causal_relationships = []
    for node in causal_graph.nodes():
        successors = list(causal_graph.successors(node))
        for successor in successors:
            causal_relationships.append({
                "cause": node,
                "effect": successor,
                "confidence": 0.5  # Default confidence, can be adjusted based on more sophisticated analysis
            })
    return causal_relationships

def estimate_causal_strength(cause: str, effect: str, context: str) -> float:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cause, effect, context])

    cause_vec = tfidf_matrix[0]
    effect_vec = tfidf_matrix[1]
    context_vec = tfidf_matrix[2]

    cause_context_sim = cosine_similarity(cause_vec, context_vec)[0][0]
    effect_context_sim = cosine_similarity(effect_vec, context_vec)[0][0]
    cause_effect_sim = cosine_similarity(cause_vec, effect_vec)[0][0]

    strength = (cause_context_sim + effect_context_sim + cause_effect_sim) / 3
    return float(strength)
