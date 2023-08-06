#ifndef _AngleKMeans_H
#define _AngleKMeans_H

#define _USE_MATH_DEFINES
// #define EIGEN_USE_BLAS
// #define EIGEN_DONT_PARALLELIZE 
#include <iostream>
#include <algorithm>
#include <fstream>
#include <stdlib.h>
#include <cmath>
#include <vector>
#include <numeric>
#include <limits>
#include <functional>
#include <set>
#include <ctime>
#include <chrono>
#include "Eigen400/Eigen/Dense"
#include "Eigen400/Eigen/Sparse"
#include "Eigen400/Eigen/Core"

using Eigen::MatrixXd;
using Eigen::MatrixXi;
using Eigen::VectorXd;
using Eigen::VectorXi;
using Eigen::RowVectorXd;
using namespace std;

typedef Eigen::Triplet<double> Tri;
typedef Eigen::SparseMatrix<double, Eigen::RowMajor> spMatdr; 
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matdr;
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> Matdc;
typedef Eigen::Matrix<bool,   Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matbr;
typedef Eigen::Matrix<bool, 1, Eigen::Dynamic, Eigen::ColMajor> Vecbr;
typedef Eigen::Array<bool,Eigen::Dynamic,1> ArrayXb;
typedef RowVectorXd Vecdr;
typedef VectorXd Vecdc;

typedef struct Veci_int{
    vector<int> labels;
    vector<int> dist_num;
    int iter;
    double cal_dist_num;
    double time;
};

class AngleKMeans{
public:
    int N = 0;
    int dim = 0;
    int c_true = 0;
    int debug = 0;

    Matdr X;
    Matdr Y_mat;
    Matdr eye_c;
    Vecdr o;
    Matdr C;
    Matdr Cn;
    // Matdr D_CC;
    Matdr A_CC;

    Vecdc c_norm;
    Vecdc x_norm;
    Vecdc nc;

    vector<vector<int>> Y;
    vector<vector<int>> dist_num_arr;
    vector<double> time_arr;
    vector<int> iter_arr;
    vector<int> dist_num_total;

    AngleKMeans();
    AngleKMeans(vector<vector<double>> &X, int c_true, int debug);
    ~AngleKMeans();

    void opt(vector<vector<int>> &Y, int ITER);
    Veci_int opt_once(vector<int> &y, int ITER);

    void cal_center(Matdr &X, vector<int> &y, Matdr &C);
    void cal_center2(Matdr &X, spMatdr &Y_mat, Matdr &C);
    void Eudist2(Matdr &X, Vecdc &xnorm, Matdr &D);
    void Eudist_X2v(Matdr &X, Vecdr &v, Vecdc &d);
};
#endif
