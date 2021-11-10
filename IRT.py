# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:50:57 2021

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
    
    code_question = data['Item'].values
    right_ans = data['Right_ans'].values
    a = data['a'].values
    b = data['b'].values
    c = data['c'].values
    
    return code_question, right_ans, a, b, c


# Cập nhật theta sau khi thí sinh trả lời k câu hỏi
def update_theta(theta, lr, a, b, c, X):
    '''
    a, b, c, X là vector có độ dài k
    '''
    temp = np.exp(a*(theta-b))
    s = np.sum((a * temp / (c + temp)) * (X - c - (1-c)*temp / (1+temp) ))

    theta = (1-lr) * theta + lr*s

    return theta

def binary_search(a, b, eps, index_remove, get_max=False):
    '''
    tìm chỉ số trong mảng b sao cho abs(a-b[i]) < eps
    tìm chỉ số i sao cho b[i] càng gần a càng tốt
    đồng thời i không nằm trong index_remove
    lấy ra câu khó nhất nếu get_max=True
    '''
    # trả về chỉ số của phần tử trong mảng b thỏa mãn |a-b| < eps
    index = np.argsort(b)
    if get_max:
        return index[-1]
    
    b = b[index]
    
    L = 0
    R = len(b) - 1
    result = -1
    
    while L <= R:
        m = (L + R) // 2
        
        if (abs(a - b[m]) <= eps):
            if (index[m] not in index_remove):
                result = index[m]
                eps = abs(a - b[m])
            if b[m] > a:
                R = m - 1
            else:
                L = m + 1
            
        elif b[m] - a >= eps:
            R = m - 1
        else:
            L = m + 1

    return result


# Chạy trên một bộ dữ liệu cụ thể
def run(path_data, theta, eps, K=None, max_seq_right=None):
    code_question, right_ans, a, b, c = read_data(path_data)
    
    # lưu các thông tin sau k câu hỏi
    code_question_k = np.array(['']) # mã câu hỏi
    index_question_k = np.array([]) # chỉ số của câu hỏi đã lấy ra
    answer_k = np.array([]) # câu trả lời
    a_k = np.array([])
    b_k = np.array([])
    c_k = np.array([])
    X_k = np.array([]).astype(int) # 1 là đúng, 0 là sai
    theta_k = np.array([]) # năng lực của thí sinh
    seq_right = 0 # lưu số lượng câu trả lời đúng liên tiếp cho đến câu hiện tại
    
    if K == None:
        K = len(a)
        
    print('Bắt đầu: ')
    for k in range(K):
        print('==============================================================')
        print('Câu hỏi số {}:'.format(k))
        print('Theta: {}'.format(round(theta, 3)))
        theta_k = np.append(theta_k, theta)
        
        # Tìm độ khó của câu tiếp theo
        i = binary_search(theta, b, eps, index_question_k, get_max=(seq_right==max_seq_right))
        index_question_k = np.append(index_question_k, i)
        
        if i == -1:
            k -= 1
            print('\nKhông có // không còn câu hỏi phù hợp với năng lực')
            break
        
        print('Độ khó: {}'.format(b[i]))
        print('Mã câu hỏi: {}'.format(code_question[i]))
        print('(Đáp án đúng: {})'.format(right_ans[i]))
                
        ans = input('Nhập câu trả lời: ')
        while ans not in ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd']:
            print('Câu trả lời không hợp lệ, nhập lại...')
            ans = input('Nhập câu trả lời: ')
        
        ans = ans.upper()
        answer_k = np.append(answer_k, ans)
        
        if ans != right_ans[i]:
            X_k = np.append(X_k, 0)
            seq_right = 0
        else:
            X_k = np.append(X_k, 1)
            seq_right += 1
            
        a_k = np.append(a_k, a[i])
        b_k = np.append(b_k, b[i])
        c_k = np.append(c_k, c[i])
        code_question_k = np.append(code_question_k, code_question[i])
        
        theta = update_theta(theta, lr, a_k, b_k, c_k, X_k)
        # print('==============================================================')
        
        
    print('==============================================================')
    print('KẾT THÚC: ')
    print('Năng lực của thí sinh: ', theta)
    print('Lịch sử làm bài: ')
    
    for i in range(k+1):
        print('''Câu hỏi số: {}
                 Mã câu hỏi: {}
                 Câu trả lời của thí sinh: {}
                 Trả lời đúng/sai: {}
                 Năng lực của thí sinh: {}
                 Độ phân biệt: {}
                 Độ khó: {}
                 Độ đoán mò: {}'''.format(i, code_question_k[i+1], answer_k[i], X_k[i], theta_k[i], a_k[i], b_k[i], c_k[i]))

        

if __name__ == '__main__':
    # theta khởi tạo ngẫu nhiên theo phân phối chuẩn
    theta = 0 #np.random.randn()
    lr = 0.01
    eps = 0.05
    # Số câu tối đa cần trả lời 
    K = 100
    # Số câu trả lời đúng liên tiếp thì lấy ra câu khó nhất
    max_seq_right = 5
    path_data = './500b_v3.csv'
    theta = run(path_data, theta, eps, K, max_seq_right)
    
    
    
    
    
    
    
    
    
    
    
    
    
    