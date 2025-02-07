def transpose(field):
	return [list(row) for row in zip(*field)]

def invert(field):
	return [row[::-1] for row in field]
