#ifndef BALL_KMEANSPP_XD_H_
#define BALL_KMEANSPP_XD_H_

#include <iostream>
#include <fstream>
#include <time.h>
#include <cstdlib>
#include <chrono>
#include <algorithm>
#include "Eigen339/Eigen/Dense"
#include <unistd.h>
#include <vector>
#include <cfloat>
#include <numeric>

using namespace std;
using namespace Eigen;

typedef double OurType;

typedef VectorXd VectorOur;

typedef MatrixXd MatrixOur;

typedef vector<vector<OurType>> ClusterDistVector;

typedef vector<vector<unsigned int>> ClusterIndexVector;

typedef Array<bool, 1, Dynamic> VectorXb;

typedef struct Neighbor
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

typedef vector<Neighbor> sortedNeighbors;

MatrixOur load_data(const char* filename);

inline MatrixOur
update_centroids(MatrixOur& dataset, ClusterIndexVector& cluster_point_index, unsigned int k, unsigned int n,
                 VectorXb& flag,
                 unsigned int iteration_counter, MatrixOur& old_centroids);


inline void update_radius(MatrixOur& dataset, ClusterIndexVector& cluster_point_index, MatrixOur& new_centroids,
                          ClusterDistVector& temp_dis,
                          VectorOur& the_rs, VectorXb& flag, unsigned int iteration_counter, unsigned int& cal_dist_num,
                          unsigned int the_rs_size);

inline sortedNeighbors
get_sorted_neighbors_Ring(VectorOur& the_Rs, MatrixOur& centers_dis, unsigned int now_ball, unsigned int k,
                          vector<unsigned int>& now_center_index);

inline sortedNeighbors
get_sorted_neighbors_noRing(VectorOur& the_rs, MatrixOur& centers_dist, unsigned int now_ball, unsigned int k,
                            vector<unsigned int>& now_center_index);


inline void
cal_centers_dist(MatrixOur& new_centroids, unsigned int iteration_counter, unsigned int k, VectorOur& the_rs,
                 VectorOur& delta, MatrixOur& centers_dis);

inline MatrixOur cal_dist(MatrixOur& dataset, MatrixOur& centroids);

inline MatrixOur
cal_ring_dist_Ring(unsigned j, unsigned int data_num, unsigned int dataset_cols, MatrixOur& dataset,
                   MatrixOur& now_centers,
                   ClusterIndexVector& now_data_index);

inline MatrixOur
cal_ring_dist_noRing(unsigned int data_num, unsigned int dataset_cols, MatrixOur& dataset, MatrixOur& now_centers,
                     vector<unsigned int>& now_data_index);


void initialize(MatrixOur& dataset, MatrixOur& centroids, VectorXi& labels, ClusterIndexVector& cluster_point_index,
                ClusterIndexVector& clusters_neighbors_index,
                ClusterDistVector& temp_dis);


inline MatrixOur initial_centroids(MatrixOur dataset, int k, int random_seed = -1);
Veci_int ball_k_means_Ring(MatrixOur& dataset, MatrixOur& centroids, int ITER, bool detail = false);
Veci_int ball_k_means_noRing(MatrixOur& dataset, MatrixOur& centroids, int ITER, bool detail = false);

Veci_int ball_k_means(MatrixOur& dataset, MatrixOur& centroids, int ITER, bool isRing = false, bool detail = false);
#endif //BALL_KMEANSPP_XD_H_
