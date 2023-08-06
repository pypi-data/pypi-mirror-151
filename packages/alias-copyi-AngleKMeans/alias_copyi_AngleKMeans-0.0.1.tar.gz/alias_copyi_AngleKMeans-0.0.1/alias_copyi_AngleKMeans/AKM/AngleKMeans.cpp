#include "AngleKMeans.h"

AngleKMeans::AngleKMeans(){}

AngleKMeans::AngleKMeans(std::vector<std::vector<double>> &X, int c_true, int debug){
    this->N = X.size();
    this->dim = X[0].size();
    this->c_true = c_true;
    this->debug = debug;

    this->X.resize(N, dim);
    for (int i = 0; i < N; i++){
        this->X.row(i) = VectorXd::Map(&X[i][0], X[i].size());
    }
    this->o = MatrixXd::Zero(1, dim);
    this->C.resize(c_true, dim);
    this->Cn.resize(N, dim);
    // this->D_CC.resize(c_true, c_true);
    this->A_CC.resize(c_true, c_true);
    this->c_norm.resize(c_true);
    this->x_norm.resize(N);
    this->eye_c = MatrixXd::Identity(c_true, c_true);
    this->nc.resize(c_true);
}

AngleKMeans::~AngleKMeans() {}

void AngleKMeans::cal_center(Matdr &X, vector<int> &y, Matdr &C){

    nc.setZero();
    C.setZero();
    // #pragma omp parallel for reduction(+:C)
    for (int i = 0; i < y.size(); i++){
        int tmp_c = y[i];
        C.row(tmp_c) += X.row(i);
        nc(tmp_c) ++;
    }

    C = C.array().colwise() / nc.array();
}

void AngleKMeans::Eudist2(Matdr &X, Vecdc &xnorm, Matdr &D){
    D.noalias() = -2 * X * X.transpose();
    D.colwise() += xnorm;
    D.rowwise() += xnorm.transpose();
}

void AngleKMeans::Eudist_X2v(Matdr &X, Vecdr &v, Vecdc &d){
}


Veci_int AngleKMeans::opt_once(std::vector<int> &y, int ITER){
    std::chrono::time_point<std::chrono::steady_clock> t1;
    std::chrono::time_point<std::chrono::steady_clock> t2;

    Eigen::setNbThreads(12);
    Vecdc r2(N);
    Vecdc c_norm_n(N);
    Vecdc ocx(N);
    Matdr D_CC(c_true, c_true);

    vector<vector<int>> Ind_D(c_true, vector<int>(c_true, 0));

    int Iter;
    vector<int> dist_num(ITER, 0);
    VectorXi change = MatrixXi::Zero(N, 1);
    VectorXi dist_num_par = MatrixXi::Zero(N, 1);

    t1 = std::chrono::steady_clock::now();

    x_norm = X.rowwise().squaredNorm();

    for (Iter = 0; Iter < ITER; Iter++){

        // update C
        cal_center(X, y, C);

        Cn = C(y, Eigen::placeholders::all);
        c_norm.noalias() = C.rowwise().squaredNorm();  // c:dist
        c_norm_n = c_norm(y);

        // compute D_CC, A_CC
        Eudist2(C, c_norm, D_CC);   // c*c:dist
        A_CC = (D_CC.colwise() + c_norm).rowwise() - c_norm.transpose();
        D_CC = D_CC.cwiseSqrt();
        D_CC.diagonal().array() = 0;
        A_CC.array() /= 2 * (D_CC.array().colwise() * c_norm.cwiseSqrt().array());
        A_CC = A_CC.array().acos();

        // argsort D
        for (int i = 0; i < c_true; i++){
            iota(Ind_D[i].begin(), Ind_D[i].end(), 0);
            sort(Ind_D[i].begin(), Ind_D[i].end(), [&, i](int i1, int i2){ return D_CC(i, i1) < D_CC(i, i2); });
        }
        
        // cout << D_CC.row(0) << endl;
        // for (int i = 0; i < c_true; i++){
        //     cout << D_CC(0, Ind_D[0][i]) << ", ";
        // }
        // cout << endl;

        // update y
        r2.noalias() = (X - Cn).rowwise().squaredNorm();  // r   n:dist


        // compute beta
        ocx = c_norm_n.array() + r2.array() - x_norm.array();
        ocx.array() /= 2 * c_norm_n.cwiseSqrt().array() * r2.cwiseSqrt().array();
        ocx = ocx.array().acos();

        change.setZero();
        dist_num_par.setZero();

        #pragma omp parallel for
        for (int i = 0; i < y.size(); i++){

            int k = y[i];;
            double rr = r2(i);
            double r = sqrt(rr);
            int c_old = y[i];

            if (D_CC(k, Ind_D[k][1]) >= 2 * r){
                continue;
            }

            Vecdr tmp1 = (A_CC.row(k).array() - ocx(i)).cos() - (D_CC.row(k) * 0.5 / r).array();
            vector<int> cal_ind;
            cal_ind.clear();
            int jj;
            for (int j = 1; j < c_true; j++){
                jj = Ind_D[k][j];
                if (D_CC(k, jj) >= 2 * r){
                    break;
                }
                if (tmp1(jj) > 0){
                    cal_ind.push_back(jj);
                }
            }
            if (cal_ind.size() == 0){
                continue;
            }

            Vecdc d_xi_c = c_norm(cal_ind) - 2 * C(cal_ind, Eigen::placeholders::all) * X.row(i).transpose();

            ptrdiff_t c_new_ptr;
            auto tmp_d = d_xi_c.minCoeff(& c_new_ptr);
            if (tmp_d < rr - x_norm(i)){
                int c_new = (int) c_new_ptr;
                c_new = cal_ind[c_new];
                if (c_old != c_new){
                    change(i) = 1;
                    y[i] = c_new;
                }
            }
            dist_num_par(i) = cal_ind.size();
        }

        dist_num[Iter] = c_true * c_true + c_true + N + dist_num_par.sum();

        if (change.sum() == 0){
            break;
        }
    }

    t2 = std::chrono::steady_clock::now();

    Veci_int ret;
    ret.time = std::chrono::duration<double>(t2 - t1).count();
    ret.iter = Iter + 1;
    ret.cal_dist_num = accumulate(dist_num.begin(), dist_num.end(), decltype(dist_num)::value_type(0));
    ret.dist_num = dist_num;
    ret.labels = y;
    return ret;
}

void AngleKMeans::opt(std::vector<std::vector<int>> &Y_init, int ITER){
    int rep = Y_init.size();
    this->Y.resize(rep);

    // t1 = std::chrono::steady_clock::now();
    // t2 = std::chrono::steady_clock::now();
    // double time_1 = std::chrono::duration<double>(t2 - t1).count();
    // std::cout << "xnorm time " << time_1 << std::endl;

    // Y
    time_arr.resize(rep);
    iter_arr.resize(rep);
    dist_num_arr.resize(rep);
    dist_num_total.resize(rep);

    for (int rep_i = 0; rep_i < rep; rep_i++){
        auto ret = opt_once(Y_init[rep_i], ITER);

        iter_arr[rep_i] = ret.iter;
        time_arr[rep_i] = ret.time;
        dist_num_arr[rep_i] = ret.dist_num;
        dist_num_total[rep_i] = ret.cal_dist_num;
        Y[rep_i] = ret.labels;
    }
}

