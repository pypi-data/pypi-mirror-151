

windows:

0.- Install visual studio build tools 2019 -------------- THIS MIGHT NOT BE NECESARY ---------------

1.- Install Python >= 3.6.5 32 or 64 bits. It must match the C compiler for the libraries to work (from https://www.python.org/ )

2.- run:
		pip3 install numpy pyqt5 nibabel pydicom scikit-image scipy PyOpenGL PyOpenGL_accelerate

3.- run make in the Framework/CExtend directory (your compiler has to match 32 or 64 bits from python)

4.- run:
		python FiberVis.py

linux:
### https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get ###
0.- run:
		sudo add-apt-repository ppa:jonathonf/python-3.6
		sudo apt-get update
		sudo apt-get install python3.6

1.- run:
		pip3 install --upgrade pip
		python3 -m pip install nibabel pydicom scikit-image scipy numpy pyqt5 PyOpenGL PyOpenGL_accelerate

2.- run in the Framework/CExtend directory:
		make

2.5.- In case of problems with OpenGL library, when running make on the C libraries
		Check on the link below for further installation of OpenGL libraries
		https://en.wikibooks.org/wiki/OpenGL_Programming/Installation/Linux

3.- run:
		python3.6 FiberVis.py

mac:

0.- Check that Python 3.6+ is install by running:
		python3 -V

	if not, install Python 3.6+ from https://www.python.org/

	install gcc using brew:
		brew install gcc

	change target in Framework/CExtend/Makefile:
		CC=gcc    to CC=gcc-8     (or the version installed by brew... check with gcc doble tap in terminal)

1.- run:
		python3 -m pip install --upgrade pip
		python3 -m pip install nibabel pydicom scikit-image scipy numpy pyqt5 PyOpenGL PyOpenGL_accelerate

2.- run in the Framework/CExtend directory:
		make

	if failed with "GL/gl.h: No such file or directory", then run:
		sudo apt-get install libgl-dev
		make

3.- run:
		python3 FiberVis.py