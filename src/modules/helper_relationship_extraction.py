# src/modules/helper_relationship_extraction.py

import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def extract_relationships(context, entities):
    # Parse the context
    doc = nlp(context)

    relationships = []

    print("Tokens and their dependencies:")
    for token in doc:
        print(f"{token.text}: {token.dep_} ({token.pos_})")

    # Iterate through the tokens in the parsed document
    for token in doc:
        # Check if the token is a verb
        if token.pos_ == "VERB":
            # Find the subject, direct object, and indirect object of the verb
            subject = None
            dobj = None
            iobj = None
            prep_objs = []
            for child in token.children:
                if child.dep_ == "nsubj" and any(ent.lower() in child.text.lower() for ent in entities):
                    subject = child.text
                if child.dep_ in ["dobj", "attr"] and any(ent.lower() in child.text.lower() for ent in entities):
                    dobj = child.text
                if child.dep_ in ["iobj", "dative"] and any(ent.lower() in child.text.lower() for ent in entities):
                    iobj = child.text
                if child.dep_ == "prep":
                    for grandchild in child.children:
                        if grandchild.dep_ == "pobj" and any(ent.lower() in grandchild.text.lower() for ent in entities):
                            prep_objs.append((child.text, grandchild.text))

            print(f"For verb '{token.text}': subject={subject}, dobj={dobj}, iobj={iobj}, prep_objs={prep_objs}")

            # If subject and direct object are found, add the relationship
            if subject and dobj:
                relationships.append({
                    "source": subject,
                    "target": dobj,
                    "relationship": token.lemma_
                })

            # If subject and indirect object are found, add the relationship
            if subject and iobj:
                relationships.append({
                    "source": subject,
                    "target": iobj,
                    "relationship": token.lemma_
                })

            # Handle prepositional objects
            if subject and prep_objs:
                for prep, obj in prep_objs:
                    relationships.append({
                        "source": subject,
                        "target": obj,
                        "relationship": f"{token.lemma_}_{prep}"
                    })

    print("Extracted relationships:", relationships)
    return relationships
