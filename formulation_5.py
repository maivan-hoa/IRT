import math

def update_phi(p, k, gamma, a, b, c, X):
	s = 0
	for i in range(k):
		temp = math.exp(a[i]*(p-b[i]))
		s += (a[i] * temp / (c[i] + temp)) * (X[i] - c[i] - (1-c[i])*temp / (1+temp) )

	p = (1-gamma) * p + gamma*s

	return p