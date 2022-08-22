import redis
import cv2
import numpy as np
import struct
from time import perf_counter


def receiver(r: redis.Redis):
    ttic = perf_counter()
    num_data = r.llen('images')
    for i in range(num_data):
        tic = perf_counter()
        received = r.lpop('images')
        image = cv2.imdecode(np.frombuffer(received, np.uint8), cv2.IMREAD_COLOR)
        toc = perf_counter()
        print(f'Received {i+1} ({(toc - tic)*1000:.1f} ms) (bytes: {len(received):,})')
    ttoc = perf_counter()
    elapsed_time = ttoc - ttic
    print(f'Received {num_data} images in {elapsed_time:.4f} s ({elapsed_time/num_data*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/1000.png", np.array(image))


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    receiver(r)
    