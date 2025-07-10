import json
import csv
import numpy as np
from bs4 import BeautifulSoup
from IPython.display import HTML, display

def create_csv_from_json(relations_file, nodes_file, output_file="output.csv", embedding_dim=100, epochs=500, learning_rate=0.1, margin=1.0):
    """
    Reads relations and nodes from JSON files, and creates a CSV file
    with columns "start node", "relation", "end node", "start node embedding", "relation embedding", "end node embedding".
    Includes a simplified TransE-like embedding training.

    Args:
        relations_file (str): Path to the relations JSON file.
        nodes_file (str): Path to the nodes JSON file.
        output_file (str, optional): Path to the output CSV file.
            Defaults to "output.csv".
        embedding_dim (int, optional): The dimension of the node and relation embeddings.
            Defaults to 100.
        epochs (int, optional): The number of training epochs.
            Defaults to 100.
        learning_rate (float, optional): The learning rate for the optimization.
            Defaults to 0.01.
        margin (float, optional): The margin used in the TransE loss function.
            Defaults to 1.0.
    """
    try:
        with open(relations_file, 'r', encoding='utf-8-sig') as f_relations, \
             open(nodes_file, 'r', encoding='utf-8-sig') as f_nodes:
            relations_data = json.load(f_relations)
            nodes_data = json.load(f_nodes)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return

    # 1. Create a dictionary to store node information using elementId as key for faster lookup
    node_dict = {node['n']['elementId']: node['n'] for node in nodes_data}

    # 2. Create a set of unique node IDs and relation types
    unique_node_ids = set()
    unique_relation_types = set()
    for relation_item in relations_data:
        relation = relation_item['r']
        unique_node_ids.add(relation['startNodeElementId'])
        unique_node_ids.add(relation['endNodeElementId'])
        unique_relation_types.add(relation['type'])

    # 3. Create mappings from node IDs and relation types to indices
    node_id_to_index = {node_id: i for i, node_id in enumerate(unique_node_ids)}
    relation_type_to_index = {relation_type: i for i, relation_type in enumerate(unique_relation_types)}
    index_to_node_id = {i: node_id for node_id, i in node_id_to_index.items()} #inverse mapping

    # 4. Initialize node and relation embeddings (TransE)
    node_embeddings = np.random.rand(len(unique_node_ids), embedding_dim)
    relation_embeddings = np.random.rand(len(unique_relation_types), embedding_dim)

    # 5. Training loop
    for epoch in range(epochs):
        total_loss = 0
        for relation_item in relations_data:
            relation = relation_item['r']
            start_node_element_id = relation['startNodeElementId']
            end_node_element_id = relation['endNodeElementId']
            relation_type = relation['type']

            # Get indices
            start_node_index = node_id_to_index[start_node_element_id]
            end_node_index = node_id_to_index[end_node_element_id]
            relation_type_index = relation_type_to_index[relation_type]

            # Get embeddings
            start_node_embedding = node_embeddings[start_node_index]
            end_node_embedding = node_embeddings[end_node_index]
            relation_embedding = relation_embeddings[relation_type_index]

            # Calculate the TransE distance
            distance = np.linalg.norm(start_node_embedding + relation_embedding - end_node_embedding)

            # Generate a corrupted triple for negative sampling
            corrupted_end_node_index = np.random.randint(len(unique_node_ids))
            while corrupted_end_node_index == end_node_index:
                corrupted_end_node_index = np.random.randint(len(unique_node_ids))
            corrupted_end_node_embedding = node_embeddings[corrupted_end_node_index]
            corrupted_distance = np.linalg.norm(start_node_embedding + relation_embedding - corrupted_end_node_embedding)

            # Calculate the TransE loss
            loss = max(0, margin + distance - corrupted_distance)
            total_loss += loss

            # Update embeddings (simplified gradient descent)
            if loss > 0:
                grad_start = 2 * (start_node_embedding + relation_embedding - end_node_embedding)
                grad_relation = 2 * (start_node_embedding + relation_embedding - end_node_embedding)
                grad_end = -2 * (start_node_embedding + relation_embedding - end_node_embedding)
                grad_corrupted_end = 2 * (start_node_embedding + relation_embedding - corrupted_end_node_embedding)

                node_embeddings[start_node_index] -= learning_rate * grad_start
                relation_embeddings[relation_type_index] -= learning_rate * grad_relation
                node_embeddings[end_node_index] -= learning_rate * grad_end
                node_embeddings[corrupted_end_node_index] -= learning_rate * grad_corrupted_end

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

    # 6. Prepare data for CSV
    csv_data = []
    for relation_item in relations_data:
        relation = relation_item['r']
        start_node_element_id = relation['startNodeElementId']
        end_node_element_id = relation['endNodeElementId']
        relation_type = relation['type']

        # Check if start and end nodes exist
        if start_node_element_id in node_dict and end_node_element_id in node_dict:
            start_node_name = node_dict[start_node_element_id]['properties'].get('name', 'Unknown')
            end_node_name = node_dict[end_node_element_id]['properties'].get('name', 'Unknown')
            start_node_embedding = node_embeddings[node_id_to_index[start_node_element_id]].tolist()  # Get from trained embeddings
            relation_embedding = relation_embeddings[relation_type_to_index[relation_type]].tolist()      # Get from trained embeddings
            end_node_embedding = node_embeddings[node_id_to_index[end_node_element_id]].tolist()    # Get from trained embeddings

            csv_data.append({
                "start node": start_node_name,
                "relation": relation_type,
                "end node": end_node_name,
                "start node embedding": start_node_embedding,
                "relation embedding": relation_embedding,
                "end node embedding": end_node_embedding
            })
        else:
            print(f"Warning: Skipping relation with ID {relation['identity']} as start or end node was not found.")

    if not csv_data:
        print("No valid relations found to write to CSV.")
        return

    # 7. Write to CSV
    try:
        with open(output_file, 'w', newline='') as csvfile:
            #  Include the new embedding columns in the fieldnames
            fieldnames = ["start node", "relation", "end node", "start node embedding", "relation embedding", "end node embedding"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"Successfully wrote data to {output_file}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    relations_file = 'relations.json'
    nodes_file = 'nodes.json'
    create_csv_from_json(relations_file, nodes_file)
