from model.model import Model

model = Model()
print(f"Numero nodi: {model.get_num_nodi()}")
print(f"Numero archi: {model.get_num_archi()}")
model.buildGraph()
print(f"Numero nodi: {model.get_num_nodi()}")
print(f"Numero archi: {model.get_num_archi()}")