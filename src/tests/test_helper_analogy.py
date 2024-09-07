# src/tests/test_helper_analogy.py

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_analogy import (
    find_analogies,
    map_concepts,
    apply_analogy,
    evaluate_analogy
)

class TestHelperAnalogy(unittest.TestCase):
    def setUp(self):
        self.source_domain = "The solar system consists of planets orbiting around the sun."
        self.target_domain = "The atom consists of electrons orbiting around the nucleus."

    def test_find_analogies(self):
        analogies = find_analogies(self.source_domain, self.target_domain, num_analogies=3)
        self.assertEqual(len(analogies), 3)
        for analogy in analogies:
            self.assertIn('source_concept', analogy)
            self.assertIn('target_concept', analogy)
            self.assertIn('similarity', analogy)
            self.assertTrue(0 <= analogy['similarity'] <= 1)

    def test_map_concepts(self):
        result = map_concepts("planet", self.source_domain, self.target_domain)
        self.assertIn('source_concept', result)
        self.assertIn('mapped_concept', result)
        self.assertIn('source_similarity', result)
        self.assertIn('target_similarity', result)
        self.assertEqual(result['source_concept'], "planet")
        self.assertTrue(0 <= result['source_similarity'] <= 1)
        self.assertTrue(0 <= result['target_similarity'] <= 1)

    def test_apply_analogy(self):
        source_problem = "How do planets stay in orbit around the sun?"
        source_solution = "Planets stay in orbit due to the gravitational force of the sun."
        target_problem = "How do electrons stay in orbit around the nucleus?"

        result = apply_analogy(source_problem, source_solution, target_problem)
        self.assertIn('proposed_solution', result)
        self.assertIn('confidence', result)
        self.assertTrue(0 <= result['confidence'] <= 1)

    def test_evaluate_analogy(self):
        analogy = {
            "source_concept": "planet",
            "target_concept": "electron",
            "similarity": 0.7
        }
        context = "We are studying the structure of atoms and the behavior of subatomic particles."

        evaluation = evaluate_analogy(analogy, context)
        self.assertIn('source_relevance', evaluation)
        self.assertIn('target_relevance', evaluation)
        self.assertIn('overall_relevance', evaluation)
        self.assertIn('applicability', evaluation)
        self.assertTrue(0 <= evaluation['source_relevance'] <= 1)
        self.assertTrue(0 <= evaluation['target_relevance'] <= 1)
        self.assertTrue(0 <= evaluation['overall_relevance'] <= 1)
        self.assertTrue(0 <= evaluation['applicability'] <= 1)

if __name__ == '__main__':
    unittest.main()
