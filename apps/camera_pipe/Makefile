CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: camera_pipe graph

naive: camera_pipe_naive

camera_pipe: camera.so
	python main.py 3700 50 2.0 11

camera_pipe_naive: camera_naive.so
	python main.py 3700 50 2.0 11

camera.so: camera_pipe_polymage.cpp
	$(CXX) $(CXX_FLAGS) camera_pipe_polymage.cpp -o camera.so

camera_naive.so: camera_pipe_polymage_naive.cpp
	$(CXX) $(CXX_FLAGS) camera_pipe_polymage_naive.cpp -o camera.so

graph:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
