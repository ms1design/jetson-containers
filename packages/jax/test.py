#!/usr/bin/env python3
print('Testing JAX...')

import jax
import jax.numpy as jnp
from jax import random
import os

# Print JAX version and CUDA device information
print('JAX version: ' + str(jax.__version__))
print('CUDA devices: ' + str(jax.devices()))

# Fail if CUDA isn't available
assert len(jax.devices()) > 0, 'No CUDA devices found'

# Check that version can be parsed
from packaging import version

print('PACKAGING_VERSION=' + str(version.parse(jax.__version__)))
print('JAX_CUDA_ARCH_LIST=' + os.environ.get('JAX_CUDA_ARCH_LIST', 'None') + '\n')

# Quick CUDA tensor test
key = random.PRNGKey(0)
a = jnp.zeros(2)
print('Tensor a = ' + str(a))

b = random.normal(key, (2,))
print('Tensor b = ' + str(b))

c = a + b
print('Tensor c = ' + str(c))

# LAPACK test
print('Testing LAPACK (via jax.numpy.linalg)...')
a = random.normal(key, (4, 4))
b = random.normal(key, (4, 4))

x = jnp.linalg.solve(b, a)

print('Done testing LAPACK (via jax.numpy.linalg)\n')

# Neural network test
print('JAX OK\n')
