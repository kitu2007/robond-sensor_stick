import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

image = mpimg.imread('Udacian.jpeg')
plt.imshow(image)

r_hist = np.histogram(image[:,:,0], bins=32, range=(0,256))
g_hist = np.histogram(image[:,:,1], bins=32, range=(0,256))
b_hist = np.histogram(image[:,:,2], bins=32, range=(0,256))

# generating bin centers
bin_edges = r_hist[1]
bin_centers = (bin_edges[1:]) + bin_edges[0:len(bin_edges)-1])/2

# plot a figure with all three bar charts
fig = plt.figure(figsize=(12,3))
plt.subplot(131)
plt.bar(bin_centers, r_hist[0])
plt.xlim(0,256)
plt.title('R Histograms')
plt.subplot(132)
plt.bar(bin_centers, g_hist[0])
plt.xlim(0,256)
plt.title('G Histograms')
plt.subplot(133)
plt.bar(bin_centers, b_hist[0])
plt.xlim(0,256)
plt.title('G Histograms')
plt.show()

hist_features = np.concatenate((r_hist[0],g_hist[0],b_hist[0])).astype(np.float64)
norm_features = hist_features / np.sum(hist_features)

def color_hist(img, nbins=32, bins_range=(0,256)):
    # Convert from RGB to HSV using cv2.cvtColor()
    hsv = cv2.cvtColor(img, cv2.RGB2HSV)
    # Compute histogram of HSV channels separately
    h_hist = np.histogram(hsv[0], bins = nbins, range = bin_range)
    s_hist = np.histogram(hsv[1], bins = nbins, range = bin_range)
    v_hist = np.histogram(hsv[2], bins = nbins, range = bin_range)

    hist_features = np.concatenate((h_hist[0],s_hist[0],v_hist[0])).astype(np.float64)
    norm_features = hist_features / np.sum(hist_features)
    return norm_features



from sklearn import svm
np.random.seed(424)
n_clusters=5


