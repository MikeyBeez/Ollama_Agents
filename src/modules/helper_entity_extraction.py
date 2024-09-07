# src/modules/helper_entity_extraction.py

import spacy
from typing import List

class EntityExtractionHelper:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def helper_extract_entities(self, context: str) -> List[str]:
        """
        Extract entities from the given context using NLP techniques.

        Args:
        context (str): The input text from which to extract entities.

        Returns:
        List[str]: A list of extracted entities.
        """
        doc = self.nlp(context)
        entities = []

        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]:
                entities.append(ent.text)

        # Also consider noun chunks as potential entities
        for chunk in doc.noun_chunks:
            if chunk.text not in entities:
                entities.append(chunk.text)

        return list(set(entities))  # Remove duplicates

# Example usage
if __name__ == "__main__":
    extractor = EntityExtractionHelper()
    context = "Apple Inc. released a new iPhone model in California last week. CEO Tim Cook announced it during a special event."
    entities = extractor.helper_extract_entities(context)
    print("Extracted entities:", entities)
