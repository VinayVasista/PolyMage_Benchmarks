CXX=icpc
CXX_FLAGS=-openmp -ipo -O3 -xhost -fPIC -shared

#CXX=g++
#CXX_FLAGS=-fopenmp -O3 -fPIC -shared

all: $(APP) graph

naive: $(APP)_naive

$(APP)_opt.so: $(APP)_polymage.cpp
	$(CXX) $(CXX_FLAGS) $< -o $@

$(APP)_naive.so: $(APP)_polymage_naive.cpp
	$(CXX) $(CXX_FLAGS) $< -o $@

graph: graph.png

graph.png: graph.dot
	dot -Tpng $< > $@

clean:
	rm -f *.pyc *.so graph.png
