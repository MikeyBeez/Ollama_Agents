# src/tests/test_helper_analogy.py

import unittest
from src.modules.helper_analogy import find_analogies, map_concepts, apply_analogy, evaluate_analogy, generate_analogy_chain

class TestHelperAnalogy(unittest.TestCase):

    def test_find_analogies(self):
        source_domain = "The solar system consists of planets orbiting around the sun."
        target_domain = "The atom consists of electrons orbiting around the nucleus."
        analogies = find_analogies(source_domain, target_domain, num_analogies=3)
        self.assertEqual(len(analogies), 3)
        for analogy in analogies:
            self.assertIn('source_concept', analogy)
            self.assertIn('target_concept', analogy)
            self.assertIn('similarity', analogy)
            self.assertTrue(0 <= analogy['similarity'] <= 1)

    def test_map_concepts(self):
        result = map_concepts("planet", "The solar system consists of planets orbiting around the sun.",
                              "The atom consists of electrons orbiting around the nucleus.")
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
        self.assertIn('probabilistic_assessment', result)
        self.assertTrue(0 <= result['confidence'] <= 1)
        self.assertIn('posterior_probability', result['probabilistic_assessment'])

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

    def test_generate_analogy_chain(self):
        initial_domain = "The solar system consists of planets orbiting around the sun."
        target_domain = "The corporate structure consists of departments reporting to the CEO."
        steps = 3
        analogy_chain = generate_analogy_chain(initial_domain, target_domain, steps)
        self.assertEqual(len(analogy_chain), steps + 1)
        for analogy in analogy_chain:
            self.assertIn('source_concept', analogy)
            self.assertIn('target_concept', analogy)
            self.assertIn('similarity', analogy)

if __name__ == '__main__':
    unittest.main()
