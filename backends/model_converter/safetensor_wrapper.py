from safetensors import safe_open


class SafetensorWrapper:

	def __init__(self , fname ):
		self.file = safe_open(fname, framework="np", device="cpu")
		self.new_items = {}

	def keys(self):
		return list(self.file.keys()) + list(self.new_items.keys())

	def __contains__(self, k):
		return True if k in self.file.keys() else k in self.new_items

	def __getitem__(self , k):
		return self.new_items[k] if k in self.new_items else self.file.get_tensor(k)

	def __setitem__(self, key , item ):
		self.new_items[key] = item

	def __iter__(self):
		return iter(self.keys())