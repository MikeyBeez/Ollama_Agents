"""
Test script for cognitive bias-based ARC analysis with evaluation metrics
"""

import os
import sys
from pathlib import Path
import json
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import track

from modules.arc_analyzer import ARCAnalyzer

console = Console()

def predict_output(input_grid: np.ndarray, patterns: dict) -> np.ndarray:
    """Predict output grid based on detected patterns"""
    output = np.zeros_like(input_grid)
    
    # Apply patterns in priority order
    if 'preservation' in patterns:
        # Copy preserved components
        for pattern in patterns['preservation']:
            color = pattern['color']
            mask = input_grid == color
            output[mask] = color
            
    if 'movement' in patterns:
        # Apply movements
        for pattern in patterns['movement']:
            color = pattern['color']
            dx = int(round(pattern['dx']))
            dy = int(round(pattern['dy']))
            mask = input_grid == color
            if dx > 0:
                mask = np.roll(mask, dx, axis=0)
            elif dx < 0:
                mask = np.roll(mask, -dx, axis=0)
            if dy > 0:
                mask = np.roll(mask, dy, axis=1)
            elif dy < 0:
                mask = np.roll(mask, -dy, axis=1)
            output[mask] = color
            
    if 'territory' in patterns:
        # Apply territory expansions
        for pattern in patterns['territory']:
            color = pattern['color']
            growth_ratio = pattern['growth_ratio']
            mask = input_grid == color
            # Simple dilation based on growth ratio
            from scipy.ndimage import binary_dilation
            iterations = int(round(growth_ratio - 1))
            if iterations > 0:
                dilated = binary_dilation(mask, iterations=iterations)
                output[dilated] = color
                
    return output

def evaluate_prediction(predicted: np.ndarray, actual: np.ndarray) -> float:
    """Calculate prediction accuracy"""
    return np.mean(predicted == actual)

def analyze_arc_tasks(data_dir: str):
    """Analyze all ARC tasks in the given directory"""
    analyzer = ARCAnalyzer()
    
    # Find all task files
    task_files = list(Path(data_dir).glob('*.json'))
    console.print(f"Found {len(task_files)} task files")
    
    # Track bias statistics and accuracies
    bias_stats = {
        'size': 0,
        'preservation': 0,
        'movement': 0,
        'territory': 0,
        'knowledge': 0
    }
    
    total_accuracy = 0
    solved_count = 0
    
    # Create results table
    table = Table(title="ARC Task Analysis Results")
    table.add_column("Task ID", style="cyan")
    table.add_column("Primary Biases", style="green")
    table.add_column("Train Accuracy", justify="right")
    table.add_column("Test Accuracy", justify="right")
    table.add_column("Status", style="bold")
    
    for task_file in track(task_files, description="Analyzing tasks..."):
        # Load task data
        with open(task_file, 'r') as f:
            task_data = json.load(f)
            
        # Analyze training examples
        analysis = analyzer.analyze_task(task_file)
        consistent_biases = analysis['combined_analysis']['consistent_biases']
        
        # Update bias statistics
        for bias in consistent_biases:
            bias_stats[bias] += 1
            
        # Calculate training accuracy
        train_accuracies = []
        for i, pair in enumerate(task_data['train']):
            input_grid = np.array(pair['input'])
            actual_output = np.array(pair['output'])
            
            # Use patterns from other training examples
            other_analyses = analysis['train_analyses'][:i] + analysis['train_analyses'][i+1:]
            if other_analyses:
                patterns = analyzer.combine_analyses(other_analyses)['combined_patterns']
                predicted_output = predict_output(input_grid, patterns)
                accuracy = evaluate_prediction(predicted_output, actual_output)
                train_accuracies.append(accuracy)
        
        train_accuracy = np.mean(train_accuracies) if train_accuracies else 0
        
        # Calculate test accuracy
        test_accuracies = []
        for pair in task_data['test']:
            input_grid = np.array(pair['input'])
            actual_output = np.array(pair['output'])
            
            # Use patterns from all training examples
            patterns = analysis['combined_analysis']['combined_patterns']
            predicted_output = predict_output(input_grid, patterns)
            accuracy = evaluate_prediction(predicted_output, actual_output)
            test_accuracies.append(accuracy)
            
        test_accuracy = np.mean(test_accuracies)
        total_accuracy += test_accuracy
        
        # Consider task solved if test accuracy > 0.95
        solved = test_accuracy > 0.95
        if solved:
            solved_count += 1
            
        # Add row to results table
        table.add_row(
            task_file.stem,
            ", ".join(consistent_biases),
            f"{train_accuracy:.2%}",
            f"{test_accuracy:.2%}",
            "SOLVED" if solved else "UNSOLVED"
        )
    
    # Print results
    console.print(table)
    
    # Print summary statistics
    console.print("\n=== Summary Statistics ===")
    console.print(f"Total tasks analyzed: {len(task_files)}")
    console.print(f"Tasks solved: {solved_count} ({solved_count/len(task_files):.1%})")
    console.print(f"Average accuracy: {total_accuracy/len(task_files):.1%}")
    console.print("\nBias Occurrence Rates:")
    for bias, count in bias_stats.items():
        console.print(f"- {bias}: {count/len(task_files):.1%}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_arc_biases.py <arc_data_dir>")
        sys.exit(1)
        
    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: {data_dir} is not a directory")
        sys.exit(1)
        
    analyze_arc_tasks(data_dir)

if __name__ == "__main__":
    main()