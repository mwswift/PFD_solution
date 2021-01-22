#!/usr/bin/env python

import numpy as np
import yaml
import sys
from scipy.optimize import brentq 
import matplotlib.pyplot as plt

kB = 0.0000861733 # eV/K

def PFD_solution(param_dict, print_values=True, plot_fname=None):

	'''
	Implements an analytical approximation to the solution of the
	Poisson-Fermi-Dirac equation

	inputs:
		param_dict containing the following values:
			phi0       : Charge-neutrality potential (V)
            NSites     : Defect site density (cm^-3)
            Ef0        : Formation energy at charge neutrality (eV)
            epsilon    : Dielectric constant
            alpha      : Saturation parameter
            T          : Temperature (Kelvin)
            phi_target : Target potential for finding xstar (V)
        
        print_values (bool) [True]: print resulting values to stdout
        plot_fname (str)    [None]: filename to save a plot of phi vs x


	returns:
		None

	'''

	# Read parameters
	phi0    = param_dict["phi0"]
	NSites  = param_dict["NSites"]
	Ef0     = param_dict["Ef0"]
	epsilon = param_dict["epsilon"]
	alpha   = param_dict["alpha"]
	T       = param_dict["T"]
	phi_target = param_dict["phi_target"]

	# Calculate derived quantities
	ftoV = kB*T  
	B    = alpha * np.exp(Ef0/ftoV)
	lamb = 6.90089807e+8*np.sqrt(epsilon * T/(alpha * NSites)) # Angstroms
	f0   = phi0 / ftoV

	# Eq. 8
	U = -np.log((np.exp(f0)+B)/(1+B)) - np.log((np.exp(-f0)+B)/(1+B))
	
	# Eq. 9
	fp0 = -np.sqrt(-2*U)

	xi1 = -fp0
	x1 = xi1 * lamb

	# Eq. 12
	def phi1(x):
		xi = x/lamb

		f = f0 + fp0 * xi + 0.5*xi**2

		return phi0 - f * ftoV

	# Eq. 15
	c = xi1 - np.sqrt(2)

	# Eq.14
	def phi2(x):
		xi = x/lamb
		
		f = 4 * np.arctanh(np.exp(-np.sqrt(2/B) * (xi - c)))

		return phi0 - f * ftoV

	xi2 = np.sqrt(B/2)
	x2 = xi2*lamb

	# Connect two approximations
	def phi(x):
		if x <= x1:
			return phi1(x)
		else:
			return phi2(x)

	# Eq. 11
	sigma = 6.90089807e-14 * fp0 * np.sqrt(alpha * NSites * T / epsilon)
	capacitance = 16.0218 * np.abs(sigma / phi0)

	if print_values:
		print("x_1      = {0:8.4f} A".format(x1))
		print("phi(x_1) = {0:8.4f} V".format(phi(x1)))
		print("x_2      = {0:8.2E} A".format(x2))
		print("phi(x_2) = {0:8.4f} V".format(phi(x2)))
		print("phi(inf) = {0:8.4f} V".format(phi0))
		print("sigma    = {0:8.4f} e/nm^2".format(sigma))
		print("C/A      = {0:8.4f} muF/cm^2".format(capacitance))

	# Find xstar such that phi(xstar) = phi_target
	def phi_minus_phi_target(x):
		return phi(x) - phi_target

	xmin = 0
	xmax = max(x2, 1000.0)
	try:
		xstar = brentq(phi_minus_phi_target, xmin, xmax, full_output=False)
		if print_values:
			print("xstar    = {0:8.2f} A".format(xstar))
	except:
		xstar = None
		print("Could not find xstar for phi={0:3.1f} between x={1:3.1f} and x={2:3.1f}".format(
			phi_target, xmin, xmax))

	if plot_fname is not None:
		plt.figure()
		xlist = np.logspace(-1, 8, num=200)
		ylist = [phi(x) for x in xlist]
		plt.xscale("log")
		plt.xlim([10**-1,10**8])
		plt.plot(xlist, ylist)
		if xstar is not None:
			xpoints=[x1, xstar, x2]
		else:
			xpoints=[x1, x2]
		ypoints=[phi(x) for x in xpoints]
		plt.plot(xpoints, ypoints, "x")
		plt.xlabel("x ($\mathrm{\AA}$)")
		plt.ylabel("$\phi$ (V)")
		plt.grid()
		plt.savefig(plot_fname)
		plt.close()


if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		raise TypeError("Provide filename with input parameters")

	fname = sys.argv[1]

	with open(fname, 'r') as f:
		param_dict = yaml.safe_load(f)

	PFD_solution(param_dict, plot_fname = fname.split(".")[0]+".pdf")



