# src/modules/system_dynamics_helpers.py

import networkx as nx
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt

def create_system_graph(nodes: List[str], edges: List[Tuple[str, str, Dict[str, Any]]]) -> nx.DiGraph:
    """
    Create a directed graph representing the system.

    Args:
    nodes (List[str]): List of node names.
    edges (List[Tuple[str, str, Dict[str, Any]]]): List of edges with attributes.

    Returns:
    nx.DiGraph: A directed graph representing the system.
    """
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def identify_feedback_loops(G: nx.DiGraph) -> List[List[str]]:
    """
    Identify feedback loops in the system.

    Args:
    G (nx.DiGraph): The system graph.

    Returns:
    List[List[str]]: List of feedback loops (each loop is a list of node names).
    """
    return list(nx.simple_cycles(G))

def calculate_centrality(G: nx.DiGraph) -> Dict[str, float]:
    """
    Calculate centrality measures for nodes in the system.

    Args:
    G (nx.DiGraph): The system graph.

    Returns:
    Dict[str, float]: Dictionary of node centralities.
    """
    return nx.eigenvector_centrality(G)

def identify_bottlenecks(G: nx.DiGraph) -> List[str]:
    """
    Identify potential bottlenecks in the system.

    Args:
    G (nx.DiGraph): The system graph.

    Returns:
    List[str]: List of potential bottleneck nodes.
    """
    betweenness = nx.betweenness_centrality(G)
    threshold = sum(betweenness.values()) / len(betweenness)
    return [node for node, score in betweenness.items() if score > threshold]

def simulate_system_behavior(G: nx.DiGraph, time_steps: int, initial_state: Dict[str, float]) -> Dict[str, List[float]]:
    """
    Simulate system behavior over time (simple linear model).

    Args:
    G (nx.DiGraph): The system graph.
    time_steps (int): Number of time steps to simulate.
    initial_state (Dict[str, float]): Initial state of each node.

    Returns:
    Dict[str, List[float]]: Time series of each node's state.
    """
    state = initial_state.copy()
    time_series = {node: [state[node]] for node in G.nodes()}

    for _ in range(time_steps):
        new_state = state.copy()
        for node in G.nodes():
            incoming = sum(state[pred] * G[pred][node].get('weight', 1) for pred in G.predecessors(node))
            new_state[node] = 0.5 * state[node] + 0.5 * incoming
        state = new_state
        for node in G.nodes():
            time_series[node].append(state[node])

    return time_series

def visualize_system(G: nx.DiGraph, filename: str = 'system_visualization.png'):
    """
    Visualize the system graph.

    Args:
    G (nx.DiGraph): The system graph.
    filename (str): Output file name for the visualization.
    """
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=500, arrowsize=20, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("System Dynamics Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def analyze_system_dynamics(nodes: List[str], edges: List[Tuple[str, str, Dict[str, Any]]],
                            initial_state: Dict[str, float], time_steps: int) -> Dict[str, Any]:
    """
    Analyze system dynamics.

    Args:
    nodes (List[str]): List of node names.
    edges (List[Tuple[str, str, Dict[str, Any]]]): List of edges with attributes.
    initial_state (Dict[str, float]): Initial state of each node.
    time_steps (int): Number of time steps to simulate.

    Returns:
    Dict[str, Any]: Analysis results.
    """
    G = create_system_graph(nodes, edges)
    feedback_loops = identify_feedback_loops(G)
    centrality = calculate_centrality(G)
    bottlenecks = identify_bottlenecks(G)
    time_series = simulate_system_behavior(G, time_steps, initial_state)
    visualize_system(G)

    return {
        "feedback_loops": feedback_loops,
        "centrality": centrality,
        "bottlenecks": bottlenecks,
        "time_series": time_series
    }
