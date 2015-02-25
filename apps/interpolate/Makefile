CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: interpolate graph.png

interpolate: interpolate.so
	python main.py ../../images/rgb.png ../../images/alpha.png 11

interpolate.so: interpolate_polymage.cpp
	$(CXX) $(CXX_FLAGS) interpolate_polymage.cpp -o interpolate.so

graph.png:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
