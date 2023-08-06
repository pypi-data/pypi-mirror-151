# Start from the base version of many linux from PyPA 
FROM quay.io/pypa/manylinux1_x86_64
# Install cython and pathlib
RUN for i in $(ls /opt/python); do /opt/python/$i/bin/pip install cython pathlib; done

