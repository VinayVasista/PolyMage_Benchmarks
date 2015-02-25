CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: pyramid_blending graph.png

pyramid_blending: blending.so
	python main.py ../../images/grand_canyon1.jpg ../../images/grand_canyon2.jpg 11 2048 2048

blending.so: blending_polymage.cpp
	$(CXX) $(CXX_FLAGS) blending_polymage.cpp -o blending.so

graph.png:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
