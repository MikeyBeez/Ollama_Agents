# Using Ollama Agents for ARC Challenges

## Quick Start
The core functionality for solving ARC challenges is in `/users/bard/mcp/arc_testing/`.

### Core Functions
- `ValueMapDetector`: Detects value transformations
  ```python
  detector = ValueMapDetector(pattern_detector=GeometricPatternDetector())
  transforms = detector.detect(before_grid, after_grid)
  ```

### Key Paths
```
/users/bard/mcp/arc_testing/     # Main ARC testing directory
/users/bard/mcp/arc_testing/tests/  # Test cases
```

### Value Mapping Conventions
1. Simple transformations: When values map consistently (e.g., 1->3 always)
2. Pattern transformations: Only needed when mappings are inconsistent

### Test Requirements
- Transform outputs must match expected format:
  ```python
  {
    'type': 'value_map',
    'scope': 'global',  # or 'pattern'
    'mapping': {1: 3, 2: 4},  # value mappings
    'confidence': 1.0
  }
  ```

### Best Practices
1. Check for simple consistent mappings first
2. Only use pattern detection if inconsistencies found
3. Format output as required by tests

## Common Testing Patterns
```python
# Simple consistency check
mappings = {}
for i in range(before.shape[0]):
    for j in range(before.shape[1]):
        value = before[i,j]
        if value == 0:  # Skip background
            continue
        new_value = after[i,j]
        if value not in mappings:
            mappings[value] = new_value
        elif new_value != mappings[value]:
            # Found inconsistency
            return []
```

## Tips
1. Don't overcomplicate simple transformations
2. Only use pattern detection when needed
3. Focus on value consistency first