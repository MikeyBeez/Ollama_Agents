# src/modules/knowledge_management.py

import json
import networkx as nx
from typing import List, Dict, Any, Tuple
from datetime import datetime
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.errors import DataProcessingError

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_node(self, node_id: str, attributes: Dict[str, Any]):
        self.graph.add_node(node_id, **attributes)

    def add_edge(self, source: str, target: str, relationship: str, weight: float = 1.0, timestamp: datetime = datetime.now()):
        self.graph.add_edge(source, target, relationship=relationship, weight=weight, timestamp=timestamp)

    def get_node(self, node_id: str) -> Dict[str, Any]:
        return self.graph.nodes[node_id]

    def get_related_nodes(self, node_id: str, relationship: str = None) -> List[Tuple[str, str, float]]:
        related = []
        for _, target, data in self.graph.out_edges(node_id, data=True):
            if relationship is None or data['relationship'] == relationship:
                related.append((target, data['relationship'], data['weight']))
        return related

    def update_edge_weight(self, source: str, target: str, relationship: str, new_weight: float):
        self.graph[source][target][relationship]['weight'] = new_weight
        self.graph[source][target][relationship]['timestamp'] = datetime.now()

class KnowledgeManager:
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph()

    def add_fact(self, fact: str, source: str, confidence: float):
        fact_id = self._generate_id(fact)
        self.knowledge_graph.add_node(fact_id, {'type': 'fact', 'content': fact, 'source': source})
        self.knowledge_graph.add_edge('root', fact_id, 'contains', weight=confidence)

    def add_relationship(self, source_fact: str, target_fact: str, relationship: str, confidence: float):
        source_id = self._generate_id(source_fact)
        target_id = self._generate_id(target_fact)
        self.knowledge_graph.add_edge(source_id, target_id, relationship, weight=confidence)

    def get_related_facts(self, fact: str, relationship: str = None) -> List[Tuple[str, str, float]]:
        fact_id = self._generate_id(fact)
        return self.knowledge_graph.get_related_nodes(fact_id, relationship)

    def update_fact_confidence(self, fact: str, new_confidence: float):
        fact_id = self._generate_id(fact)
        self.knowledge_graph.update_edge_weight('root', fact_id, 'contains', new_confidence)

    def _generate_id(self, content: str) -> str:
        return hash(content)

    def to_json(self) -> str:
        return json.dumps(nx.node_link_data(self.knowledge_graph.graph))

    def from_json(self, json_data: str):
        data = json.loads(json_data)
        self.knowledge_graph.graph = nx.node_link_graph(data)

knowledge_manager = KnowledgeManager()

def classify_query_topic(query: str, model_name: str) -> str:
    """
    Classify the given query into a topic.
    """
    try:
        classification_prompt = f"Classify the following query into a general topic area: {query}"
        return process_prompt(classification_prompt, model_name, "TopicClassifier")
    except Exception as e:
        logger.error(f"Error classifying query topic: {str(e)}")
        return "general"

def determine_research_depth(query: str, model_name: str) -> int:
    """
    Determine the appropriate research depth for a given query.
    """
    try:
        depth_prompt = f"On a scale of 1 to 5, how deep should the research go for this query: '{query}'? Respond with ONLY a single integer between 1 and 5."
        depth = int(process_prompt(depth_prompt, model_name, "ResearchDepthDeterminer").strip())
        return max(1, min(depth, 5))
    except Exception as e:
        logger.error(f"Error determining research depth: {str(e)}")
        return 3  # Default to medium depth if there's an error

