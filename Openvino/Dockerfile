FROM openvino/ubuntu18_runtime:2020.2 as openvino_hackathon

USER root
ADD . /code
WORKDIR /code
RUN cd /code && \
    chmod 777 /code && \
    apt update && apt install -y libsm6 libxext6 && \
    apt-get install -y libxrender1 && \
    pip3 install -r requirements.txt

RUN /bin/bash -c "source /opt/intel/openvino/bin/setupvars.sh"

RUN echo "source /opt/intel/openvino/bin/setupvars.sh" >> /root/.bashrc

CMD ["sleep", "infinity"]