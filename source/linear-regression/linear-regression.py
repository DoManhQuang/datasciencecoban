import numpy as np
import matplotlib.pyplot as plt


def display_chart_linear(vector_z, vector_q, linear, oxy):
    if linear is not None:
        b = linear[0][0]
        a = linear[1][0]
        x_linear = np.linspace(oxy[0], oxy[1], 6)
        y_linear = x_linear * a + b
        # print(x_linear)
        # print(y_linear)
        plt.plot(x_linear, y_linear)
        pass

    plt.xlabel('mực nước (m)')
    plt.ylabel('dòng xả (m3/s)')
    plt.axis([oxy[0], oxy[1], oxy[2], oxy[3]])
    plt.plot(vector_z, vector_q, 'bo')
    plt.show()
    pass


def linear_regression(y_vector, v_matrix):
    w_1 = np.linalg.pinv(np.dot(v_matrix.T, v_matrix))
    w_2 = np.dot(v_matrix.T, y_vector)
    w = np.dot(w_1, w_2)
    return w


if __name__ == '__main__':
    dong_xa_oy = np.array([[55, 156, 287, 442, 618, 812, 2016, 2297, 2590,
                            2894, 3210, 3536, 5317, 5701, 6094, 6496,
                            6906, 7325]]).T

    muc_nuoc_ox = np.array([[196.5, 197., 197.5, 198., 198.5, 199.,
                             201.5, 202., 202.5, 203., 203.5, 204.,
                             206.5, 207., 207.5, 208., 208.5, 209.0]]).T
    oxy_array = [195, 210, 0, 8000]

    b_vector = np.array(np.ones((muc_nuoc_ox.__len__(), 1)))
    a_matrix = np.concatenate((b_vector, muc_nuoc_ox), axis=1)

    liner_vector = linear_regression(dong_xa_oy, a_matrix)

    display_chart_linear(muc_nuoc_ox, dong_xa_oy, liner_vector, oxy_array)

    from sklearn import linear_model
    lin_model = linear_model.LinearRegression(fit_intercept=False)
    lin_model.fit(a_matrix, dong_xa_oy)
    print('Solution found by sk-learn w = : ', lin_model.coef_)
    print('Solution found by team w = ', liner_vector.T)





