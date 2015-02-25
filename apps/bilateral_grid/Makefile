CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: bilateral_grid graph.png

bilateral_grid: bilateral.so
	python main.py ../../images/rgb.png 11

bilateral.so: bilateral_grid_polymage.cpp
	$(CXX) $(CXX_FLAGS) bilateral_grid_polymage.cpp -o bilateral.so

graph.png:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
