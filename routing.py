import numpy as np

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = {name: {"cost": 0, "next_hop": None}}  # Il costo per raggiungere se stessi è 0.
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor] = {"cost": cost, "next_hop": neighbor}
    
    def update_routing_table(self, neighbor_table, neighbor_name):
        updated = False
        for dest, data in neighbor_table.items():
            if dest == self.name:  # Ignorare il costo verso se stessi.
                continue
            new_cost = self.neighbors[neighbor_name] + data["cost"]
            if dest not in self.routing_table or new_cost < self.routing_table[dest]["cost"]:
                self.routing_table[dest] = {"cost": new_cost, "next_hop": neighbor_name}
                updated = True
        return updated
    
    def print_routing_table(self):
        print(f"Routing Table for Node {self.name}:")
        print("Destination\tCost\tNext Hop")
        for dest, data in self.routing_table.items():
            if dest == self.name:  # Non stampare la voce verso se stessi.
                continue
            print(f"{dest}\t\t{data['cost']}\t{data['next_hop']}")
        print("-" * 40)

class Network:
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
    
    def add_link(self, node1, node2, cost):
        self.nodes[node1].add_neighbor(node2, cost)
        self.nodes[node2].add_neighbor(node1, cost)
    
    def simulate_routing(self):
        converged = False
        while not converged:
            converged = True
            for node_name, node in self.nodes.items():
                for neighbor_name in node.neighbors:
                    neighbor = self.nodes[neighbor_name]
                    if node.update_routing_table(neighbor.routing_table, neighbor_name):
                        converged = False
    
    def print_routing_tables(self):
        for node in self.nodes.values():
            node.print_routing_table()

if __name__ == "__main__":
    network = Network()
    network.add_node("A")
    network.add_node("B")
    network.add_node("C")
    network.add_node("D")

    network.add_link("A", "B", 1)
    network.add_link("A", "C", 4)
    network.add_link("B", "C", 2)
    network.add_link("C", "D", 1)

    print("Initial Routing Tables:")
    network.print_routing_tables()

    network.simulate_routing()

    print("\n\nFinal Routing Tables After Convergence:")
    network.print_routing_tables()