def approximate(eps, a, b):
	L = 0
	R = len(b) - 1 

	result = None

	while L<R:
		m = ceil(L + n/2)
		if abs(a - b[m]) < eps:
			result = b[m]
			break
		else:
			if a < b[m] - eps:
				R = m - 1
			else:
				L = m + 1

	return result