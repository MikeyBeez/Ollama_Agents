# src/tests/test_system_dynamics_helpers.py

import unittest
import networkx as nx
from src.modules.helper_system_dynamics import *

class TestSystemDynamicsHelpers(unittest.TestCase):

    def setUp(self):
        self.nodes = ['A', 'B', 'C']
        self.edges = [('A', 'B', {'weight': 0.5}), ('B', 'C', {'weight': 0.7}), ('C', 'A', {'weight': 0.3})]
        self.G = create_system_graph(self.nodes, self.edges)

    def test_create_system_graph(self):
        self.assertIsInstance(self.G, nx.DiGraph)
        self.assertEqual(set(self.G.nodes()), set(self.nodes))
        self.assertEqual(set(self.G.edges()), set((a, b) for a, b, _ in self.edges))

    def test_identify_feedback_loops(self):
        loops = identify_feedback_loops(self.G)
        self.assertEqual(len(loops), 1)
        self.assertEqual(set(loops[0]), set(self.nodes))

    def test_calculate_centrality(self):
        centrality = calculate_centrality(self.G)
        self.assertEqual(set(centrality.keys()), set(self.nodes))
        self.assertTrue(all(0 <= v <= 1 for v in centrality.values()))

    def test_identify_bottlenecks(self):
        bottlenecks = identify_bottlenecks(self.G)
        self.assertTrue(set(bottlenecks).issubset(set(self.nodes)))

    def test_simulate_system_behavior(self):
        initial_state = {node: 1.0 for node in self.nodes}
        time_steps = 10
        time_series = simulate_system_behavior(self.G, time_steps, initial_state)
        self.assertEqual(set(time_series.keys()), set(self.nodes))
        self.assertTrue(all(len(v) == time_steps + 1 for v in time_series.values()))

    def test_analyze_system_dynamics(self):
        initial_state = {node: 1.0 for node in self.nodes}
        time_steps = 10
        analysis = analyze_system_dynamics(self.nodes, self.edges, initial_state, time_steps)
        self.assertIn('feedback_loops', analysis)
        self.assertIn('centrality', analysis)
        self.assertIn('bottlenecks', analysis)
        self.assertIn('time_series', analysis)

if __name__ == '__main__':
    unittest.main()
