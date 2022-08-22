# Introduction
Test sending images to redis (c++), and getting images from redis (python).

# Setup
```
mkdir data/receive
mkdir build && cd build
cmake ..
make
```

# Usage
- ```./sender``` (run in ```build``` directory): send images to redis (c++).
- ```./receive_assert.sh```: receive images from redis (python), and assert if it is equal to the original image.
- ```python test_send_receive.py```: test send & receive with various methods (python).

