# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:50:57 2021

@author: Mai Van Hoa - HUST
"""

import pandas as pd
import math
import numpy as np
import os
import csv
from datetime import datetime
import yaml


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


def write_data(path_log, data):
            
    with open(path_log, 'a', newline='') as f:
        csvwriter = csv.writer(f) 
        # writing the data 
        csvwriter.writerow(data)
            


def print_summary(theta, k, code_question_k, answer_k, X_k, theta_k, a_k, b_k, c_k):
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
                 Độ đoán mò: {}'''.format(i, code_question_k[i], answer_k[i], 
                                     X_k[i], round(theta_k[i], 3), a_k[i], b_k[i], c_k[i]))

# Cập nhật theta sau khi thí sinh trả lời k câu hỏi
def update_theta(theta, lr, a, b, c, X):
    '''
    a, b, c, X là vector có độ dài k
    '''
    temp = np.exp(a*(theta-b))
    s = np.sum((a * temp / (c + temp)) * (X - c - (1-c)*temp / (1+temp) ))

    theta = (1-lr) * theta + lr*s

    return theta


def find_next(a, b, eps, index_remove, get_max=False, get_min=False):
    '''
    tìm chỉ số trong mảng b sao cho abs(a-b[i]) < eps
    tìm chỉ số i sao cho b[i] càng gần a càng tốt
    đồng thời i không nằm trong index_remove
    lấy ra câu khó nhất nếu get_max=True
    '''
    # trả về chỉ số của phần tử trong mảng b thỏa mãn |a-b| < eps
    if get_max:
        index = np.argsort(b)
        if index[-1] not in index_remove:
            return index[-1]
        return -1
    
    if get_min:
        index = np.argsort(b)
        for i in range(len(index)):
            if index[i] not in index_remove:
                return index[i]
        return -1
    
    delta = abs(b - a)
    index = np.argsort(delta)
    delta = delta[index]
    
    result = -1
    for i in range(len(delta)):
        if delta[i]<=eps and index[i] not in index_remove:
            return index[i]
        
    return result



# Chạy trên một bộ dữ liệu cụ thể
def run(ID, path_data, path_log, time_checked, theta, eps, max_seq_right, 
        max_seq_wrong, max_seq_theta, eps_theta, K=None):
    
    code_question, right_ans, a, b, c = read_data(path_data)
    
    # lưu các thông tin sau k câu hỏi
    code_question_k = np.array([]) # mã câu hỏi
    index_question_k = np.array([]) # chỉ số của câu hỏi đã lấy ra
    answer_k = np.array([]) # câu trả lời
    a_k = np.array([])
    b_k = np.array([])
    c_k = np.array([])
    X_k = np.array([]).astype(int) # 1 là đúng, 0 là sai
    theta_k = np.array([]) # năng lực của thí sinh
    
    seq_right = 0 # lưu số lượng câu trả lời đúng liên tiếp cho đến câu hiện tại
    seq_wrong = 0 # lưu số lượng câu trả lời sai liên tiếp cho đến câu hiện tại
    seq_theta = 0 # lưu số lượng câu trả lời liên tiếp mà theta thay đổi không 
                  # đáng kể cho đến câu hiện tại
    
    
    if K == None:
        K = len(a)
        
    print('Bắt đầu: ')
    for k in range(K):
        print('==============================================================')
        print('Câu hỏi số {}:'.format(k))
        print('Theta: {}'.format(round(theta, 3)))
        theta_k = np.append(theta_k, theta)
        
        # Tìm độ khó của câu tiếp theo
        get_max = (seq_right==max_seq_right)
        if get_max:
            print("====LẤY RA CÂU KHÓ NHẤT====")
            
        get_min = (seq_wrong==max_seq_wrong)
        if get_min:
            print("====LẤY RA CÂU DỄ NHẤT CHƯA TRẢ LỜI====")
        
        # i = binary_search(theta, b, eps, index_question_k, get_max=get_max)
        i = find_next(theta, b, eps, index_question_k, get_max=get_max, get_min=get_min)
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
            seq_wrong += 1
        else:
            X_k = np.append(X_k, 1)
            seq_right += 1
            seq_wrong = 0
            
        a_k = np.append(a_k, a[i])
        b_k = np.append(b_k, b[i])
        c_k = np.append(c_k, c[i])
        code_question_k = np.append(code_question_k, code_question[i])
        
        theta = update_theta(theta, lr, a_k, b_k, c_k, X_k)
        
        if get_max:
            if ans==right_ans[i]:
                print('TRẢ LỜI ĐÚNG CÂU KHÓ NHẤT')
                break
            else:
                print('TRẢ LỜI SAI CÂU KHÓ NHẤT')
                break
            
        if get_min:
            if ans==right_ans[i]:
                print('TRẢ LỜI ĐÚNG CÂU DỄ NHẤT')
                break
            else:
                print('TRẢ LỜI SAI CÂU DỄ NHẤT')
                break
        
        
        if abs(theta - theta_k[k]) > eps_theta:
            seq_theta = 0
        else:
            seq_theta += 1 # nếu theta thay đổi không đáng kể, tăng bộ đếm
            
        if (seq_theta==max_seq_theta):
            print('===THETA KHÔNG THAY ĐỔI QUÁ NHIỀU===')
            break
        # print('==============================================================')
    
    data = [ID, theta, time_checked+1, datetime.today().strftime('%Y-%m-%d-%H:%M:%S')]
    write_data(path_log, data)
    print_summary(theta, k, code_question_k, answer_k, X_k, theta_k, a_k, b_k, c_k)
        

        

if __name__ == '__main__':
    path_config = './config.yaml'
    with open(path_config, encoding="utf8") as file:
        conf = yaml.full_load(file)
    
    path_data = conf['path_data']
    path_log = conf['path_log']
    ID = conf['ID']
    lr = conf['lr']
    eps = conf['eps']
    K = conf['K']
    max_seq_wrong = conf['max_seq_wrong']
    max_seq_right = conf['max_seq_right']
    max_seq_theta = conf['max_seq_theta']
    eps_theta = conf['eps_theta']
    
    if not os.path.exists(path_log):
        fields = ['ID', 'Theta', 'Time_check', 'Date']
        write_data(path_log, fields)
        
    # theta khởi tạo từ làm lần thi trước của thí sinh
    data_log = pd.read_csv(path_log)
    df_id = data_log[data_log['ID'] == ID]
    time_checked = len(df_id)
    
    if time_checked == 0:
        theta = 0 #np.random.randn()
    else:
        theta = df_id[df_id['Time_check'] == time_checked].Theta.values[0]
        
    
    print('CÁC THAM SỐ KHỞI TẠO:')
    print('''
          ID thí sinh: {}
          Theta: {}
          learning rate: {}
          eps: {}
          K: {}
          '''.format(ID, theta, lr, eps, K))
    
    
    run(ID, path_data, path_log, time_checked, theta, eps, max_seq_right, 
        max_seq_wrong, max_seq_theta, eps_theta, K)
    
    
    
    
    
    
    
    
    
    
    
    
    
    