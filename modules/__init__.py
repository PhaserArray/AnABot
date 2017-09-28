from os.path import basename, isfile, dirname
from os import walk

def is_module(file):
	if not file.endswith(".py"):
		return False
	if file.endswith("__.py"):
		return False
	return True

__all__ = [f[:-3] for f in next(walk(dirname(__file__)))[2] if is_module(f)]