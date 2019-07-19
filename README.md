# tf-pose-estimation

# Install in TX2

## 刷机
教程：https://blog.csdn.net/DeepWolf/article/details/88640937 <br>
使用的是Jetpack 3.3 <br>
对应的CUDA:9.0， cudnn:7

## 配置此工程需要的依赖
pip2库版本见 [pip2_list.txt](./pip2_list.txt) <br>
ROS下只使用python2和pip2

### 一些较难安装的库参考
scipy: https://blog.csdn.net/whitesilence/article/details/70338056 <br>
numba: https://blog.csdn.net/m0_37167788/article/details/90898236 <br>
backports.functools_lru_cache: https://pypi.org/project/backports.functools_lru_cache/1.0.1/
## Install tensorflow
教程：https://blog.csdn.net/zhangziju/article/details/85252474

使用二进制直接安装GPU版本即可，即 <br>
`
$: pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp33 tensorflow-gpu
` <br>
当前为tensorflow 1.9

## Install ROS
教程： https://blog.csdn.net/Kamfai_Row/article/details/89409386#ROS_Kinetic__154

## Install realsense D435
教程： http://blog.leanote.com/post/bsw_is_u@163.com/TX2%E5%AE%89%E8%A3%85intel-realsense-D435%E5%8F%8AROS-%E4%B8%8BD435%E7%9A%84%E5%90%AF%E5%8A%A8

**如果不能使用，则试下其他版本，如<realsense ros: v2.2.5, librealsense: v2.22.0>**

## 分配交换空间
TX2内存空间不够用，需要交换空间 <br>
教程：https://cloud.tencent.com/developer/article/1342505

## How to use
1. 使用前开启超频模式:
`./jetson_clocks.sh` <br>
2. `roslaunch tfpose_ros realsense_video.launch `
## 其他

### 安装teamviewer
https://blog.csdn.net/jacke121/article/details/94001148

### TX2 GPU使用情况查看工具
https://blog.csdn.net/weixin_43640369/article/details/87341875

### tx2 commands
https://blog.csdn.net/haoqimao_hard/article/details/80516828

## master branch installation change

```
Build c++ library for post processing. See : https://github.com/ildoonet/tf-pose-estimation/tree/master/tf_pose/pafprocess
```
$ cd tf_pose/pafprocess
$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```
对于在ROS下使用c++ library情况下，python3改为python2
```
$ swig -python -c++ pafprocess.i && python2 setup.py build_ext --inplace


