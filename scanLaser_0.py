import numpy as np # 数值处理
import argparse # 命令行参数
import cv2 #绑定openCV

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-r", "--radius", type = int,
                help = "radius of Gaussian blur; must be odd")
args = vars(ap.parse_args())

# 加载图像，复制图像并转换为灰度图
image = cv2.imread(args["image"])orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 查找图像中最亮点的敏感方法是使用cv2.minMaxLoc，称其敏感的原因是该方法极易受噪音干扰，可以通过预处理步骤应用高斯模糊解决。
# 寻找最小、最大像素强度所在的（x,y）
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
# 在最大像素上绘制空心蓝色圆圈
cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)

# 展示该方法的结果
cv2.imshow("Naive", image)

# 使用cv2.minMaxLoc，如果不进行任何预处理，可能会非常容易受到噪音干扰。
# 相反，最好先对图像应用高斯模糊以去除高频噪声。这样，即使像素值非常大（同样由于噪声）也将被其邻居平均。
# 在图像上应用高斯模糊消除高频噪声，然后寻找最亮的像素
# 高斯模糊的半径取决于实际应用和要解决的问题；
gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
image = orig.copy()
cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)

# 展示效果显著提升后的方法结果
cv2.imshow("Robust", image)
cv2.waitKey(0)
