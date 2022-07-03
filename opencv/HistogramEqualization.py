from cv2 import PSNR
import numpy as np
import cv2
import math

img = cv2.imread("window.jpg") # 이미지 불러오기
img_y = cv2.imread("window.jpg",cv2.IMREAD_GRAYSCALE) # 그레이 스케일 이미지 불러오기
# ycbcr의 y성분과 같음

hist,bins=np.histogram(img_y.ravel(),256,[0,256]) #이미지의 y성분 히스토그램
cdf=hist.cumsum() # 누적합 구해서 cdf에 저장
cdf_m = np.ma.masked_equal(cdf,0) # cdf에서 0인 부분 무시
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min()) # 히스토그램 equalization 수식
cdf = np.ma.filled(cdf_m, 0).astype('uint8')
img2 = cdf[img_y]


height, width, channel = img.shape
b = img[..., 0] 
g = img[..., 1] 
r = img[..., 2] 
y = np.zeros((height, width), dtype=float) 
cr = np.zeros((height, width), dtype=float) 
cb = np.zeros((height, width), dtype=float)
for i in range(height): 
    for j in range(width): 
        y[i][j] = round(0.299 * r[i][j] + 0.587 * g[i][j] + 0.114 * b[i][j])
        cr[i][j] = -0.172 * r[i][j] -0.339 * g[i][j] + 0.511 * b[i][j] + 128 
        cb[i][j] = 0.511 * r[i][j] -0.428 * g[i][j] - 0.083 * b[i][j] + 128 

out = (np.dstack((img2, cr, cb))).astype(np.uint8)
cv2.imshow("com",out)
com = cv2.cvtColor(out,cv2.COLOR_YCrCb2RGB)
cv2.imshow("com2",com)

cv2.imshow("out2",img2)
b2= np.zeros((height, width), dtype=float) 
g2 = np.zeros((height, width), dtype=float) 
r2 = np.zeros((height, width), dtype=float) 
for i in range(height): 
    for j in range(width): 
        r2[i][j] = y[i][j] + 1.371 * (cr[i][j] - 128)
        g2[i][j] = y[i][j] - 0.698 * (cr[i][j] - 128) - 0.336*(cb[i][j] - 128)
        b2[i][j] = y[i][j] + 1.732 * (cb[i][j] - 128)


out2 = (np.dstack((r2, g2, b2))).astype(np.uint8)


#--① 컬러 스케일을 BGR에서 YUV로 변경
img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) 
#--② YUV 컬러 스케일의 첫번째 채널에 대해서 이퀄라이즈 적용
img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0]) 
#--③ 컬러 스케일을 YUV에서 BGR로 변경
img2 = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) 
cv2.imshow("histo",img2)


d=PSNR(img,img2)
d2=PSNR(img,com)
print("내장함수를 사용해 구한 psnr : ",d)
print("직접 함수를 통해 구한 psnr : ",d2)
print("yuv : ",y)
print("yuv_gray : ",img_y)

cv2.waitKey()