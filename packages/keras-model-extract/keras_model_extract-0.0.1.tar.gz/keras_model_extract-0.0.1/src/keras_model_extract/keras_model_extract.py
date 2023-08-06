class Node:
    """
    Represents a node (layer) in the model.

    Properties:
        - children: children nodes (sub-layers)
        - parent_names: unique names of parent nodes
        - shape: layer output shape
        - name: unique layer name (from TF/Keras)
        - __layer: reference to the instance of the layer (if `include_layer_ref` is `True`)
    """

    def __init__(self, include_layer_ref=False):
        self.children = []
        self.parent_names = []
        self.shape = None
        self.name = None
        self.include_layer_ref = include_layer_ref
        if include_layer_ref:
            self.__layer = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


# https://github.com/tensorflow/tensorflow/blob/a4dfb8d1a71385bd6d122e4f27f86dcebb96712d/tensorflow/python/keras/utils/layer_utils.py#L213
# helper function to build dependency graph


def __get_layer_summary_with_connections(layer, relevant_nodes):
    info = {}
    connections = []
    for node in layer._inbound_nodes:
        if relevant_nodes and node not in relevant_nodes:
            # node is not part of the current network
            continue

        for inbound_layer, node_index, tensor_index, _ in node.iterate_inbound():
            connections.append(inbound_layer.name)

    name = layer.name
    info["type"] = layer.__class__.__name__
    info["parents"] = connections

    return info


def iterate(node, func):
    """
    Helper function to iterate through model tree.

    At every step it applies `func` to the current node (layer).

    Paramter `node` is the starting layer/node.
    """

    def __iterate(t):
        func(t)
        for c in t.children:
            __iterate(c)

    __iterate(node)


def copy_model_tree(model, include_layer_ref=False):
    """
    Main conversion function. Receives Keras/TF model returns
    a dictionary of `Node(s)` where keys are Node names.

    Parameter include_layer_ref controls whether to save references
    to Keras/TF layers which makes the tree operations slower, so only
    use when necessary.
    """
    nodes = dict()

    relevant_nodes = []
    for v in model._nodes_by_depth.values():
        relevant_nodes += v

    for layer in model.layers:  # create nodes
        n = Node()
        n.name = layer.name
        n.shape = layer.get_output_shape_at(0)
        if include_layer_ref:
            n.__layer = layer
        nodes[layer.name] = n

    for layer in model.layers:  # create links
        parents = __get_layer_summary_with_connections(layer, relevant_nodes)
        nodes[layer.name].parent_names = parents["parents"]
        for parent in parents["parents"]:
            nodes[parent].children.append(nodes[layer.name])

    return nodes
