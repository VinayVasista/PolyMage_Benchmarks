CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: camera_pipe graph

naive: camera_pipe_naive

camera_pipe: camera_opt.so
	rm -f camera.so
	ln -s $< camera.so
	python main.py 3700 50 2.0 11

camera_pipe_naive: camera_naive.so
	rm -f camera.so
	ln -s $< camera.so
	python main.py 3700 50 2.0 11

camera_opt.so: camera_pipe_polymage.cpp
	$(CXX) $(CXX_FLAGS) $< -o $@

camera_naive.so: camera_pipe_polymage_naive.cpp
	$(CXX) $(CXX_FLAGS) $< -o $@

graph:
	dot -Tpng graph.dot >graph.png

clean:
	rm -f *.pyc *.so graph.png
