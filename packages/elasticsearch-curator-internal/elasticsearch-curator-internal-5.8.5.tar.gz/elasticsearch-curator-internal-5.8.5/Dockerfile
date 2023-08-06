FROM python:3.9.4-alpine3.13 as builder

# Add the community repo for access to patchelf binary package
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/v3.13/community/' >> /etc/apk/repositories
RUN pip install --upgrade pip
RUN apk --no-cache upgrade && apk --no-cache add build-base tar musl-utils openssl-dev patchelf
# patchelf-wrapper is necessary now for cx_Freeze, but not for Curator itself.
RUN pip3 install setuptools wheel cx_Freeze patchelf-wrapper

COPY . .
RUN ln -s /lib/libc.musl-x86_64.so.1 ldd
RUN ln -s /lib /lib64
RUN pip3 install -r requirements.txt
RUN python3 setup.py build_exe

FROM python:3.9.4-alpine3.13
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/v3.13/community/' >> /etc/apk/repositories
RUN apk --no-cache upgrade && apk --no-cache add openssl-dev expat && apk --no-cache add wget && apk --no-cache add curl
COPY . /tmp/
RUN pip install --upgrade pip
RUN pip3 install prometheus_client elasticsearch
#RUN pip3 install -e /tmp
COPY --from=builder build/exe.linux-x86_64-3.9 /curator/
RUN mkdir /.curator

ENV LD_LIBRARY_PATH /curator/lib:$LD_LIBRARY_PATH
ENTRYPOINT ["/curator/curator"]

