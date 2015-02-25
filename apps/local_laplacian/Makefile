CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: local_laplacian graph.png

local_laplacian: laplacian.so
	python main.py ../../images/rgb.png 1 1 11

laplacian.so: laplacian_polymage.cpp
	$(CXX) $(CXX_FLAGS) laplacian_polymage.cpp -o laplacian.so

graph.png:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
