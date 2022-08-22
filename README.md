# Introduction
Test sending images to redis (c++), and getting images from redis (python).

# Setup
1. ```mkdir data/receive```
2. ```mkdir build && cd build```
3. ```cmake ..```
4. ```make```

# Usage
- ```./sender``` (in ```build``` directory): send images (c++).
- ```./receive_assert.sh```: receive images (python), and assert if it is equal to the original image.
- ```python test_send_receive.py```: test send & receive with various methods (python).

