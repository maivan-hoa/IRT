# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 00:00:01 2021

@author: Mai Van Hoa - HUST
"""

import pandas as pd
import math
import numpy as np


def read_data(path):
    '''
    a - độ phân biệt
    b - độ khó
    c - độ đoán mò
    '''
    data = pd.read_csv(path)
    
    a = data['a'].values
    b = data['b'].values
    c = data['c'].values
    
    return a, b, c


# Xác suất trả lời đúng câu hỏi i của thí sinh có năng lực theta
def right_probability(theta, a, b, c):
    temp = np.exp(a*(theta-b))
    X = c + (1-c)*( temp / (1 + temp))
    
    return X

# Cập nhật theta sau khi thí sinh trả lời k câu hỏi
def update_theta(theta, lr, a, b, c, X):
    '''
    a, b, c, X là vector có độ dài k
    '''
    temp = np.exp(a*(theta-b))
    s = np.sum((a * temp / (c + temp)) * (X - c - (1-c)*temp / (1+temp) ))

    theta = (1-lr) * theta + lr*s

    return theta

def binary_search(a, b, eps):
    # trả về chỉ số của phần tử trong mảng b thỏa mãn |a-b| < eps
    index = np.argsort(b)
    b = b[index]
    
    L = 0
    R = len(b) - 1
    
    while L <= R:
        m = (L + R) // 2
        
        if abs(a - b[m]) < eps:
            return index[m]
        elif b[m] - a > eps:
            R = m - 1
        else:
            L = m + 1
            
    return -1


# Chạy trên một bộ dữ liệu cụ thể
def run(path_data, theta, K=None):
    a, b, c = read_data(path_data)
    
    if K == None:
        K = len(a)
        
    for k in range(1, K+1):
        X_k = right_probability(theta, a, b, c)[:k]
        a_k = a[:k]
        b_k = b[:k]
        c_k = c[:k]
        
        theta = update_theta(theta, lr, a_k, b_k, c_k, X_k)
        # print(theta)
    return theta


def run_multi(path_data, theta):
    for path in path_data:
        theta = run(path, theta)
        
    return theta
        

if __name__ == '__main__':
    
    # theta khởi tạo ngẫu nhiên theo phân phối chuẩn
    theta = np.random.randn()
    lr = 0.001
    eps = 1
    
    
# =============================================================================
#     # Chạy trên một bộ dl
#     K = 400
#     path_data = './500_v2.csv'
#     theta = run(theta, K)
# =============================================================================
    
    
    # Chạy trên nhiều bộ
    path_1 = './data_1.csv'
    path_2 = './data_2.csv'
    path_3 = './data_3.csv'
    path_4 = './data_4.csv'
    path_5 = './data_5.csv'
    
    path_data = [path_1, path_2, path_3, path_4]
    run_multi(path_data, theta)
    
    
    _, b, _ = read_data(path_5)
    i = binary_search(theta, b, eps)
    
    if i != -1:
        print('Với năng lực {}, câu hỏi tiếp theo là câu số {}, có độ khó là {}'.format(theta, i+1, b[i]))
    else:
        print('Không có câu hỏi tiếp theo phù hợp với năng lực')










