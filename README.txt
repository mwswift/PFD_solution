Code accompanying "Modeling the electrical double layer at solid-state electrochemical interfaces"
Michael W Swift, James W Swift, Yue Qi

Software distributed under the GNU General Public License, version 3 (GPL-3.0)

+++

For the analytical approximations to the full solution, use PFD_solution.py

Required software:
	python
		numpy, scipy, and matplotlib

Instructions for use:
	Execute the provided python script, providing a .yaml file with the input parameters as an argument

Example:
	./PFD_solution.py LiF.yaml

Example input files:
	LiF.yaml
	Li2CO3.yaml
	Li2O_111.yaml
	Li2O_110.yaml
	LLZO.yaml

Example output files:
	Plots and stdout for the respective input files

+++

For the full numerical solution to the PDF equation, see the Mathematica notebooks:

https://www.wolframcloud.com/obj/swift/Published/PFD_LLZO.nb
https://www.wolframcloud.com/obj/swift/Published/PFD_Interlayers.nb

Required software:
	Wolfram Mathematica: tested on versions 12.1.0.0 and 11.1.1.0

Installation guide:
	Install Mathematica and open notebooks

Demo & Instructions for Use:
	Select all cells (Ctrl+A) and run (Shift+Enter)
	PFD_LLZO includes needed LLZO parameters.
	PFD_Interlayers has LiF Li2CO3, and Li2O parameters.  Li2CO3 and Li2O are commented out.  To reproduce results in these materials, comment out LiF data and uncomment desired data before re-running.
	Expected output is plots showing numerical solution, both in physical and dimensionless units, together with some numerical comparisons with the approximations discussed in the text.
	Runtime should be ~10 seconds.

