import json
import csv

def create_csv_from_json(relations_file, nodes_file, output_file="output.csv"):
    """
    Reads relations and nodes from JSON files, and creates a CSV file
    with columns "start node", "relation", and "end node".

    Args:
        relations_file (str): Path to the relations JSON file.
        nodes_file (str): Path to the nodes JSON file.
        output_file (str, optional): Path to the output CSV file.
            Defaults to "output.csv".
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

    # Create a dictionary to store node information using elementId as key for faster lookup
    node_dict = {node['n']['elementId']: node['n'] for node in nodes_data}

    # Prepare data for CSV
    csv_data = []
    for relation_item in relations_data:
        relation = relation_item['r']
        start_node_element_id = relation['startNodeElementId']
        end_node_element_id = relation['endNodeElementId']

        # Check if start and end nodes exist
        if start_node_element_id in node_dict and end_node_element_id in node_dict:
            start_node_name = node_dict[start_node_element_id]['properties'].get('name', 'Unknown')  #handles the cases where a node doesn't have a name.
            end_node_name = node_dict[end_node_element_id]['properties'].get('name', 'Unknown')    #handles the cases where a node doesn't have a name.
            csv_data.append({
                "start node": start_node_name,
                "relation": relation['type'],
                "end node": end_node_name
            })
        else:
            print(f"Warning: Skipping relation with ID {relation['identity']} as start or end node was not found.")

    if not csv_data:
        print("No valid relations found to write to CSV.")
        return

    # Write to CSV
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["start node", "relation", "end node"])
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"Successfully wrote data to {output_file}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    relations_file = '/content/relations.json'  # Replace with your actual file name
    nodes_file = '/content/nodes.json'      # Replace with your actual file name
    create_csv_from_json(relations_file, nodes_file)
