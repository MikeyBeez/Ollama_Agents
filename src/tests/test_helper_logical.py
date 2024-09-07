# src/tests/test_helper_logical.py

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_logical import (
    parse_logical_statement,
    check_validity,
    identify_fallacies,
    generate_truth_table
)

class TestHelperLogical(unittest.TestCase):
    def test_parse_logical_statement(self):
        statement = "If it rains, then the ground will be wet"
        parsed = parse_logical_statement(statement)
        self.assertEqual(parsed["type"], "conditional")
        self.assertEqual(parsed["antecedent"], "it rains")
        self.assertEqual(parsed["consequent"], "the ground will be wet")

        statement = "All dogs are mammals"
        parsed = parse_logical_statement(statement)
        self.assertEqual(parsed["type"], "universal")
        self.assertEqual(parsed["subject"], "dogs")
        self.assertEqual(parsed["predicate"], "mammals")

    def test_check_validity(self):
        premises = [
            "If it rains, then the ground will be wet",
            "It rains"
        ]
        conclusion = "The ground will be wet"
        result = check_validity(premises, conclusion)
        self.assertTrue(result["valid"])
        self.assertEqual(result["explanation"], "Valid modus ponens argument.")

        premises = [
            "If it rains, then the ground will be wet",
            "The ground is wet"
        ]
        conclusion = "It rained"
        result = check_validity(premises, conclusion)
        self.assertFalse(result["valid"])

    def test_identify_fallacies(self):
        argument = "You're stupid, so your argument must be wrong."
        fallacies = identify_fallacies(argument)
        self.assertEqual(len(fallacies), 1)
        self.assertEqual(fallacies[0]["type"], "ad hominem")

        argument = "If we don't act now, everyone will die! We must act immediately!"
        fallacies = identify_fallacies(argument)
        self.assertEqual(len(fallacies), 1)  # only hasty generalization
        self.assertEqual(fallacies[0]["type"], "hasty generalization")

    def test_generate_truth_table(self):
        statement = "A AND B"
        truth_table = generate_truth_table(statement)
        self.assertEqual(len(truth_table), 4)  # 2^2 rows
        self.assertTrue(all(set(row.keys()) == {'A', 'B', 'result'} for row in truth_table))

        true_count = sum(1 for row in truth_table if row['result'] is True)
        self.assertEqual(true_count, 1, f"Expected 1 True result, but got {true_count}. Truth table: {truth_table}")

        # Check specific cases
        self.assertFalse(truth_table[0]['result'], f"Expected False for False AND False, but got {truth_table[0]}")
        self.assertFalse(truth_table[1]['result'], f"Expected False for False AND True, but got {truth_table[1]}")
        self.assertFalse(truth_table[2]['result'], f"Expected False for True AND False, but got {truth_table[2]}")
        self.assertTrue(truth_table[3]['result'], f"Expected True for True AND True, but got {truth_table[3]}")

        statement = "A OR NOT B"
        truth_table = generate_truth_table(statement)
        self.assertEqual(len(truth_table), 4)  # 2^2 rows

        true_count = sum(1 for row in truth_table if row['result'] is True)
        self.assertEqual(true_count, 3, f"Expected 3 True results, but got {true_count}. Truth table: {truth_table}")

        # Check specific cases
        self.assertTrue(truth_table[0]['result'], f"Expected True for False OR NOT False, but got {truth_table[0]}")
        self.assertFalse(truth_table[1]['result'], f"Expected False for False OR NOT True, but got {truth_table[1]}")
        self.assertTrue(truth_table[2]['result'], f"Expected True for True OR NOT False, but got {truth_table[2]}")
        self.assertTrue(truth_table[3]['result'], f"Expected True for True OR NOT True, but got {truth_table[3]}")

if __name__ == '__main__':
    unittest.main()
