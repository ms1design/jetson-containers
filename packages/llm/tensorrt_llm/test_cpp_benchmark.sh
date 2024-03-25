#!/usr/bin/env bash

set -ex

echo "testing cpp benchmark..."

cd /opt/tensorrt_llm/cpp/build

echo "testing cpp gptSessionBenchmark gpt_350m..."

./benchmarks/gptManagerBenchmark --help

./benchmarks/gptSessionBenchmark \
    --engine_dir /opt/tensorrt_llm/benchmarks/trt_engines/gpt_350m \
    --batch_size "1" \
    --input_output_len "60,20"

echo "cpp gptSessionBenchmark gpt_350m OK"


echo "cpp benchmark OK"
