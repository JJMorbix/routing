import numpy as np

# Classe che rappresenta un nodo nella rete
class Node:
    def __init__(self, name):
        self.name = name  # Nome del nodo
        self.neighbors = {}  # Dizionario dei vicini e dei relativi costi
        # Tabella di routing inizializzata con se stesso: costo 0
        self.routing_table = {name: {"cost": 0, "next_hop": None}}  
    
    # Metodo per aggiungere un vicino con un costo specificato
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor] = {"cost": cost, "next_hop": neighbor}
    
    # Metodo per aggiornare la tabella di routing basandosi sui dati dei vicini
    def update_routing_table(self, neighbor_table, neighbor_name):
        updated = False  # Flag per rilevare se la tabella è stata modificata
        for dest, data in neighbor_table.items():
            if dest == self.name:  # Ignora l'aggiornamento verso se stesso
                continue
            # Calcolo del nuovo costo verso la destinazione
            new_cost = self.neighbors[neighbor_name] + data["cost"]
            # Aggiornamento della tabella se il nuovo costo è più basso
            if dest not in self.routing_table or new_cost < self.routing_table[dest]["cost"]:
                self.routing_table[dest] = {"cost": new_cost, "next_hop": neighbor_name}
                updated = True
        return updated
    
    # Metodo per stampare la tabella di routing del nodo
    def print_routing_table(self):
        print(f"Routing Table for Node {self.name}:")
        print("Destination\tCost\tNext Hop")
        for dest, data in self.routing_table.items():
            if dest == self.name:  # Non stampare il costo verso se stesso
                continue
            print(f"{dest}\t\t{data['cost']}\t{data['next_hop']}")
        print("-" * 40)

# Classe che rappresenta l'intera rete
class Network:
    def __init__(self):
        self.nodes = {}  # Dizionario dei nodi nella rete
    
    # Metodo per aggiungere un nuovo nodo alla rete
    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
    
    # Metodo per aggiungere un collegamento bidirezionale tra due nodi
    def add_link(self, node1, node2, cost):
        self.nodes[node1].add_neighbor(node2, cost)
        self.nodes[node2].add_neighbor(node1, cost)
    
    # Simulazione del processo di convergenza utilizzando l'algoritmo Distance Vector
    def simulate_routing(self):
        converged = False  # Flag per rilevare la convergenza
        while not converged:
            converged = True
            for node_name, node in self.nodes.items():
                for neighbor_name in node.neighbors:
                    neighbor = self.nodes[neighbor_name]
                    # Se un nodo aggiorna la sua tabella, la rete non è ancora convergente
                    if node.update_routing_table(neighbor.routing_table, neighbor_name):
                        converged = False
    
    # Metodo per stampare tutte le tabelle di routing nella rete
    def print_routing_tables(self):
        for node in self.nodes.values():
            node.print_routing_table()

# Blocco principale di esecuzione dello script
if __name__ == "__main__":
    # Creazione di una rete e aggiunta dei nodi
    network = Network()
    network.add_node("A")
    network.add_node("B")
    network.add_node("C")
    network.add_node("D")

    # Aggiunta di collegamenti tra i nodi con costi iniziali
    network.add_link("A", "B", 1)
    network.add_link("A", "C", 4)
    network.add_link("B", "C", 2)
    network.add_link("C", "D", 1)

    # Stampa delle tabelle di routing iniziali
    print("Initial Routing Tables:")
    network.print_routing_tables()

    # Simulazione della convergenza delle tabelle di routing
    network.simulate_routing()

    # Stampa delle tabelle di routing finali dopo la convergenza
    print("\n\nFinal Routing Tables After Convergence:")
    network.print_routing_tables()
