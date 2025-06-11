"""
ARC puzzle analyzer using cognitive biases
"""

import numpy as np
from typing import Dict, List, Optional
import json
from pathlib import Path
from .cognitive_biases import CognitiveBiases

class ARCAnalyzer:
    def __init__(self, min_component_size: int = 4):
        self.biases = CognitiveBiases(min_component_size)
        
    def analyze_task(self, task_file: str) -> Dict:
        """Analyze a single ARC task file"""
        # Load task data
        with open(task_file, 'r') as f:
            task_data = json.load(f)
            
        # Analyze each train/test pair
        train_analyses = []
        for pair in task_data['train']:
            analysis = self.analyze_pair(
                np.array(pair['input']),
                np.array(pair['output'])
            )
            train_analyses.append(analysis)
            
        # Combine analyses to find consistent patterns
        combined_analysis = self.combine_analyses(train_analyses)
        
        return {
            'task_id': Path(task_file).stem,
            'train_analyses': train_analyses,
            'combined_analysis': combined_analysis
        }
        
    def analyze_pair(self, input_grid: np.ndarray, 
                    output_grid: np.ndarray) -> Dict:
        """Analyze transformation between input/output pair"""
        analysis = {
            'size_patterns': self.biases.detect_size_bias(input_grid),
            'preservation_patterns': self.biases.detect_preservation_bias(input_grid, output_grid),
            'movement_patterns': self.biases.detect_movement_bias(input_grid, output_grid),
            'territory_patterns': self.biases.detect_power_seeking_bias(input_grid, output_grid),
            'knowledge_patterns': self.biases.detect_knowledge_seeking_bias(output_grid)
        }
        
        # Calculate confidence scores for each bias type
        confidence_scores = {
            'size': len(analysis['size_patterns']) / max(1, np.sum(input_grid != 0)),
            'preservation': len(analysis['preservation_patterns']) / max(1, len(self.biases.find_connected_components(input_grid))),
            'movement': len(analysis['movement_patterns']) / max(1, len(self.biases.find_connected_components(input_grid))),
            'territory': len(analysis['territory_patterns']) / max(1, len(self.biases.find_connected_components(input_grid))),
            'knowledge': len(analysis['knowledge_patterns']) / max(1, len(self.biases.find_connected_components(output_grid)))
        }
        
        analysis['confidence_scores'] = confidence_scores
        
        # Determine primary biases (those with confidence > 0.5)
        primary_biases = [bias for bias, score in confidence_scores.items() 
                         if score > 0.5]
        analysis['primary_biases'] = primary_biases
        
        return analysis
    
    def combine_analyses(self, analyses: List[Dict]) -> Dict:
        """Combine multiple analyses to find consistent patterns"""
        if not analyses:
            return {}
            
        # Count occurrences of each bias type
        bias_counts = {}
        for analysis in analyses:
            for bias in analysis['primary_biases']:
                bias_counts[bias] = bias_counts.get(bias, 0) + 1
                
        # Calculate consistency scores
        n_examples = len(analyses)
        consistency_scores = {
            bias: count / n_examples 
            for bias, count in bias_counts.items()
        }
        
        # Identify consistent patterns (appear in > 75% of examples)
        consistent_biases = [
            bias for bias, score in consistency_scores.items()
            if score > 0.75
        ]
        
        # Combine pattern details for consistent biases
        combined_patterns = {}
        for bias in consistent_biases:
            patterns = []
            for analysis in analyses:
                if bias in analysis['primary_biases']:
                    patterns.extend(analysis[f'{bias}_patterns'])
            combined_patterns[bias] = patterns
            
        return {
            'consistency_scores': consistency_scores,
            'consistent_biases': consistent_biases,
            'combined_patterns': combined_patterns
        }