def process_query(user_input: str, model_name: str) -> Dict[str, Any]:
    """
    Process a user query to extract topic and research depth.
    """
    try:
        topic = classify_query_topic(user_input, model_name)
        depth = determine_research_depth(user_input, model_name)
        return {
            "topic": topic,
            "depth": depth
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {"topic": "general", "depth": 3}

def assess_source_credibility(source: str, model_name: str) -> float:
    """
    Assess the credibility of a given source.
    """
    try:
        credibility_prompt = f"Assess the credibility of this source on a scale of 0 to 1: {source}"
        credibility_score = float(process_prompt(credibility_prompt, model_name, "CredibilityAssessor").strip())
        return max(0, min(credibility_score, 1))
    except Exception as e:
        logger.error(f"Error assessing source credibility: {str(e)}")
        return 0.5  # Default to neutral credibility if there's an error

def update_knowledge_base(new_info: str, topic: str, model_name: str) -> None:
    """
    Update the knowledge base with new information on a given topic.
    """
    try:
        confidence = assess_source_credibility(new_info, model_name)
        knowledge_manager.add_fact(new_info, "user_input", confidence)
        knowledge_manager.add_relationship("root", new_info, topic, confidence)
        logger.info(f"Knowledge base updated with new information on topic: {topic}")
    except Exception as e:
        logger.error(f"Error updating knowledge base: {str(e)}")

def extract_key_concepts(text: str, model_name: str) -> List[str]:
    """
    Extract key concepts from a given text.
    """
    try:
        extraction_prompt = f"Extract the key concepts from the following text as a comma-separated list: {text}"
        concepts = process_prompt(extraction_prompt, model_name, "ConceptExtractor")
        return [concept.strip() for concept in concepts.split(',')]
    except Exception as e:
        logger.error(f"Error extracting key concepts: {str(e)}")
        return []

def generate_follow_up_questions(context: str, model_name: str) -> List[str]:
    """
    Generate follow-up questions based on the given context.
    """
    try:
        question_prompt = f"Based on the following context, generate 3 relevant follow-up questions:\n\n{context}"
        questions = process_prompt(question_prompt, model_name, "QuestionGenerator")
        return [q.strip() for q in questions.split('\n') if q.strip()]
    except Exception as e:
        logger.error(f"Error generating follow-up questions: {str(e)}")
        return []

def summarize_topic(topic: str, context: str, model_name: str) -> str:
    """
    Generate a summary of a given topic based on the provided context.
    """
    try:
        summary_prompt = f"Summarize the following information about the topic '{topic}':\n\n{context}"
        return process_prompt(summary_prompt, model_name, "TopicSummarizer")
    except Exception as e:
        logger.error(f"Error summarizing topic: {str(e)}")
        return f"Unable to summarize topic '{topic}' due to an error."

def identify_knowledge_gaps(topic: str, current_knowledge: str, model_name: str) -> List[str]:
    """
    Identify gaps in the current knowledge about a given topic.
    """
    try:
        gap_prompt = f"Given the current knowledge about the topic '{topic}':\n\n{current_knowledge}\n\nIdentify potential gaps or areas that require further research."
        gaps = process_prompt(gap_prompt, model_name, "KnowledgeGapIdentifier")
        return [gap.strip() for gap in gaps.split('\n') if gap.strip()]
    except Exception as e:
        logger.error(f"Error identifying knowledge gaps: {str(e)}")
        return []

def compare_information(info1: str, info2: str, model_name: str) -> Dict[str, Any]:
    """
    Compare two pieces of information and identify similarities and differences.
    """
    try:
        compare_prompt = f"Compare the following two pieces of information:\n\nInfo 1: {info1}\n\nInfo 2: {info2}\n\nIdentify key similarities and differences."
        comparison = process_prompt(compare_prompt, model_name, "InformationComparer")
        return json.loads(comparison)
    except Exception as e:
        logger.error(f"Error comparing information: {str(e)}")
        return {"similarities": [], "differences": [], "error": str(e)}

def validate_information(info: str, model_name: str) -> Dict[str, Any]:
    """
    Validate a piece of information and assess its reliability.
    """
    try:
        validation_prompt = f"Validate the following information and assess its reliability:\n\n{info}"
        validation = process_prompt(validation_prompt, model_name, "InformationValidator")
        return json.loads(validation)
    except Exception as e:
        logger.error(f"Error validating information: {str(e)}")
        return {"reliability": 0.5, "explanation": f"Error in validation: {str(e)}"}

def generate_knowledge_tree(topic: str, model_name: str) -> Dict[str, Any]:
    """
    Generate a knowledge tree for a given topic.
    """
    try:
        tree_prompt = f"Generate a knowledge tree for the topic '{topic}'. Include main branches and sub-branches."
        tree = process_prompt(tree_prompt, model_name, "KnowledgeTreeGenerator")
        return json.loads(tree)
    except Exception as e:
        logger.error(f"Error generating knowledge tree: {str(e)}")
        return {"topic": topic, "branches": [], "error": str(e)}

def evaluate_knowledge_consistency(statements: List[str], model_name: str) -> Dict[str, Any]:
    """
    Evaluate the consistency of a set of knowledge statements.
    """
    try:
        consistency_prompt = f"Evaluate the consistency of the following statements:\n\n{json.dumps(statements)}\n\nIdentify any inconsistencies or contradictions."
        evaluation = process_prompt(consistency_prompt, model_name, "ConsistencyEvaluator")
        return json.loads(evaluation)
    except Exception as e:
        logger.error(f"Error evaluating knowledge consistency: {str(e)}")
        return {"consistency_score": 0.5, "inconsistencies": [], "error": str(e)}

def infer_new_knowledge(knowledge_manager: KnowledgeManager, model_name: str) -> List[Tuple[str, str, str, float]]:
    """
    Infer new knowledge based on existing knowledge in the knowledge graph.
    """
    try:
        # Extract existing knowledge from the graph
        existing_knowledge = knowledge_manager.to_json()
        inference_prompt = f"Based on the following knowledge graph, infer new relationships or facts:\n\n{existing_knowledge}"
        inferred_knowledge = process_prompt(inference_prompt, model_name, "KnowledgeInferer")

        # Parse and validate inferred knowledge
        inferred_items = json.loads(inferred_knowledge)
        validated_inferences = []
        for item in inferred_items:
            if validate_new_knowledge(item['fact'], knowledge_manager, model_name)[0]:
                validated_inferences.append((item['source'], item['target'], item['relationship'], item['confidence']))

        return validated_inferences
    except Exception as e:
        logger.error(f"Error inferring new knowledge: {str(e)}")
        return []

def validate_new_knowledge(fact: str, existing_knowledge: KnowledgeManager, model_name: str) -> Tuple[bool, float]:
    """
    Validate new knowledge against existing knowledge.
    """
    try:
        existing_facts = existing_knowledge.to_json()
        validation_prompt = f"Validate the following new fact against the existing knowledge:\n\nNew fact: {fact}\n\nExisting knowledge: {existing_facts}\n\nIs this new fact consistent with and supported by the existing knowledge? Respond with 'True' or 'False' and provide a confidence score between 0 and 1."
        validation_result = process_prompt(validation_prompt, model_name, "KnowledgeValidator")
        is_valid, confidence = validation_result.split(',')
        return bool(is_valid.strip().lower() == 'true'), float(confidence.strip())
    except Exception as e:
        logger.error(f"Error validating new knowledge: {str(e)}")
        return False, 0.0
