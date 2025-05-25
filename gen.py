import random
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

def generate_positive_normal_int(mean=10, std_dev=2, round_result=False):
    val = -1
    while val <= 0:
        sample = random.normalvariate(mean, std_dev)
        val = round(sample) if round_result else int(sample)
    return val

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate random network topology")
    parser.add_argument('--nodes', type=int, default=15, help='Number of nodes')
    parser.add_argument('--links', type=int, default=3, help='Average number of links per node')
    parser.add_argument('--min_hop', type=int, default=3, help='Minimum hop count for non-direct connections')
    parser.add_argument('--delay', type=int, default=3, help='Mean delay in ms for each link')
    parser.add_argument('--std_dev', type=int, default=1, help='Standard deviation for delay and link generation')
    return parser.parse_args()

def generate_topology(args):
    topo = {f"r{i}": [] for i in range(1, args.nodes + 1)}

    for x in topo.keys():
        current_links = len(topo[x])
        excludes = {x}
        # Avoid duplicate links
        existing_links = {k for k, v in topo.items() if x in v}
        current_links += len(existing_links)
        needed_links = max(0, generate_positive_normal_int(args.links, args.std_dev) - current_links)

        while needed_links > 0:
            possible_links = [k for k in topo.keys() if k not in excludes and x not in topo[k]]
            if not possible_links:
                break
            link = random.choice(possible_links)
            topo[x].append(link)
            excludes.add(link)
            needed_links -= 1

    return topo

def export_topology(topo, args):
    all_nodes = set(topo.keys())
    for targets in topo.values():
        all_nodes.update(targets)

    lines = ["[nodes]"]
    for node in sorted(all_nodes):
        lines.append(f"{node}: _")

    lines.append("[links]")
    for src, dests in topo.items():
        for dest in dests:
            delay = generate_positive_normal_int(args.delay, args.std_dev)
            lines.append(f"{src}:{dest} delay={delay}ms")

    output_text = "\n".join(lines)
    with open("topology.txt", "w") as f:
        f.write(output_text)
    print(output_text)
    return output_text

def visualize_topology(topo):
    G = nx.Graph()
    for src, dests in topo.items():
        for dest in dests:
            G.add_edge(src, dest)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen',
            edge_color='gray', font_size=12, node_size=2000)
    plt.title("Topology")
    plt.tight_layout()
    plt.savefig("topology.jpg", format='jpg', dpi=300)  # Save as JPG
    # plt.show()
    return G

def report_non_direct_connections(G, min_hop, filename="prod-cons.txt"):
    lines = [f"Non-directly connected node pairs with hop count >= {min_hop}:\n"]
    
    for u, v in combinations(G.nodes, 2):
        if not G.has_edge(u, v):
            try:
                length = nx.shortest_path_length(G, source=u, target=v)
                if length >= min_hop:
                    line = f"{u} - {v} : {length} hops"
                    print(line)
                    lines.append(line)
            except nx.NetworkXNoPath:
                pass
    
    with open(filename, "w") as f:
        f.write("\n".join(lines))

def main():
    args = parse_arguments()
    topo = generate_topology(args)
    export_topology(topo, args)
    G = visualize_topology(topo)
    report_non_direct_connections(G, args.min_hop)

if __name__ == "__main__":
    main()