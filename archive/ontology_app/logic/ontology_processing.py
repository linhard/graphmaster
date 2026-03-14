import os
import csv
from rdflib import Graph


def list_ontologies(folder_path):
    """List all .ttl ontology files in the folder."""
    if not os.path.exists(folder_path):
        return []
    return [file for file in os.listdir(folder_path) if file.endswith(".ttl")]


def extract_tokens(file_path):
    """Extract tokens (Subjects, Predicates, Objects) from a .ttl ontology file."""
    graph = Graph()
    graph.parse(file_path, format="ttl")

    tokens = []
    for subject, predicate, obj in graph:
        tokens.append({"type": "Subject", "token": str(subject), "source": "Triple"})
        tokens.append({"type": "Predicate", "token": str(predicate), "source": "Triple"})
        tokens.append({"type": "Object", "token": str(obj), "source": "Triple"})

    return tokens


def vectorize_tokens(tokens, progress_bar):
    """Simulate token vectorization with progress."""
    import time
    vectors = []
    for i, token in enumerate(tokens):
        time.sleep(0.1)  # Simulate processing
        vectors.append([token, i * 0.1])  # Dummy vector
        progress_bar.setValue(int((i + 1) / len(tokens) * 100))
    return vectors


def save_to_csv(tokens, vectors, file_path):
    """Save tokens and their vectors to a CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Token", "Vector"])
        for token, vector in zip(tokens, vectors):
            writer.writerow([token, vector])
