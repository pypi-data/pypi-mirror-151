import os
from math import exp


def is_hexa(seq):
	if (seq[0] == seq[1] == seq[2]) and (seq[3] == seq[4] == seq[5]):
		return 0.001
	return None

def is_fivetwo(seq):
	if (seq[0] == seq[1] == seq[2] == seq[3] == seq[4]) and (seq[5] == seq[6]):
		return 0.001
	return None

def is_twofive(seq):
	if (seq[0] == seq[1] ) and (seq[2] == seq[3] == seq[4] == seq[5] == seq[6]):
		return 0.001
	return None

def is_twofour(seq):
	if (seq[0] == seq[1] ) and (seq[2] == seq[3] == seq[4] == seq[5]):
		return 0.004
	return None

def is_threetwotwo(seq):
	if (seq[0] == seq[1] == seq[2]) and (seq[3] == seq[4]) and (seq[5] == seq[6]):
		return 0.004
	return None

def is_threetwo(seq):
	if (seq[0] == seq[1] == seq[2]) and (seq[3] == seq[4]):
		return 0.0156
	return None

def is_same(seq):
	return seq == len(seq) * seq[0]

def is_six(seq):
	if is_same(seq[:6]):
		return 0.001
	return None

def is_five(seq):
	if is_same(seq[:5]):
		return 0.004
	return None

def is_four(seq):
	if is_same(seq[:4]):
		return 0.0156
	return None

def is_three(seq):
	if is_same(seq[:3]):
		return 0.0625
	return None

def is_twoonethree(seq):
	# too common
	if (seq[0] == seq[1]) and (seq[3] == seq[4] == seq[5]):
		return 0.0156
	return None

def is_twoonetwo(seq):
	# too common
	if (seq[0] == seq[1]) and (seq[3] == seq[4]):
		return 0.0625
	return None

def is_twoonefour(seq):
	if (seq[0] == seq[1]) and (seq[3] == seq[4] == seq[5] == seq[6]):
		return 0.004
	return None

def has_backward_motif(seq):
	# these are the motifs to look for
	for motif in [is_six, is_hexa, is_fivetwo, is_twofive, is_twofour, is_threetwotwo, is_five, is_twoonefour, is_twoonethree]:
		if motif(seq):
			return (motif.__name__.ljust(15), motif(seq))
	return None

def has_forward_motif(seq):
	# these are the motifs to look for
	for motif in [is_hexa]: #, is_threetwo]:
		if motif(seq):
			return (motif.__name__.ljust(15), motif(seq))
	for motif in [is_four, is_three]:
		if motif(seq[3:7]):
			return (motif.__name__.ljust(15), motif(seq[3:7]))
	return None

def has(motif, seq):
	for i in range(0,len(seq),3):
		try:
			if motif(seq[i:]):
				return True
		except:
			pass
	return False

