import networkx as nx
import matplotlib.pyplot as plt


class CircuitGraph:
    def __init__(self, circuit):
        self.circuit = circuit
        self.vertices = self.circuit.get_vertices()
        self.graph = nx.DiGraph(self.vertices.keys())

    def draw_topological_graph(self):
        labels = {node: node for node, _ in self.circuit.wires.items()}
        colors = self.circuit.get_colors()
        print(colors)
        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            print(nodes)
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

        # Computing the position of each layer for circuit leveling
        pos = nx.multipartite_layout(self.graph, subset_key="layer")

        unique_colors = list(set(colors.values()))  # Unique colors used
        legend_labels = ["1" if color == "green" else "0" for color in unique_colors]

        # Create a custom legend for your color-coded nodes
        legend_handles = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=label,
                markerfacecolor=color,
                markersize=10,
            )
            for color, label in zip(unique_colors, legend_labels)
        ]

        fig, ax = plt.subplots()
        nx.draw_networkx(
            self.graph,
            pos=pos,
            ax=ax,
            with_labels=True,
            labels=labels,
            node_color=[colors[node] for node in self.graph.nodes()],
        )
        nx.draw_networkx_edge_labels(
            self.graph, pos=pos, ax=ax, edge_labels=self.vertices
        )

        ax.legend(
            handles=legend_handles,
            labels=legend_labels,
            title="Logic Value",
            loc="upper right",
        )
        ax.set_title(f"Graph of the {self.circuit.circuitName} circuit")
        fig.tight_layout()
        plt.show()
