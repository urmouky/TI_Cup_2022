import cv2
import numpy as np
 
 
# 文档长宽，下面是A4纸比例
x = 420  # 长
y = 600  # 宽
 
def preProcessor(img):
    """
    图片预处理
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度
    blurred = cv2.bilateralFilter(gray, 2, 200, 200)  # 双边滤波降噪
    edged = cv2.Canny(blurred, 25, 200)  # 边缘识别
    edged = cv2.dilate(edged, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))  # 膨胀连接边缘
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 寻找轮廓
    print(len(contours))
    paperCnt = None  # 文档轮廓
    
    if len(contours) > 0:
        # 按轮廓面积降序排列
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours:
            # 近似轮廓
            peri = cv2.arcLength(c, True)  # 获取轮廓周长
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # 多边形拟合，输出多边形顶点
            if len(approx) == 4:
                paperCnt = approx
                break
    cv2.polylines(img, [paperCnt], True, (0, 255, 0), 3)  # 画出轮廓
    return [i[0] for i in paperCnt]
 
 
def transform(img, mp, dp):
    """
    透视变换，mp：原图像点， dp：目标图像点
    """
    global x
    global y
    # 修改点的格式
    pts1 = np.float32(mp)
    pts2 = np.float32(dp)
     
    # 生成透视矩阵
    M = cv2.getPerspectiveTransform(pts1, pts2)
     
    # 转换
    dst = cv2.warpPerspective(img, M, (x, y))
    return dst
 
 
def enhance(img):
    """
    增强显示
    """
    dst = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 自适应阈值
    th = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    return th
 
 
def show(img):
    """
    绘图
    """
    global x
    global y
    cv2.imshow('Scanner', img)
    k = cv2.waitKey(0)
    if k == 27:  # 按ESC退出
        cv2.destroyAllWindows()
    elif k == ord('r'):  # 按r旋转结果
        init = [[0, 0], [x, 0], [x, y], [0, y]]
        dstp = init[1:] + init[:1]
        img = transform(img, init, dstp)
        show(img)
    elif k == ord('s'):  # 按s保存图片
        cv2.imwrite('Scanned5.png')
 
 
if __name__ == "__main__":
    img = cv2.imread(".\Lib\doc_test.jpg")
    src = img.copy()
    mp = preProcessor(img)
    cv2.imshow('Result', img)
    dp = [[0, y], [x, y], [x, 0], [0, 0]]
    docimg = transform(src, mp, dp)
    docimg = enhance(docimg)
    cv2.namedWindow('Scanner', cv2.WINDOW_NORMAL)
    show(docimg)