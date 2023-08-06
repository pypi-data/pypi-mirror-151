import numpy as np
from scipy import interpolate, signal
from scipy.fftpack import fft, ifft, fftshift
# data 数据数组
# signalqualityminthre 睡前 1 睡中 0.5 正常的数据有时候幅值是比较低
# perindex 睡前 0.7 睡中 0.8
def signalquaily(data, signalqualityminthre, perindex):
	fs = 250
	# data 为 6s 的数据
	L = len(data)
	# datatest = band_pass(data, [1,30])
	data = DFA_3(data,int(L/25)+1)  # 去趋势
	data = low_pass(data) # 去除不必要的高频信息
	data = band_stop(data, [48, 52]) # 去除工频干扰

	# 幅值判断 + 异常冲击判断
	# 滑窗检测 统计百分比 通过
	windowlength = int(L/3)
	windowstep = int(L/10)
	num = int(L/windowstep)
	datanew = np.append(data, np.zeros(windowlength))
	signalqualitymaxthre = 200

	numindex = []
	for i in range(num):
		temp = datanew[i*windowstep:i*windowstep+windowlength]
		analytic_temp = signal.hilbert(temp)
		env_temp = np.abs(analytic_temp)
		env_temp = smooth(env_temp, int(windowlength / 25)+1 )
		# print(np.mean(env_temp[:]))
		if np.mean(env_temp[:]) > signalqualityminthre and np.max(env_temp[:]) < signalqualitymaxthre:
			numindex.append(1)
		else:
			numindex.append(0)
	Perindex = sum(numindex)/len(numindex)

	# 对脑电波形的判断 脑电波应该在0.5-45的区间内具有很高的能量比 其余的部分应该没有

	fl_fft = np.abs(fftshift(fft(data)))
	fl_spectrum = fl_fft[int(len(fl_fft) / 2 + 1):] ** 2
	fbin = (fs / 2) / len(fl_spectrum)
	EEGLen = int(np.ceil(40 / fbin)) - int(np.ceil(0.5 / fbin))
	restLen = len(fl_spectrum) - EEGLen
	EEG_power_fl = np.sum(fl_spectrum[int(np.ceil(0.5 / fbin)):int(np.ceil(40 / fbin))]) / EEGLen
	rest_power_fl = (np.sum(fl_spectrum) - np.sum(fl_spectrum[int(np.ceil(0.5 / fbin)):int(np.ceil(40 / fbin))])) / restLen
	Powerindex = np.log(rest_power_fl / EEG_power_fl)

	# 如果出现范围内具有单一频率成分的现象 那么应当被拒绝掉 信号需要通过平稳性检验
	# 这个直接当作工频干扰去掉

	if Perindex >= perindex and Powerindex < 0: # 睡中 0.8 睡前 0.7
		return True
	else:
		return False

def smooth(a, WSZ):
	# a:原始数据，NumPy 1-D array containing the data to be smoothed
	# 必须是1-D的，如果不是，请使用 np.ravel()或者np.squeeze()转化
	# WSZ: smoothing window size needs, which must be odd number,
	# as in the original MATLAB implementation
	out0 = np.convolve(a, np.ones(WSZ, dtype=int), 'valid') / WSZ
	r = np.arange(1, WSZ - 1, 2)
	start = np.cumsum(a[:WSZ - 1])[::2] / r
	stop = (np.cumsum(a[:-WSZ:-1])[::2] / r)[::-1]
	return np.concatenate((start, out0, stop))

def band_stop(data, coe, sf=250):
	b, a = signal.butter(2, [coe[0] * 2/sf, coe[1] * 2/sf], 'bandstop')
	filteredData = signal.filtfilt(b, a, data, padlen=0)

	return filteredData
def low_pass(data, sf=250):
	b, a = signal.butter(2, 2 * 45 / sf, 'lowpass')
	filteredData = signal.filtfilt(b, a, data, padlen=0)

	return filteredData
def DFA_3(Epoch, window):
	# 新的去趋势方法
	# window 默认值为199
	trend = signal.savgol_filter(Epoch, window, 3)
	signal_Clean = Epoch - trend
	return signal_Clean
def print_ok():
	print('hello world')
