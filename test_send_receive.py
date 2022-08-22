import redis
import cv2
import numpy as np
import struct
import msgpack
from PIL import Image
from io import BytesIO
from time import perf_counter

from assert_equal import assert_equal


# PIL
def sender_1(r: redis.Redis, image_path, num_iter=10):
    img = Image.open(image_path)
    encoded = BytesIO()
    tic = perf_counter()
    for i in range(num_iter):
        img.save(encoded, format=img.format)
        r.rpush('sender_1', encoded.getvalue())
    encoded.close()
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'sender_1 Sent {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')


# PIL but open file with 'rb' mode
def sender_2(r: redis.Redis, image_path, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):
        encoded = open(image_path, 'rb').read()
        r.rpush('sender_2', encoded)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'sender_2 Sent {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')


# np.tobytes() w/ cv2 encoding
def sender_3(r: redis.Redis, image_path, num_iter=10):
    img = cv2.imread(image_path)
    tic = perf_counter()
    for i in range(num_iter):
        retval, buffer = cv2.imencode('.png', img)
        encoded = buffer.tobytes()
        r.rpush('sender_3', encoded)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'sender_3 Sent {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')


# np.tobytes w/o encoding w/o shape info
def sender_4(r: redis.Redis, image_path, num_iter=10):
    img = cv2.imread(image_path)
    tic = perf_counter()
    for i in range(num_iter):
        encoded = img.tobytes()
        r.rpush('sender_4', encoded)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'sender_4 Sent {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')


# np.tobytes w/o encoding w/ shape info
def sender_5(r: redis.Redis, image_path, num_iter=10):
    img = cv2.imread(image_path)
    tic = perf_counter()
    for i in range(num_iter):
        h, w, c = img.shape
        shape = struct.pack('>III', h, w, c)
        encoded = shape + img.tobytes()
        r.rpush('sender_5', encoded)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'sender_5 Sent {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')


def receiver_1(r: redis.Redis, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):
        received = r.lpop('sender_1')
        img = Image.open(BytesIO(received))
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'receiver_1 Received {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/receiver_1.png", np.array(img))


def receiver_2(r: redis.Redis, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):
        received = r.lpop('sender_2')
        img = Image.open(BytesIO(received))
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'receiver_2 Received {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/receiver_2.png", np.array(img))
    

def receiver_3(r: redis.Redis, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):
        received = r.lpop('sender_3')
        img = cv2.imdecode(np.frombuffer(received, np.uint8), cv2.IMREAD_COLOR)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'receiver_3 Received {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/receiver_3.png", np.array(img))


def receiver_4(r: redis.Redis, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):
        received = r.lpop('sender_4')
        img = np.frombuffer(received, np.uint8).reshape((720, 1280, 3))
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'receiver_4 Received {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/receiver_4.png", np.array(img))


def receiver_5(r: redis.Redis, num_iter=10):
    tic = perf_counter()
    for i in range(num_iter):       
        encoded = r.lpop('sender_5')
        h, w, c = struct.unpack('>III',encoded[:12])
        img = np.frombuffer(encoded[12:], np.uint8).reshape(h, w, c)
    toc = perf_counter()
    elapsed_time = toc - tic
    print(f'receiver_5 Received {num_iter} images in {elapsed_time:.4f} s ({elapsed_time/num_iter*1000:.1f} ms / image).')
    cv2.imwrite("./data/receive/receiver_5.png", np.array(img))


# def toRedis(r: redis.Redis, a: np.ndarray, n: str):
#    """Store given Numpy array 'a' in Redis under key 'n'"""
#    h, w, c = a.shape
#    shape = struct.pack('>III', h, w, c)
#    encoded = shape + a.tobytes()
#    r.rpush(n, encoded)
#    return


# def fromRedis(r: redis.Redis, n: str):
#    """Retrieve Numpy array from Redis key 'n'"""
#    encoded = r.lpop(n)
#    h, w, c = struct.unpack('>III',encoded[:12])
#    a = np.frombuffer(encoded[12:], np.uint8).reshape(h, w, c)
#    return a


if __name__ == '__main__':
    num_iter = 10
    r = redis.Redis(host='localhost', port=6379, db=0)
    image_path = "./data/send/1000.png"
    sender_1(r, image_path, num_iter)
    sender_2(r, image_path, num_iter)
    sender_3(r, image_path, num_iter)
    sender_4(r, image_path, num_iter)
    sender_5(r, image_path, num_iter)
    
    receiver_1(r, num_iter)
    receiver_2(r, num_iter)
    receiver_3(r, num_iter)
    receiver_4(r, num_iter)
    receiver_5(r, num_iter)
    
    assert_equal(image_path, './data/receive/receiver_1.png')
    assert_equal(image_path, './data/receive/receiver_2.png')
    assert_equal(image_path, './data/receive/receiver_3.png')
    assert_equal(image_path, './data/receive/receiver_4.png')
    assert_equal(image_path, './data/receive/receiver_5.png')
    