#!/usr/bin/env bash

set -ex

mkdir -p /opt/tensorrt_llm/benchmarks/trt_engines/gpt_350m

echo "testing python benchmark..."

python3 /opt/tensorrt_llm/benchmarks/python/benchmark.py \
    -m gpt_350m \
    --mode plugin \
    --batch_size "1;8;64" \
    --input_output_len "60,20;128,20" \
    --log_level verbose \
    --output_dir /opt/tensorrt_llm/benchmarks/trt_engines/gpt_350m \
    --enable_cuda_graph \
    --strongly_typed

echo "python benchmark OK"
