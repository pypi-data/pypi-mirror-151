#include "EKM.h"

EKM::EKM(){}

EKM::EKM(vector<vector<double>> &X, int c_true, bool debug){
    this->N = X.size();
    this->dim = X[0].size();
    this->c_true = c_true;
    this->debug = debug;

    this->X.resize(N, dim);
    for (int i = 0; i < N; i++)
        this->X.row(i) = VectorXd::Map(&X[i][0], X[i].size());

    if (debug){
        cout << "N = " << N << ", dim = " << dim << ", c = " << c_true << endl;
    }

}

EKM::~EKM(){}

void EKM::opt(vector<vector<vector<double>>> &Cen, int ITER){

    int rep = Cen.size();

    Y.resize(rep);
    n_iter_.resize(rep);
    time_arr.resize(rep);
    cal_num_dist.resize(rep);
    dist_num_arr.resize(rep);

    for (int rep_i = 0; rep_i < rep; rep_i++){
        Veci_int ret = opt_once(Cen[rep_i], ITER);

        time_arr[rep_i] = ret.time;
        n_iter_[rep_i] = ret.iter;
        cal_num_dist[rep_i] = ret.cal_dist_num;
        dist_num_arr[rep_i] = ret.dist_num_arr;

        Y[rep_i].assign(ret.labels.data(),ret.labels.data() + N);
    }
}

Veci_int EKM::opt_once(vector<vector<double>> &Cen_vec, int ITER){

    MatrixOur Cen;
    Cen.resize(c_true, dim);
    for (int i = 0; i < c_true; i++)
        Cen.row(i) = VectorXd::Map(&Cen_vec[i][0], Cen_vec[i].size());

    Veci_int ret = run(X, Cen, ITER, debug);
    return ret;
}