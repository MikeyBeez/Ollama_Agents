# src/modules/helper_pattern_identification.py

import numpy as np
from typing import List, Dict, Any, Union
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller

def identify_numerical_patterns(data: List[float]) -> Dict[str, Any]:
    """
    Identify patterns in numerical data.

    Args:
    data (List[float]): List of numerical values.

    Returns:
    Dict[str, Any]: Dictionary containing identified patterns.
    """
    np_data = np.array(data)
    patterns = {
        "mean": np.mean(np_data),
        "median": np.median(np_data),
        "std_dev": np.std(np_data),
        "skewness": stats.skew(np_data),
        "kurtosis": stats.kurtosis(np_data),
        "trend": "increasing" if np.polyfit(range(len(data)), data, 1)[0] > 0 else "decreasing"
    }

    if len(data) >= 8:
        patterns["is_normal_distribution"] = stats.normaltest(np_data)[1] > 0.05
    else:
        patterns["is_normal_distribution"] = "Insufficient data for normality test"

    return patterns

def identify_sequence_patterns(sequence: List[Any]) -> Dict[str, Any]:
    """
    Identify patterns in a sequence of items.

    Args:
    sequence (List[Any]): List of items.

    Returns:
    Dict[str, Any]: Dictionary containing identified patterns.
    """
    return {
        "length": len(sequence),
        "unique_items": len(set(sequence)),
        "most_common": max(set(sequence), key=sequence.count),
        "has_duplicates": len(sequence) != len(set(sequence)),
        "is_sorted": all(sequence[i] <= sequence[i+1] for i in range(len(sequence)-1)),
        "is_palindrome": sequence == sequence[::-1]
    }

def identify_time_series_patterns(time_series: List[float]) -> Dict[str, Any]:
    """
    Identify patterns in time series data.

    Args:
    time_series (List[float]): List of time series values.

    Returns:
    Dict[str, Any]: Dictionary containing identified patterns.
    """
    np_series = np.array(time_series)
    patterns = {
        "trend": "increasing" if np.polyfit(range(len(time_series)), time_series, 1)[0] > 0 else "decreasing",
        "seasonality": "detected" if np.abs(np.fft.fft(np_series)[1:].max()) > len(np_series)/2 else "not detected",
        "autocorrelation": np.correlate(np_series, np_series, mode='full')[len(np_series):].max()
    }

    if len(time_series) > 3:  # adfuller requires more than 3 samples
        patterns["stationarity"] = "stationary" if adfuller(np_series)[1] < 0.05 else "non-stationary"
    else:
        patterns["stationarity"] = "Insufficient data for stationarity test"

    return patterns

def identify_clusters(data: List[List[float]], n_clusters: int = 2) -> Dict[str, Any]:
    """
    Identify clusters in multidimensional data.

    Args:
    data (List[List[float]]): List of data points.
    n_clusters (int): Number of clusters to identify.

    Returns:
    Dict[str, Any]: Dictionary containing identified clusters.
    """
    np_data = np.array(data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(np_data)
    return {
        "n_clusters": n_clusters,
        "cluster_centers": kmeans.cluster_centers_.tolist(),
        "labels": kmeans.labels_.tolist(),
        "inertia": kmeans.inertia_
    }

def identify_dimensional_patterns(data: List[List[float]], n_components: int = 2) -> Dict[str, Any]:
    """
    Identify patterns in high-dimensional data using PCA.

    Args:
    data (List[List[float]]): List of high-dimensional data points.
    n_components (int): Number of principal components to compute.

    Returns:
    Dict[str, Any]: Dictionary containing identified patterns.
    """
    np_data = np.array(data)
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(np_data)
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(normalized_data)
    return {
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "cumulative_explained_variance": np.cumsum(pca.explained_variance_ratio_).tolist(),
        "principal_components": pca.components_.tolist(),
        "transformed_data": pca_result.tolist()
    }

def identify_patterns(data: Union[List[float], List[Any], List[List[float]]]) -> Dict[str, Any]:
    """
    Identify patterns in the given data.

    Args:
    data (Union[List[float], List[Any], List[List[float]]]): Input data.

    Returns:
    Dict[str, Any]: Dictionary containing identified patterns.
    """
    if all(isinstance(x, (int, float)) for x in data):
        return {
            "data_type": "numerical",
            "numerical_patterns": identify_numerical_patterns(data),
            "time_series_patterns": identify_time_series_patterns(data)
        }
    elif all(isinstance(x, list) for x in data):
        return {
            "data_type": "multidimensional",
            "cluster_patterns": identify_clusters(data),
            "dimensional_patterns": identify_dimensional_patterns(data)
        }
    else:
        return {
            "data_type": "sequence",
            "sequence_patterns": identify_sequence_patterns(data)
        }
