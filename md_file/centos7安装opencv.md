1. yum -y update

2. yum -y install cmake

3. yum -y install git

4. yum install gcc gcc-c++ kernel-devel -y

5. yum install gcc-gfortran -y 

6. yum install libgnomeui-devel -y

7. yum install gtk2 gtk2-devel gtk2-devel-docs -y

8. yum install gnome-devel gnome-devel-docs  -y

9. cd /opt/pkg

10. wget http://pkgconfig.freedesktop.org/releases/pkg-config-0.29.2.tar.gz 

11. tar xvf pkg-config-0.29.2.tar.gz

12.  cd pkg-config-0.29.2

13. ./configure --prefix=/usr/local/pkg-config --with-internal-glib

14. make

15. make install

16. yum -y install epel-release

17. yum localinstall –nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm 

18. yum localinstall –nogpgcheck https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm 

19. rpm –import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro

20. rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm

21. yum -y install ffmpeg ffmpeg-devel

22. yum install python-devel numpy

23. yum install libdc1394-devel

24. yum install libv4l-devel

25. yum install gstreamer-plugins-base-devel

26. opencv源码编译

27. cd opencv 

28. mkdir build  

29. cd build

30. yum -y install gedit

31. vim /home/name/opencv/3rdparty/ippicv/ippicv.cmake

32.  #记得lc换成自己的用户名
    将47行的       "https://raw.githubusercontent.com/opencv/opencv_3rdparty/${IPPICV_COMMIT}/ippicv/"

33. 改为步骤1中手动下载的文件的本地路径：

    "file:///home/lc/下载/" #（仅供参考，根据自己的路径填写）


31. cmake -D WITH_TBB=ON -D WITH_EIGEN=ON ..   
32. cmake -D BUILD_DOCS=ON -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF ..   
33. cmake -D WITH_OPENCL=OFF -D WITH_CUDA=OFF -D BUILD_opencv_gpu=OFF -D BUILD_opencv_gpuarithm=OFF -D BUILD_opencv_gpubgsegm=OFF -D BUILD_opencv_gpucodec=OFF -D BUILD_opencv_gpufeatures2d=OFF -D BUILD_opencv_gpufilters=OFF -D BUILD_opencv_gpuimgproc=OFF -D BUILD_opencv_gpulegacy=OFF -D BUILD_opencv_gpuoptflow=OFF -D BUILD_opencv_gpustereo=OFF -D BUILD_opencv_gpuwarping=OFF ..    
34. cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..  
35. make
36. sudo  make install
37. cd /etc/ld.so.conf.d
38. touch opencv.conf
39. /bin/bash -c 'echo "/usr/local/lib64" > /etc/ld.so.conf.d/opencv.conf'
40. ldconfig
41. vim /etc/bashrc
42. 在文件末尾另起行加入
43. PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig 
44. export PKG_CONFIG_PATH
45. 保存退出
46. source /etc/bashrc
47. updatedb
48. cd  /usr/lib/
49. mkdir pkgconfig
50. cp /usr/local/lib64/pkgconfig/opencv.pc /usr/lib/pkgconfig
51. echo "#ADD OpenCV in PKG_CONFIG" >> ~/.bashrc
52. echo "PKG_CONFIG_PATH=/usr/lib/pkgconfig:${PKG_CONFIG_PATH}" >> ~/.bashrc
53. echo "export PKG_CONFIG_PATH" >> ~/.bashrc
54. source ~/.bashrc
55. 

