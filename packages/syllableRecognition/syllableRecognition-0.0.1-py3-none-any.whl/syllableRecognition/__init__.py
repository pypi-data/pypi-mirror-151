#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    ：syllableFunction.py
@Author  ：唐维康
@Date    ：2022/3/12 16:55 
@功能：
@用法：
'''

import librosa
import numpy as np
import os
from sklearn.cluster import *
from hmmlearn.hmm import *
import time
import multiprocessing as ms
import soundfile as sf
import math

def run_kmeans(dataset, K, m=20):
    labs = KMeans(n_clusters=K, random_state=9).fit_predict(dataset)
    return labs

def gen_para_GMM(fea_collect, N_mix):
    # 首先对特征进行kmeans 聚类
    feas = np.concatenate(fea_collect, axis=0)
    N, D = np.shape(feas)
    # print("sub_fea_shape",feas.shape)
    # 初始化聚类中心
    labs = run_kmeans(feas, N_mix, m=20)
    mus = np.zeros([N_mix, D])
    sigmas = np.zeros([N_mix, D])
    ws = np.zeros(N_mix)
    for m in range(N_mix):
        index = np.where(labs == m)[0]
        # print("----index---------",index)
        sub_feas = feas[index]
        mu = np.mean(sub_feas, axis=0)
        sigma = np.var(sub_feas, axis=0)
        sigma = sigma + 0.0001
        mus[m] = mu
        sigmas[m] = sigma

        # print("------N  D-------",N,np.shape(index)[0])
        ws[m] = np.shape(index)[0] / N
    ws = (ws + 0.01) / np.sum(ws + 0.01)
    return ws, mus, sigmas


def init_para_hmm(collect_fea, N_state, N_mix):
    # 初始 一定从 state 0 开始
    pi = np.zeros(N_state)
    pi[0] = 1

    #  当前状态 转移概率0.5 下一状态 转移概率0.5
    #  进入最后一个状态后不再跳出
    A = np.zeros([N_state, N_state])
    for i in range(N_state - 1):
        A[i, i] = 0.5
        A[i, i + 1] = 0.5
    A[-1, -1] = 1

    feas = collect_fea
    len_feas = []
    for fea in feas:
        len_feas.append(np.shape(fea)[0])

    _, D = np.shape(feas[0])
    hmm_means = np.zeros([N_state, N_mix, D])
    hmm_sigmas = np.zeros([N_state, N_mix, D])
    hmm_ws = np.zeros([N_state, N_mix])

    for s in range(N_state):

        sub_fea_collect = []
        # 初始化时 先为每个状态平均分配特征
        for fea, T in zip(feas, len_feas):
            T_s = int(T / N_state) * s
            T_e = (int(T / N_state)) * (s + 1)

            sub_fea_collect.append(fea[T_s:T_e])
        ws, mus, sigmas = gen_para_GMM(sub_fea_collect, N_mix)
        hmm_means[s] = mus
        hmm_sigmas[s] = sigmas
        hmm_ws[s] = ws

    return pi, A, hmm_means, hmm_sigmas, hmm_ws

def extract(wav_file):
    # 读取音频数据
    y, sr = librosa.load(wav_file, sr=8000)
    # 提取特征
    fea = librosa.feature.mfcc(y, sr, n_mfcc=13, n_mels=26, n_fft=512, win_length=512, hop_length=128, lifter=0)
    # 进行正则化
    mean = np.mean(fea, axis=1, keepdims=True)
    std = np.std(fea, axis=1, keepdims=True)
    fea = (fea - mean) / std
    # 添加1阶差分
    fea_d = librosa.feature.delta(fea)
    fea = np.concatenate([fea.T, fea_d.T], axis=1)

    # f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'),
    #                                              win_length=512, hop_length=128)
    # f0[np.isnan(f0)] = 0
    # # f0 = f0.reshape((188,1))
    # f0 = f0[:, np.newaxis];
    # fea = np.concatenate((fea, f0), axis=1)

    return fea

def add_noise(audio_path, SNR, sr=8000):
    #读取语音文件data和fs
    src, sr = librosa.core.load(audio_path, sr=sr)
    #
    random_values = np.random.rand(len(src))
    #计算语音信号功率Ps和噪声功率Pn1
    Ps = np.sum(src ** 2) / len(src)
    Pn1 = np.sum(random_values ** 2) / len(random_values)

    # 计算k值
    k=math.sqrt(Ps/(10**(SNR/10)*Pn1))
    #将噪声数据乘以k,
    random_values_we_need=random_values*k
    #计算新的噪声数据的功率
    Pn=np.sum(random_values_we_need**2)/len(random_values_we_need)
    #以下开始计算信噪比
    snr=10*math.log10(Ps/Pn)
    #print("当前信噪比：",snr)

    #单独将噪音数据写入文件
    #sf.write(noise_path,random_values_we_need, sr)
    #将噪声数据叠加到纯净音频上去
    outdata=src+random_values_we_need
    # 将叠加噪声的数据写入文件
    #sf.write(out_path, outdata, sr)
    return outdata, sr

def extractSNR(wav_file, SNR):
    # 读取音频数据
    #y, sr = librosa.load(wav_file, sr=8000)
    y, sr = add_noise(wav_file, SNR, sr=8000)
    # 提取特征
    fea = librosa.feature.mfcc(y, sr, n_mfcc=13, n_mels=26, n_fft=512, win_length=512, hop_length=128, lifter=0)
    # 进行正则化
    mean = np.mean(fea, axis=1, keepdims=True)
    std = np.std(fea, axis=1, keepdims=True)
    fea = (fea - mean) / std
    # 添加1阶差分
    fea_d = librosa.feature.delta(fea)
    fea = np.concatenate([fea.T, fea_d.T], axis=1)

    # f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'),
    #                                              win_length=512, hop_length=128)
    # f0[np.isnan(f0)] = 0
    # # f0 = f0.reshape((188,1))
    # f0 = f0[:, np.newaxis];
    # fea = np.concatenate((fea, f0), axis=1)

    return fea

#计算文件夹的个数
def NumberOfFolders(path):
    return len([lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))])

#显示路径下是哪些语种
def LanguageName(path):
    LanguageList=[]
    for root, dirs, files in os.walk(path):
        for aa in dirs:
            LanguageList.append(aa)
    return LanguageList

#训练模型
def TrainTheModel(NumberOfFolders,train_path):
    time_start = time.time()
    models = []

    LanguageList = LanguageName(train_path)  # 语种名字
    #print(LanguageList)

    for i in range(NumberOfFolders):
        wav_path = os.path.join(train_path, LanguageList[i])
        #print(wav_path)
        collect_fea = []
        len_feas = []
        #将每个语种的特征提取
        dirs = os.listdir(wav_path)
        for file in dirs:
            # print(file)
            # 找到 .wav 文件并提取特征
            if file.split(".")[-1] == "wav":
                wav_file = os.path.join(wav_path, file)
                # twk测试 读出的语音文件名
                # print(wav_file)

                fea = extract(wav_file)
                collect_fea.append(fea)
                len_feas.append(np.shape(fea)[0])

        # 获取模型参数初始化
        N_state = 4
        N_mix = 3
        pi, A, hmm_means, hmm_sigmas, hmm_ws = init_para_hmm(collect_fea, N_state, N_mix)

        train_GMMHMM = GMMHMM(n_components=N_state,
                              n_mix=N_mix,
                              covariance_type='diag',
                              n_iter=90,
                              tol=1e-5,
                              verbose=False,
                              init_params="",
                              params="tmcw",
                              min_covar=0.0001
                              )
        train_GMMHMM.startprob_ = pi
        train_GMMHMM.transmat_ = A

        train_GMMHMM.weights_ = hmm_ws
        train_GMMHMM.means_ = hmm_means
        train_GMMHMM.covars_ = hmm_sigmas

        print("train syllableModel", LanguageList[i])
        train_GMMHMM.fit(np.concatenate(collect_fea, axis=0), np.array(len_feas))

        models.append(train_GMMHMM)

    #保存模型
    np.save("syllableModel5.npy", models)

    #计算程序运行时间
    time_end=time.time()
    #print('time cost {0} m'.format(round((time_end-time_start)/60,2)))

def test():
    pid = os.fork() # 创建一个子进程
    if pid == 0:
        print(11111)

#读取音节特征
def ReadFeature(path):
    ExtremePointBinaryTxt = ''
    # with open(path, "r") as f:  # 打开文件
    #     for line in f:
    #         # data = f.read()  # 读取文件
    #         ExtremePointBinaryTxt += (line.rstrip())
    # a = ExtremePointBinaryTxt.replace(',', '').replace(' ', '')
    feature=extract(path)
    return feature

#读取音节特征
def ReadFeatureSNR(path, SNR):
    ExtremePointBinaryTxt = ''
    # with open(path, "r") as f:  # 打开文件
    #     for line in f:
    #         # data = f.read()  # 读取文件
    #         ExtremePointBinaryTxt += (line.rstrip())
    # a = ExtremePointBinaryTxt.replace(',', '').replace(' ', '')
    feature=extractSNR(path, SNR)
    return feature

#查看二进制数据
def viewData():
    #train_path = "train"
    #计算文件夹的个数
    #NumberOfFolders = len([lists for lists in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, lists))]) # 语种的个数
    #TrainTheModel(NumberOfFolders)
    train_path = "train"
    NumberOfFolders =NumberOfFolders = len([lists for lists in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, lists))])
    p1 = ms.Process(target=TrainTheModel,args=(NumberOfFolders,train_path,))
    p1.start()
    p1.join()
    return 1
# if __name__=="__main__":
#     train_path = "train"
#     NumberOfFolders = NumberOfFolders(train_path)  # 语种的个数
#     TrainTheModel(train_path,NumberOfFolders)
