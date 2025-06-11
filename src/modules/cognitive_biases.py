"""
Core implementations of fundamental cognitive biases for ARC challenge
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass

@dataclass
class Component:
    """Represents a connected component in the grid"""
    pixels: Set[Tuple[int, int]]  # Set of (x,y) coordinates
    color: int
    bbox: Tuple[int, int, int, int]  # (min_x, max_x, min_y, max_y)
    size: int
    density: float
    aspect_ratio: float

class CognitiveBiases:
    def __init__(self, min_component_size: int = 4):
        self.min_component_size = min_component_size
    
    def find_connected_components(self, grid: np.ndarray) -> List[Component]:
        """Find all connected components in the grid using flood fill"""
        height, width = grid.shape
        visited = set()
        components = []
        
        def flood_fill(x: int, y: int, color: int) -> Set[Tuple[int, int]]:
            if (x, y) in visited:
                return set()
            if x < 0 or x >= height or y < 0 or y >= width:
                return set()
            if grid[x, y] != color:
                return set()
                
            pixels = {(x, y)}
            visited.add((x, y))
            
            # Check all 4 directions
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                pixels |= flood_fill(x + dx, y + dy, color)
                
            return pixels

        for x in range(height):
            for y in range(width):
                if (x, y) not in visited and grid[x, y] != 0:  # Skip background
                    pixels = flood_fill(x, y, grid[x, y])
                    if len(pixels) >= self.min_component_size:
                        # Calculate bounding box
                        xs = [p[0] for p in pixels]
                        ys = [p[1] for p in pixels]
                        bbox = (min(xs), max(xs), min(ys), max(ys))
                        
                        # Calculate metrics
                        width = bbox[1] - bbox[0] + 1
                        height = bbox[3] - bbox[2] + 1
                        area = width * height
                        density = len(pixels) / area
                        aspect_ratio = width / height if height != 0 else 0
                        
                        components.append(Component(
                            pixels=pixels,
                            color=grid[x, y],
                            bbox=bbox,
                            size=len(pixels),
                            density=density,
                            aspect_ratio=aspect_ratio
                        ))
        
        return components

    def detect_size_bias(self, grid: np.ndarray) -> List[Dict]:
        """Detect components that show size-based patterns"""
        components = self.find_connected_components(grid)
        
        size_patterns = []
        for comp in components:
            pattern = {
                'type': 'size',
                'color': comp.color,
                'size': comp.size,
                'density': comp.density,
                'bbox': comp.bbox,
                'aspect_ratio': comp.aspect_ratio
            }
            size_patterns.append(pattern)
            
        return size_patterns
    
    def detect_preservation_bias(self, input_grid: np.ndarray, 
                               output_grid: np.ndarray) -> List[Dict]:
        """Detect preserved boundaries and containment relationships"""
        input_components = self.find_connected_components(input_grid)
        output_components = self.find_connected_components(output_grid)
        
        preserved = []
        for in_comp in input_components:
            for out_comp in output_components:
                if (in_comp.color == out_comp.color and 
                    abs(in_comp.size - out_comp.size) / max(in_comp.size, out_comp.size) < 0.2):
                    preserved.append({
                        'type': 'preservation',
                        'color': in_comp.color,
                        'input_bbox': in_comp.bbox,
                        'output_bbox': out_comp.bbox,
                        'size': in_comp.size,
                        'confidence': 1 - abs(in_comp.size - out_comp.size) / max(in_comp.size, out_comp.size)
                    })
        return preserved
    
    def detect_movement_bias(self, input_grid: np.ndarray, 
                           output_grid: np.ndarray) -> List[Dict]:
        """Detect movement patterns between components"""
        input_components = self.find_connected_components(input_grid)
        output_components = self.find_connected_components(output_grid)
        
        movements = []
        for in_comp in input_components:
            for out_comp in output_components:
                if in_comp.color == out_comp.color and in_comp.size == out_comp.size:
                    # Calculate center points
                    in_center = ((in_comp.bbox[0] + in_comp.bbox[1]) / 2,
                               (in_comp.bbox[2] + in_comp.bbox[3]) / 2)
                    out_center = ((out_comp.bbox[0] + out_comp.bbox[1]) / 2,
                                (out_comp.bbox[2] + out_comp.bbox[3]) / 2)
                    
                    dx = out_center[0] - in_center[0]
                    dy = out_center[1] - in_center[1]
                    
                    if dx != 0 or dy != 0:
                        movements.append({
                            'type': 'movement',
                            'color': in_comp.color,
                            'size': in_comp.size,
                            'dx': dx,
                            'dy': dy,
                            'distance': (dx**2 + dy**2)**0.5
                        })
        return movements
    
    def detect_power_seeking_bias(self, input_grid: np.ndarray, 
                                output_grid: np.ndarray) -> List[Dict]:
        """Detect patterns related to territory control and expansion"""
        input_components = self.find_connected_components(input_grid)
        output_components = self.find_connected_components(output_grid)
        
        territory_patterns = []
        for in_comp in input_components:
            # Look for components that grew in size
            matching_output = [out for out in output_components 
                             if out.color == in_comp.color and out.size > in_comp.size]
            
            if matching_output:
                out_comp = max(matching_output, key=lambda x: x.size)
                growth = out_comp.size - in_comp.size
                
                pattern = {
                    'type': 'territory',
                    'color': in_comp.color,
                    'initial_size': in_comp.size,
                    'final_size': out_comp.size,
                    'growth': growth,
                    'growth_ratio': out_comp.size / in_comp.size
                }
                territory_patterns.append(pattern)
                
        return territory_patterns
    
    def detect_knowledge_seeking_bias(self, grid: np.ndarray) -> List[Dict]:
        """Detect patterns that suggest learning or information gathering"""
        components = self.find_connected_components(grid)
        
        # Look for components that form regular patterns
        patterns = []
        for comp in components:
            # Calculate distances between pixels
            pixels = list(comp.pixels)
            if len(pixels) < 2:
                continue
                
            distances = []
            for i in range(len(pixels)):
                for j in range(i + 1, len(pixels)):
                    dx = pixels[i][0] - pixels[j][0]
                    dy = pixels[i][1] - pixels[j][1]
                    distances.append((dx**2 + dy**2)**0.5)
                    
            # Look for regular spacing
            if distances:
                mean_dist = sum(distances) / len(distances)
                std_dist = np.std(distances)
                
                if std_dist / mean_dist < 0.2:  # Regular spacing detected
                    patterns.append({
                        'type': 'knowledge',
                        'color': comp.color,
                        'size': comp.size,
                        'regularity': 1 - (std_dist / mean_dist),
                        'mean_spacing': mean_dist
                    })
                    
        return patterns