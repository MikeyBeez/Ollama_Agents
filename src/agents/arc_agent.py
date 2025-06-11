"""
ARC Challenge Specialized Agent
Extends debug agent with grid-based reasoning capabilities
"""

import sys
import os
from typing import Dict, List, Optional, Any
import numpy as np
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agents.debug_agent import DebugAgent, debug_panel
from src.modules.adv_reasoning_engine import ReasoningEngine
from src.modules.adv_knowledge_manager import KnowledgeManager
from src.modules.logging_setup import logger
from config import DEFAULT_MODEL

console = Console()

class ARCAgent(DebugAgent):
    def __init__(self, model_name=DEFAULT_MODEL):
        super().__init__(model_name)
        self.grid_patterns = KnowledgeManager()  # Specialized for grid patterns
        
    @debug_panel
    def analyze_grid_transformation(self, input_grid: List[List[int]], 
                                  output_grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze transformation between input and output grids using reasoning engine"""
        
        # Convert grids to more detailed format for analysis
        context = {
            'input_grid': input_grid,
            'output_grid': output_grid,
            'input_shape': np.array(input_grid).shape,
            'output_shape': np.array(output_grid).shape
        }
        
        # Use reasoning engine for causal analysis
        causal_relations = self.reasoning_engine.perform_causal_analysis(context)
        
        # Generate and test hypotheses about the transformation
        hypotheses = self.reasoning_engine.generate_hypotheses(context)
        tested_hypotheses = self.reasoning_engine.test_hypotheses(hypotheses, context)
        
        # Look for analogous patterns in knowledge base
        analogies = self.reasoning_engine.find_analogies(str(input_grid), context)
        
        # Generate transformation explanation
        analysis = {
            'causal_relations': causal_relations,
            'verified_hypotheses': tested_hypotheses,
            'similar_patterns': analogies,
            'transformation_type': self._classify_transformation(tested_hypotheses)
        }
        
        # Update knowledge graph with new pattern
        self._update_pattern_knowledge(analysis)
        
        return analysis
    
    @debug_panel
    def discover_grid_functions(self, code_content: str) -> List[Dict[str, Any]]:
        """Analyze Python code to discover grid manipulation functions"""
        
        # Use reasoning engine to analyze code structure
        context = {'code': code_content, 'type': 'grid_function_analysis'}
        
        # Generate hypotheses about function purposes
        hypotheses = self.reasoning_engine.generate_hypotheses(context)
        
        # Test hypotheses about functions
        tested_hypotheses = self.reasoning_engine.test_hypotheses(hypotheses, context)
        
        discovered_functions = []
        for hypothesis in tested_hypotheses:
            if hypothesis.get('confidence', 0) > 0.7:  # Only include high confidence discoveries
                func_info = {
                    'name': hypothesis['function_name'],
                    'purpose': hypothesis['predicted_purpose'],
                    'input_type': hypothesis['expected_input'],
                    'output_type': hypothesis['expected_output'],
                    'confidence': hypothesis['confidence']
                }
                discovered_functions.append(func_info)
                
        # Update knowledge graph with function information
        self._update_function_knowledge(discovered_functions)
        
        return discovered_functions
    
    @debug_panel 
    def validate_recipe(self, recipe: List[str], test_case: Dict) -> Dict[str, Any]:
        """Validate a recipe (sequence of function calls) against a test case"""
        
        # Create execution plan
        plan = self.planning_engine.create_and_analyze_plan(
            str(recipe),
            {'test_case': test_case},
            self.knowledge_manager.get_relevant_knowledge(str(recipe)),
            cached_only=True  # Don't perform new web searches
        )
        
        # Analyze potential issues
        causal_analysis = self.reasoning_engine.perform_causal_analysis({
            'plan': plan,
            'recipe': recipe,
            'test_case': test_case
        })
        
        validation_result = {
            'is_valid': bool(plan.get('predicted_success')),
            'confidence': float(plan.get('confidence', 0)),
            'potential_issues': causal_analysis.get('potential_issues', []),
            'suggested_improvements': plan.get('suggested_improvements', [])
        }
        
        return validation_result
    
    @debug_panel
    def _classify_transformation(self, hypotheses: List[Dict]) -> str:
        """Classify the type of grid transformation based on tested hypotheses"""
        # Implementation would analyze hypotheses to determine transformation type
        transformation_types = [h.get('transformation_type') for h in hypotheses 
                              if h.get('confidence', 0) > 0.8]
        if transformation_types:
            return max(set(transformation_types), key=transformation_types.count)
        return "unknown"
    
    @debug_panel
    def _update_pattern_knowledge(self, analysis: Dict[str, Any]):
        """Update knowledge graph with new pattern information"""
        # Add pattern to knowledge graph
        pattern_info = {
            'type': analysis['transformation_type'],
            'causal_relations': analysis['causal_relations'],
            'verified_hypotheses': analysis['verified_hypotheses']
        }
        self.grid_patterns.update_knowledge_graph(
            ['grid_pattern', analysis['transformation_type']],
            str(pattern_info)
        )
        
    @debug_panel
    def _update_function_knowledge(self, functions: List[Dict[str, Any]]):
        """Update knowledge graph with discovered function information"""
        for func in functions:
            self.knowledge_manager.update_knowledge_graph(
                ['grid_function', func['name']],
                str(func)
            )

def run():
    try:
        agent = ARCAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in ARCAgent: {str(e)}")
        console.print(f"An error occurred: {str(e)}", style="bold red")

def main():
    run()

if __name__ == "__main__":
    main()