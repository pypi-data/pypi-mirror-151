#ifndef EKM_H_
#define EKM_H_
#include "exp_kmeanspp.h"

class EKM{
public:
    int N, dim, c_true;
    bool debug;
    MatrixOur X;
    vector<vector<int>> Y;
    vector<vector<int>> dist_num_arr;
    vector<int> n_iter_;
    vector<double> time_arr;
    vector<int> cal_num_dist;

    EKM();
    EKM(vector<vector<double>> &X, int c_true, bool debug);
    ~EKM();

    void opt(vector<vector<vector<double>>> &Cen, int ITER);
    Veci_int opt_once(vector<vector<double>> &Cen_vec, int ITER);

};

#endif // EKM_H_