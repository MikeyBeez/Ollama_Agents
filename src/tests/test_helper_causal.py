# src/tests/test_helper_causal.py

import unittest
import sys
import os
import networkx as nx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_causal import (
    extract_entities,
    extract_relationships,
    build_causal_graph,
    infer_causal_relationships,
    estimate_causal_strength
)

class TestHelperCausal(unittest.TestCase):
    def setUp(self):
        self.sample_context = "The excessive rain caused flooding in the city, which led to property damage and traffic disruptions."

    def test_extract_entities(self):
        entities = extract_entities(self.sample_context)
        self.assertGreater(len(entities), 0)
        self.assertTrue(any('rain' in entity.lower() for entity in entities))
        self.assertTrue(any('flooding' in entity.lower() for entity in entities))
        self.assertTrue(any('city' in entity.lower() for entity in entities))

    def test_extract_relationships(self):
        entities = extract_entities(self.sample_context)
        relationships = extract_relationships(self.sample_context, entities)
        self.assertGreater(len(relationships), 0)

        rain_flooding_relation = False
        for r in relationships:
            if ('rain' in r["source"].lower() and 'flooding' in r["target"].lower()) or \
               ('flooding' in r["source"].lower() and 'rain' in r["target"].lower()) or \
               ('rain' in r["source"].lower() and 'caused' in r["target"].lower()) or \
               ('caused' in r["source"].lower() and 'flooding' in r["target"].lower()):
                rain_flooding_relation = True
                break

        self.assertTrue(rain_flooding_relation, "Expected to find a relationship between 'rain' and 'flooding'")

    def test_build_causal_graph(self):
        relationships = [
            {"source": "rain", "target": "flooding", "relationship": "nsubj"},
            {"source": "flooding", "target": "damage", "relationship": "dobj"}
        ]
        graph = build_causal_graph(relationships)
        self.assertIsInstance(graph, nx.DiGraph)
        self.assertTrue(graph.has_edge("rain", "flooding"))
        self.assertTrue(graph.has_edge("flooding", "damage"))

    def test_infer_causal_relationships(self):
        G = nx.DiGraph()
        G.add_edge("rain", "flooding")
        G.add_edge("flooding", "damage")
        causal_relationships = infer_causal_relationships(G)
        self.assertEqual(len(causal_relationships), 2)
        self.assertTrue(any(r["cause"] == "rain" and r["effect"] == "flooding" for r in causal_relationships))
        self.assertTrue(any(r["cause"] == "flooding" and r["effect"] == "damage" for r in causal_relationships))

    def test_estimate_causal_strength(self):
        strength = estimate_causal_strength("rain", "flooding", self.sample_context)
        self.assertGreaterEqual(strength, 0)
        self.assertLessEqual(strength, 1)

        strength_related = estimate_causal_strength("rain", "flooding", self.sample_context)
        strength_unrelated = estimate_causal_strength("rain", "sunshine", self.sample_context)
        self.assertGreater(strength_related, strength_unrelated)

    def test_estimate_causal_strength_ranges(self):
        test_cases = [
            ("rain", "flooding", (0.1, 1.0)),
            ("flooding", "damage", (0.1, 1.0)),
            ("rain", "sunshine", (0.0, 0.5))
        ]
        for cause, effect, expected_range in test_cases:
            strength = estimate_causal_strength(cause, effect, self.sample_context)
            self.assertGreaterEqual(strength, expected_range[0])
            self.assertLessEqual(strength, expected_range[1])

    def test_full_causal_analysis(self):
        entities = extract_entities(self.sample_context)
        relationships = extract_relationships(self.sample_context, entities)
        graph = build_causal_graph(relationships)
        causal_relationships = infer_causal_relationships(graph)

        for relationship in causal_relationships:
            relationship['strength'] = estimate_causal_strength(
                relationship['cause'], relationship['effect'], self.sample_context
            )

        self.assertGreaterEqual(len(causal_relationships), 0)
        for relationship in causal_relationships:
            self.assertIn('cause', relationship)
            self.assertIn('effect', relationship)
            self.assertIn('confidence', relationship)
            self.assertIn('strength', relationship)
            self.assertGreaterEqual(relationship['strength'], 0)
            self.assertLessEqual(relationship['strength'], 1)

    def test_empty_context(self):
        empty_context = ""
        self.assertEqual(extract_entities(empty_context), [])
        self.assertEqual(extract_relationships(empty_context, []), [])

        empty_graph = build_causal_graph([])
        self.assertIsInstance(empty_graph, nx.DiGraph)
        self.assertEqual(len(empty_graph.nodes()), 0)
        self.assertEqual(len(empty_graph.edges()), 0)

    def test_complex_context(self):
        complex_context = """
        Climate change has led to rising global temperatures. These increased temperatures
        have caused polar ice caps to melt, resulting in rising sea levels. The rising sea
        levels threaten coastal cities with flooding, which could displace millions of people
        and cause significant economic damage.
        """
        entities = extract_entities(complex_context)
        self.assertGreater(len(entities), 3)  # Expecting multiple entities

        common_terms = ['climate', 'change', 'temperatures', 'ice', 'caps', 'sea', 'levels', 'cities', 'flooding']
        self.assertTrue(any(term.lower() in ' '.join(entities).lower() for term in common_terms))

        relationships = extract_relationships(complex_context, entities)
        graph = build_causal_graph(relationships)
        causal_relationships = infer_causal_relationships(graph)

        self.assertGreater(len(causal_relationships), 0)  # Expecting at least one causal relationship

    def test_cyclic_relationships(self):
        cyclic_relationships = [
            {"source": "A", "target": "B", "relationship": "causes"},
            {"source": "B", "target": "C", "relationship": "causes"},
            {"source": "C", "target": "A", "relationship": "causes"}
        ]
        graph = build_causal_graph(cyclic_relationships)
        self.assertTrue(nx.is_strongly_connected(graph))  # The graph should be strongly connected due to the cycle

        causal_relationships = infer_causal_relationships(graph)
        self.assertEqual(len(causal_relationships), 3)
        # Check that all relationships are present
        self.assertTrue(any(r["cause"] == "A" and r["effect"] == "B" for r in causal_relationships))
        self.assertTrue(any(r["cause"] == "B" and r["effect"] == "C" for r in causal_relationships))
        self.assertTrue(any(r["cause"] == "C" and r["effect"] == "A" for r in causal_relationships))

if __name__ == '__main__':
    unittest.main()
