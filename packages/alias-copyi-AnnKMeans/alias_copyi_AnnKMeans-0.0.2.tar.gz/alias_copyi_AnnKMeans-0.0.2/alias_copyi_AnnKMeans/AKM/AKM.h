#ifndef AKM_H_
#define AKM_H_
#include "ann_kmeanspp.h"

class AKM{
public:
    int N, dim, c_true;
    bool debug;
    MatrixOur X;
    vector<vector<int>> Y;
    vector<vector<int>> dist_num_arr;
    vector<int> n_iter_;
    vector<double> time_arr;
    vector<int> cal_num_dist;

    AKM();
    AKM(vector<vector<double>> &X, int c_true, bool debug);
    ~AKM();

    void opt(vector<vector<vector<double>>> &Cen, int ITER);
    Veci_int opt_once(vector<vector<double>> &Cen_vec, int ITER);

};

#endif // AKM_H_