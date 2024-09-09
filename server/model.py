# from .schemas import *
# import torch
import torch.nn as nn

test_model = {
    "layers": [
        {
            "type": "flatten",
            "params": {},
            "activation": None
        },
        {
            "type": "linear",
            "params": {
                "num_nodes": 28*28,
            },
            "activation": None
        },
        {
            "type": "linear",
            "params": {
                "num_nodes": 512,
            },
            "activation": "relu"
        },
        {
            "type": "linear",
            "params": {
                "num_nodes": 512,
            },
            "activation": "relu"
        },
        {
            "type": "linear",
            "params": {
                "num_nodes": 10,
            },
            "activation": None
        },
    ],
}

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def construct_torch_model(json_model: dict):
    pt_layers = []
    num_layers = len(json_model["layers"])
    for i in range(num_layers - 1): 
        curr_layer = json_model["layers"][i]
        next_layer = json_model["layers"][i + 1]
        
        if curr_layer["type"] == "flatten":
            pt_layers.append(nn.Flatten())
        elif curr_layer["type"] == "linear":
            in_nodes = curr_layer["params"]["num_nodes"]
            out_nodes = next_layer["params"]["num_nodes"]
            pt_layers.append(nn.Linear(in_nodes, out_nodes))
            if next_layer["activation"]:
                pt_layers.append(nn.ReLU())
    
    return nn.Sequential(*pt_layers)

pt_test_model = construct_torch_model(test_model)
print(pt_test_model)
