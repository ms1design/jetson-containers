#---
# name: tensorrt_llm
# group: llm
# config: config.py
# depends: [python, pytorch, optimum, tensorrt, tritonserver]
# test: [test.py, test_python_benchmark.sh, test_cpp_benchmark.sh]
# requires: '>=35'
# notes: The `tensorrt-llm` wheel that's built is saved in the container under `/opt`. Based on https://zhuanlan.zhihu.com/p/663915644
#---

ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG TENSORRT_LLM_BRANCH \
    TORCH_CUDA_ARCH_LIST \
    CUDA_ARCHS \
    CUDA_VERSION \
    CUDA_VERSION_MAJOR \
    CUDA_VERSION_MINOR \
    TRT_TARGETARCH="aarch64" \
    SRC_DIR="/tmp/TensorRT-LLM" \
    DIST_DIR="/opt/tensorrt_llm" \
    CPP_BUILD_DIR="/opt/tensorrt_llm/cpp/build"

# Install build dependencies and clone repository
RUN set -ex \
    && git clone --branch=${TENSORRT_LLM_BRANCH} --depth=1 https://github.com/NVIDIA/TensorRT-LLM.git ${SRC_DIR} \
    && git -C ${SRC_DIR} submodule update --init --recursive \
    && git -C ${SRC_DIR} lfs pull

# Apply sed commands
RUN set -ex \
    && sed -i \
        -e 's|^torch.*|torch|g' \
        -e 's|^tensorrt.*|tensorrt|g' \
        -e 's|^transformers.*|transformers|g' \
        -e 's|^sentencepiece.*|sentencepiece|g' \
        -e 's|^diffusers.*|diffusers|g' \
        -e 's|^accelerate.*|accelerate|g' \
        ${SRC_DIR}/requirements.txt \
    && sed -i \
        -e 's|${NCCL_LIB}||g' \
        ${SRC_DIR}/cpp/tensorrt_llm/CMakeLists.txt \
        ${SRC_DIR}/cpp/tensorrt_llm/plugins/CMakeLists.txt \
    && sed -i \
        -e "s|CUDA_VER=\"[^\"]*\"|CUDA_VER=\"$CUDA_VERSION_MAJOR.$CUDA_VERSION_MINOR\"|g" \
        -e 's|^    install_ubuntu_requirements||g' \
        ${SRC_DIR}/docker/common/install_tensorrt.sh \
    && sed -i '96d' ${SRC_DIR}/docker/common/install_tensorrt.sh \
    \
    # Install TensorRT 9.x \
    # TODO: Move logic to tensorrt container config.py
    && chmod +x ${SRC_DIR}/docker/common/install_*.sh \
    && ${SRC_DIR}/docker/common/install_tensorrt.sh

ENV LD_LIBRARY_PATH=/usr/local/tensorrt/lib:${LD_LIBRARY_PATH}

RUN set -ex \
    # Build TensorRT-LLM \
    && echo "CUDA_VERSION: ${CUDA_VERSION}" \
    && echo "CUDA_ARCHS: ${CUDA_ARCHS}" \
    && ${SRC_DIR}/docker/common/install_polygraphy.sh \
    && ${SRC_DIR}/docker/common/install_mpi4py.sh \
    && python3 ${SRC_DIR}/scripts/build_wheel.py \
        --clean \
        --build_type Release \
        --cuda_architectures "${CUDA_ARCHS}" \
        --build_dir ${CPP_BUILD_DIR} \
        --dist_dir /opt \
        --trt_root /usr/local/tensorrt \
        --extra-cmake-vars "ENABLE_MULTI_DEVICE=OFF" \
        --benchmarks \
        --python_bindings

RUN set -ex \
    # Copy necessary files \
    && cp -r ${SRC_DIR}/cpp/include ${DIST_DIR}/include \
    && cp -r ${SRC_DIR}/benchmarks ${DIST_DIR}/benchmarks \
    && cp ${CPP_BUILD_DIR}/benchmarks/bertBenchmark ${DIST_DIR}/benchmarks/cpp/ \
    && cp ${CPP_BUILD_DIR}/benchmarks/gptManagerBenchmark ${DIST_DIR}/benchmarks/cpp/ \
    && cp ${CPP_BUILD_DIR}/benchmarks/gptSessionBenchmark ${DIST_DIR}/benchmarks/cpp/ \
    && cp -r ${SRC_DIR}/docs ${DIST_DIR}/docs \
    && cp -r ${SRC_DIR}/examples ${DIST_DIR}/examples \
    && chmod -R a+w ${DIST_DIR}/examples \
    \
    # Install TensorRT-LLM package \
    && pip3 install --no-cache-dir --verbose /opt/tensorrt_llm*.whl --extra-index-url https://pypi.nvidia.com \
    \
    # Symlink shared libraries \
    && ln -sv $(python3 -c 'import site; print(f"{site.getsitepackages()[0]}/tensorrt_llm/libs")') ${DIST_DIR}/lib \
    && test -f ${DIST_DIR}/lib/libnvinfer_plugin_tensorrt_llm.so \
    && ln -sv ${DIST_DIR}/lib/libnvinfer_plugin_tensorrt_llm.so ${DIST_DIR}/lib/libnvinfer_plugin_tensorrt_llm.so.9 \
    && echo "${DIST_DIR}/lib" > /etc/ld.so.conf.d/tensorrt_llm.conf \
    && ldconfig -v | grep nvinfer \
    \
    # test \
    && pip3 show tensorrt_llm \
    && python3 -c 'import tensorrt_llm' \
    \
    # Cleanup unnecessary files \
    && rm -rfv \
        ${SRC_DIR} \
        /opt/*.whl \
        ${DIST_DIR}benchmarks/cpp/bertBenchmark.cpp \
        ${DIST_DIR}benchmarks/cpp/gptManagerBenchmark.cpp \
        ${DIST_DIR}benchmarks/cpp/gptSessionBenchmark.cpp \
        ${DIST_DIR}benchmarks/cpp/CMakeLists.txt
