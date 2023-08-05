//This version is completed by Yong Zheng(413511280@qq.com), Shuyin Xia（380835019@qq.com）, Xingxin Chen, Junkuan Wang.  2020.5.1
#ifndef EXP_KMEANSPP_H_
#define EXP_KMEANSPP_H_

#include <iostream>
#include <fstream>
#include <time.h>
#include <cstdlib>
#include <algorithm>
#include <chrono>
#include "Eigen339/Eigen/Core"
#include <vector>
#include <float.h>
#include <numeric>

using namespace std;
using namespace Eigen;

typedef double OurType;

typedef VectorXd VectorOur;

typedef MatrixXd MatrixOur;

typedef vector<vector<OurType> > ClusterDistVector;

typedef vector<vector<unsigned int> > ClusterIndexVector;

typedef Array<bool, 1, Dynamic> VectorXb;

struct Neighbor
    //Define the "neighbor" structure
{
    OurType distance;
    int index;
};

typedef struct Veci_int{
    VectorXi labels;
    vector<int> dist_num_arr;
    int iter;
    double cal_dist_num;
    double time;
};

typedef vector<Neighbor> SortedNeighbors;

MatrixOur load_data(const char* filename);

inline MatrixOur update_centroids(MatrixOur& dataset, ClusterIndexVector& clusters_point_index, unsigned int k,
                                  unsigned int dataset_cols, VectorXb& flag,
                                  unsigned int iteration_counter, MatrixOur& old_centroids);

inline void update_radius(MatrixOur& dataset, ClusterIndexVector& clusters_point_index, MatrixOur& new_centroids,
                          ClusterDistVector& point_center_dist,
                          VectorOur& the_rs, VectorXb& flag, unsigned int iteration_counter, unsigned int& cal_dist_num,
                          unsigned int the_rs_size);

inline SortedNeighbors
get_sorted_neighbors(VectorOur& the_rs, MatrixOur& centers_dist, unsigned int now_ball, unsigned int k,
                     vector<unsigned int>& now_center_index, vector<unsigned int>& new_in_center_index);

inline void
cal_centers_dist(MatrixOur& new_centroids, unsigned int iteration_counter, unsigned int k, VectorOur& the_rs,
                 VectorOur& delta, MatrixOur& centers_dist);

inline MatrixOur cal_dist(MatrixOur& dataset, MatrixOur& centroids);

inline MatrixOur
cal_ring_dist(unsigned int data_num, unsigned int dataset_cols, MatrixOur& dataset, MatrixOur& now_centers,
              vector<unsigned int>& now_data_index);

void initialize(MatrixOur& dataset, MatrixOur& centroids, VectorOur& labels, ClusterIndexVector& clusters_point_index,
                ClusterIndexVector& clusters_neighbors_index,
                ClusterDistVector& point_center_dist, VectorOur& lx);


Veci_int run(MatrixOur &dataset, MatrixOur &centroids, int ITER, bool debug);

bool LessSort(Neighbor a, Neighbor b);

#endif //EXP_KMEANSPP_XD_H_


