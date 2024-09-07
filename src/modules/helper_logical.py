# src/modules/helper_logical.py

import re
from typing import List, Dict, Any

def parse_logical_statement(statement: str) -> Dict[str, Any]:
    parts = statement.lower().split()

    if "if" in parts and "then" in parts:
        antecedent = " ".join(parts[parts.index("if")+1:parts.index("then")])
        antecedent = antecedent.rstrip(',')  # Remove trailing comma
        consequent = " ".join(parts[parts.index("then")+1:])
        return {"type": "conditional", "antecedent": antecedent, "consequent": consequent}
    elif "all" in parts:
        subject = parts[parts.index("all")+1]
        predicate = " ".join(parts[parts.index("are")+1:])
        return {"type": "universal", "subject": subject, "predicate": predicate}
    elif "some" in parts:
        subject = parts[parts.index("some")+1]
        predicate = " ".join(parts[parts.index("are")+1:])
        return {"type": "existential", "subject": subject, "predicate": predicate}
    else:
        return {"type": "simple", "content": statement}

def check_validity(premises: List[str], conclusion: str) -> Dict[str, Any]:
    parsed_premises = [parse_logical_statement(premise) for premise in premises]
    parsed_conclusion = parse_logical_statement(conclusion)

    if len(parsed_premises) == 2:
        if parsed_premises[0]["type"] == "conditional" and \
           parsed_premises[1]["type"] == "simple" and \
           parsed_premises[1]["content"].lower() == parsed_premises[0]["antecedent"].lower() and \
           parsed_conclusion["type"] == "simple" and \
           parsed_conclusion["content"].lower() == parsed_premises[0]["consequent"].lower():
            return {"valid": True, "explanation": "Valid modus ponens argument."}

    return {"valid": False, "explanation": "No valid argument form recognized."}

def identify_fallacies(argument: str) -> List[Dict[str, Any]]:
    fallacies = []

    if re.search(r'\b(stupid|idiot|fool)\b', argument, re.IGNORECASE):
        fallacies.append({
            "type": "ad hominem",
            "explanation": "The argument attacks the person rather than addressing the claim."
        })

    if re.search(r'\b(fear|scary|terrifying)\b', argument, re.IGNORECASE):
        fallacies.append({
            "type": "appeal to emotion",
            "explanation": "The argument relies on emotional manipulation rather than logical reasoning."
        })

    if re.search(r'\b(all|every|always|never|everyone|everybody)\b', argument, re.IGNORECASE):
        fallacies.append({
            "type": "hasty generalization",
            "explanation": "The argument draws a general conclusion from insufficient evidence."
        })

    return fallacies

def generate_truth_table(statement: str) -> List[Dict[str, Any]]:
    """
    Generate a truth table for a given logical statement.

    Args:
    statement (str): Logical statement using AND, OR, NOT, and variables (A-Z).

    Returns:
    List[Dict[str, Any]]: Truth table with variable assignments and result.
    """

    # Extract variables from the statement
    variables = sorted(set(re.findall(r'\b[A-Z]\b', statement)))
    n_variables = len(variables)

    # Replace logical operators (case-insensitive)
    statement = re.sub(r'\bAND\b', 'and', statement, flags=re.IGNORECASE)
    statement = re.sub(r'\bOR\b', 'or', statement, flags=re.IGNORECASE)
    statement = re.sub(r'\bNOT\b', 'not', statement, flags=re.IGNORECASE)

    truth_table = []
    for i in range(2**n_variables):
        row = {}
        for j, var in enumerate(variables):
            row[var] = bool(i & (1 << (n_variables - 1 - j)))

        # Replace variables with boolean values
        eval_statement = statement
        for var, value in row.items():
            eval_statement = eval_statement.replace(var, str(value))

        try:
            # Evaluate the statement
            row['result'] = eval(eval_statement)
        except Exception as e:
            # Handle evaluation errors
            print(f"Error evaluating {eval_statement}: {str(e)}")
            row['result'] = None

        truth_table.append(row)

    return truth_table
