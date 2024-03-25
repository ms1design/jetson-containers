from jetson_containers import CUDA_ARCHITECTURES, CUDA_VERSION
    
package['build_args'] = {
    'TENSORRT_LLM_BRANCH': 'main',
    'CUDA_ARCHS': ';'.join([f'{x}-real' for x in CUDA_ARCHITECTURES]),
    'CUDA_VERSION': CUDA_VERSION,
    'CUDA_VERSION_MAJOR': CUDA_VERSION.major,
    'CUDA_VERSION_MINOR': CUDA_VERSION.minor,
}
