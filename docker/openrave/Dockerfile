FROM debian:stretch
ENV PROJECT_NAME openrave
MAINTAINER osbertngok<osbertngok@gmail.com>


# git for cloning project
# cmake for building make file
# build-essential for g++
# various boost libraries

RUN apt -y update

RUN apt -y install git cmake build-essential libboost-dev libboost-thread-dev libboost-python-dev libboost-date-time-dev libboost-regex-dev libboost-filesystem-dev libboost-system-dev libxml2 libxml2-dev
RUN apt -y install pkg-config python-dev libqt4-dev libsoqt4-dev libpcre3-dev xvfb

RUN apt -y python-pip

RUN pip install scipy numpy

RUN git clone --depth=1 --branch sympy-0.7.5 https://github.com/sympy/sympy.git && cd sympy && python setup.py install

RUN git clone --depth=1 https://github.com/rdiankov/collada-dom.git && cd collada-dom && mkdir build && cd build && cmake ../ && make -j4 && make install

RUN git clone --depth=1 --branch master https://github.com/rdiankov/openrave.git && cd openrave && git checkout -qf master && mkdir build && cd build && cmake -OPT_VIDEORECORDING=OFF -OPT_PLUGINS=OFF -OPT_DOUBLE_PRECISION=OFF -OPT_ACCURATEMATH=OFF -OPT_PYTHON=ON -OPT_OCTAVE=OFF -OPT_MATLAB=OFF -OPT_STATIC=OFF -OPT_COLLADA=ON -OPT_BULLET=OFF -OPT_ODE_COLLISION=OFF -OPT_FCL_COLLISION=OFF ../ && make -j4 && make install

ENTRYPOINT ["./openrave/opernrave.py", "--example", "hanoi"]

