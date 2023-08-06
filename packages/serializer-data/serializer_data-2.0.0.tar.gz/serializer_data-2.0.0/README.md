# serializer_data
serialize and deserialize objects in a simple way

there are two classes Serializer and Serializable, the first uses static methods while the other does not (see examples)

# Test 0
from serializer_data.serializable import Serializable

data_set = {"key1": 3, "key2": 5}

serial = Serializable("fileBinary.mm")

serial.serialize(data_set)

new_data_set = serial.deserialize()

print(new_data_set)

# Test 1
from serializer_data.serializer import Serializer

data_set = {"key1": 3, "key2": 5}

serial = Serializer.serialize(data_set, "fileBinary.mm")

new_data_set = Serializer.deserialize("fileBinary.mm")

print(new_data_set)

# Installation

pip install serializer_data

# Authors
Buscarino Antonino

# License

 GNU General Public License v3
