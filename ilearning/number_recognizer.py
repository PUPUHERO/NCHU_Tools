# -*- coding: utf-8 -*-
"""
Created on Sat May 28 16:01:26 2022

@author: PUPUHERO
"""

import os
import sys
import base64
import cv2 as cv
import numpy as np
from imutils import contours #Fix:module 'myutils' has no attribute 'sort_contours'

try:
    from model import img
except ModuleNotFoundError:
    from .model import img

# =============== for pyinstaller ===============
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    thisDir_path = os.path.dirname(sys.executable)
elif __file__:
    thisDir_path = os.path.dirname(__file__)
# ================================================

class NumberRecognizer:
    def __init__(self):
        self.model = AnalyzedImage()
        self.target = AnalyzedImage()
        self.numbers = []
        self.model_set = {}
        self.__init_next()
    
    def __init_next(self):
        default_model = base64.b64decode(img)
        self.model = self.setModel(default_model)
    
    def getNumbers(self) -> str:
        self.__test_image()
        
        number_string = ""
        for number in self.numbers:
            number_string += str(number)
        
        return number_string
    
    def setModel(self, model, threshold = 75):
        self.model = AnalyzedImage(model)
        self.model.set_threshold(threshold)
        self.__make_model_set()
        
    def setTarget(self, target, threshold = 75):
        self.target = AnalyzedImage(target)
        self.target.set_threshold(threshold)
    
    def __make_model_set(self):
        model_image = self.model.image
        model_gray = self.model.image_gray
        model_contours = self.model.Contours
        
        # 單個輪廓提取到字典中
        for (i, c) in enumerate(model_contours):
            (x, y, w, h) = cv.boundingRect(c)
            roi = model_gray[y:y + h, x:x + w]  # 在模板中復制出輪廓
            roi = cv.resize(roi, (14, 28))  # 改成相同大小的輪廓
            self.model_set[i+1] = roi  # 此時字典鍵對應的輪廓即為對應數字。如鍵‘1’對應輪廓‘1’
    
    def __test_image(self):
        target_image = self.target.image
        target_gray = self.target.image_gray
        target_contours = self.target.Contours
        
        target_contours_list = []  # 存符合條件的輪廓
        for i, c in enumerate(target_contours):
            # 計算矩形
            x, y, w, h = cv.boundingRect(c)
            target_contours_list.append((x, y, w, h))
            
        for (i, (gx, gy, gw, gh)) in enumerate(target_contours_list):  # 遍歷每一組輪廓(包含1個數字)
            # 根據坐標提取每一個組(4個值)
            #(x,y) -> (w,h)
            target_contours_rectangle = target_gray[gy - 1:gy + gh + 1, gx - 1:gx + gw + 1] # 往外擴一點
            target_contours_rectangle = cv.resize(target_contours_rectangle, (14, 28))
            
            # 計算匹配得分: 1得分多少,2得分多少...
            scores = [0]  # 單次循環中,scores存的是一個數值 匹配 10個模板數值的最大得分, 先給一個0是因為數字0不會出現，因此為0分
            # 在模板中計算每一個得分
            # digits的digit正好是數值1,...,9; digitROI是每個數值的特徵表示
            for (digit, digitROI) in self.model_set.items():
                # 進行模板匹配, res是結果矩陣
                res = cv.matchTemplate(target_contours_rectangle, digitROI, cv.TM_CCOEFF_NORMED)  
                #此時roi是X digitROI是1 依次是1,2.. 匹配10次,看模板最高得分多少
                #cv::TM_CCOEFF：相關性係數匹配方法，該方法使用源圖像與其均值的差、模板與其均值的差二者之間的相關性進行匹配，最佳匹配結果在值等於1處
                #，最差匹配結果在值等於-1處，值等於0直接表示二者不相關。
                Max_score = cv.minMaxLoc(res)[1]  # 返回4個,取第二個最大值MaxScore
                scores.append(Max_score)  #存取對應模板的成績
                
            self.numbers.append((np.argmax(scores)))  # 返回score中最大值的位置 即最合適的數字
            
        # 框出數字外方格
            # cv.rectangle(target_image, (gx - 2, gy - 2), (gx + gw + 2, gy + gh + 2), (0, 0, 255), 1)  # 左上角,右下角
        
class AnalyzedImage:
    def __init__(self, image = None):
        self.threshold = 75
        self.image = image
        self.image_gray = None
        self.Contours = None
        self.__init_next()
    
    def __init_next(self):
        self.image_getContours()
        
    def set_threshold(self, threshold):
        self.threshold = threshold

    def image_getContours(self):
        # 預處理
        if (self.image == None):
            return 0
        elif (type(self.image) == str):
            self.image = cv.imread(self.image)
        elif (type(self.image) == bytes):
            npArr = np.asarray(bytearray(self.image),dtype="uint8")
            self.image = cv.imdecode(npArr, cv.IMREAD_COLOR)
        else:
            print("image must be str or bytes")
            return 0
        
        #模板轉換為灰度圖
        image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        #轉換為二值圖,把數字部分變為白色
        #cv2.THRESH_BINARY_INV：Threshold Binary, Inverted，將大於門檻值的灰階值設為0，其他值設為最大灰階值。'''一旦超過門檻=85就會把雜點當輪廓'''
        self.image_gray = cv.threshold(image_gray, self.threshold, 255, cv.THRESH_BINARY_INV)[1]# 騷寫法，函數多個返回值為元組，這裡取第二個返回值
        # 對圖像進行輪廓檢測，得到輪廓信息
        Contours , hierarchy_card = cv.findContours(self.image_gray.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        cv.drawContours(self.image, Contours, -1, (0, 0, 255), 1)# 第一個參數為目標圖像
        # 輪廓排序 changed
        self.Contours = contours.sort_contours(Contours)[0]