CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: harris graph.png

harris: harris.so
	python main.py ../../images/grand_canyon2.jpg 11

harris.so: harris_polymage.cpp
	$(CXX) $(CXX_FLAGS) harris_polymage.cpp -o harris.so

graph.png:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
