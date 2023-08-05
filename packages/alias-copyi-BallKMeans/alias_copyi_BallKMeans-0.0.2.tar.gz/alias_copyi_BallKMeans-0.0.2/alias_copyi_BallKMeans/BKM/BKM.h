#ifndef BKM_H_
#define BKM_H_
#include "ball_kmeans++_xd.h"

class BKM{
public:
    int N, dim, c_true;
    bool debug;
    MatrixOur X;
    vector<vector<int>> Y;
    vector<int> n_iter_;
    vector<double> time_arr;
    vector<int> cal_num_dist;
    vector<vector<int>> dist_num_arr;

    BKM();
    BKM(vector<vector<double>> &X, int c_true, bool debug);
    ~BKM();

    void opt(vector<vector<vector<double>>> &Cen, bool isRing, int ITER);
    Veci_int opt_once(vector<vector<double>> &Cen_vec, int ITER, bool isRing);

};

#endif // BKM_H_