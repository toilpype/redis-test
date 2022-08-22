#include <sw/redis++/redis++.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <chrono>

// #include <b64/encode.h>
// #include <unistd.h>
// #include <stdio.h>

using namespace std;
using namespace sw::redis;


int main(int argc, char** argv) {
    string image_path = "../data/send/1000.png";
    int num_iter = 100;
    auto redis = Redis("tcp://127.0.0.1:6379");
    cv::Mat image = cv::imread(image_path);
    
    auto ttic = chrono::high_resolution_clock::now();

    for (int i=0; i<num_iter; i++) {
        auto tic = chrono::high_resolution_clock::now();
        // // ver.1) 31.5 ms
        // vector<uchar> buf;
        // cv::imencode(".png", image, buf);
        // // // slightly faster mode (~ 27 ms)
        // // vector<int> encoding_params;
        // // encoding_params.push_back(cv::IMWRITE_PNG_STRATEGY);
        // // encoding_params.push_back(cv::IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY);
        // // cv::imencode(".png", image, buf, encoding_params);
        // string encoded(buf.begin(), buf.end());
        // redis.rpush("images", encoded);
        
        // // ver.2) 212.2 ms
        // stringstream stream;
        // stream << image;
        // redis.rpush("images", stream.str());
        
        // // ver.3) 211.1 ms
        // cv::String image_string;
        // image_string<< image;
        // redis.rpush("images", image_string.c_str());
        
        // ver.4) 3.8 ms
        vector<uchar> buf;
        cv::imencode(".bmp", image, buf);
        string encoded(buf.begin(), buf.end());
        redis.rpush("images", encoded);

        // // ver.5) if ver.4) is not fast enough, find another way to serialize image w/o encoding.
        // int size = 720*1280*3;
        // uchar buf[size];
        // memcpy(buf, image.data, size); // only copies 47886
        // stringstream stream = boost::serialization::serialize(image);
        // redis.rpush("images", buf);
        auto toc = chrono::high_resolution_clock::now();
        auto elapsed_ms = chrono::duration<double, std::milli> (toc - tic).count();
        printf("Sent %d (%.1f ms)\n", i+1, elapsed_ms);
    }
    auto ttoc = chrono::high_resolution_clock::now();
    
    auto total_elapsed_ms = chrono::duration<double, std::milli> (ttoc - ttic).count();
    printf("Sent %d images in %.4f s (%.1f ms / image).\n", num_iter, total_elapsed_ms/1000, total_elapsed_ms/num_iter);

    // // show window
    // string window_name = "sender";
    // cv::namedWindow(window_name);
    // char key = ' ';
    // while (key != 27) {
    //     cv::imshow(window_name, image);
    //     key = cv::waitKey(10);
    // }
}

