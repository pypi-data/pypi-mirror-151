# Keras Model Extract

This is a small utility library to access Keras/TensorFlow model's structure/tree and do stuff with it.

Currently there isn't a straight-forward way to do this without manually going through the model layers.

It currently supports:

- Model tree iteration (BFS-like)
- Accessing node parents, node children, node output type
- Accessing source layers

Node properties:

- `children`: children nodes (sub-layers)
- `parent_names`: unique names of parent nodes
- `shape`: layer output shape
- `name`: unique layer name (from TF/Keras)
- `__layer`: reference to the instance of the layer (if `include_layer_ref` is `True`)

How it works:

- It creates a pure Python tree clone of your model which is easy to walk through.

# Installation

This package has no depenedencies.

```
pip install keras-model-extract
```

# Example use

This examples show how to iterate through a model and print all the nodes.

```
>>> from keras_model_extract import copy_model_tree, iterate
>>> from keras.applications.vgg16 import VGG16
>>> model = VGG16()
>>> nodes = copy_model_tree(model)
>>> nodes
{'input_1': input_1, 'block1_conv1': block1_conv1, 'block1_conv2': block1_conv2, 'block1_pool': block1_pool, 'block2_conv1': block2_conv1, 'block2_conv2': block2_conv2, 'block2_pool': block2_pool, 'block3_conv1': block3_conv1, 'block3_conv2': block3_conv2, 'block3_conv3': block3_conv3, 'block3_pool': block3_pool, 'block4_conv1': block4_conv1, 'block4_conv2': block4_conv2, 'block4_conv3': block4_conv3, 'block4_pool': block4_pool, 'block5_conv1': block5_conv1, 'block5_conv2': block5_conv2, 'block5_conv3': block5_conv3, 'block5_pool': block5_pool, 'flatten': flatten, 'fc1': fc1, 'fc2': fc2, 'predictions': predictions}
>>> nodes['input_1'].children
[block1_conv1]
>>> nodes['block4_pool'].parent_names
['block4_conv3']
>>> nodes['block4_pool'].shape
(None, 14, 14, 512)
>>> iterate(nodes['input_1'], lambda layer: print(layer))
input_1
block1_conv1
block1_conv2
block1_pool
block2_conv1
block2_conv2
block2_pool
block3_conv1
block3_conv2
block3_conv3
block3_pool
block4_conv1
block4_conv2
block4_conv3
block4_pool
block5_conv1
block5_conv2
block5_conv3
block5_pool
flatten
fc1
fc2
predictions

```
