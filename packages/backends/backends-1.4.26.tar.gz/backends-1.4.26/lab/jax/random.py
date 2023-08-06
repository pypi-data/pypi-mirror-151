import jax
from plum import Dispatcher, Union

from . import dispatch, B
from ..types import Int, JAXDType, JAXNumeric, JAXRandomState

__all__ = []

_dispatch = Dispatcher()


@dispatch
def create_random_state(_: JAXDType, seed: Int = 0):
    return jax.random.PRNGKey(seed=seed)


B.jax_global_random_state = jax.random.PRNGKey(seed=0)


@dispatch
def global_random_state(_: JAXDType):
    return B.jax_global_random_state


@dispatch
def set_global_random_state(state: JAXRandomState):
    B.jax_global_random_state = state


@dispatch
def rand(state: JAXRandomState, dtype: JAXDType, *shape: Int):
    state, key = jax.random.split(state)
    return state, B.to_active_device(jax.random.uniform(key, shape, dtype=dtype))


@dispatch
def rand(dtype: JAXDType, *shape: Int):
    state, res = rand(global_random_state(dtype), dtype, *shape)
    B.jax_global_random_state = state
    return res


@dispatch
def randn(state: JAXRandomState, dtype: JAXDType, *shape: Int):
    state, key = jax.random.split(state)
    return state, B.to_active_device(jax.random.normal(key, shape, dtype=dtype))


@dispatch
def randn(dtype: JAXDType, *shape: Int):
    state, res = randn(global_random_state(dtype), dtype, *shape)
    B.jax_global_random_state = state
    return res


@dispatch
def choice(
    state: JAXRandomState,
    a: JAXNumeric,
    n: Int,
    *,
    p: Union[JAXNumeric, None] = None,
):
    state, key = jax.random.split(state)
    # Feeding `a` to `choice` will not work if `a` is higher-dimensional.
    inds = jax.random.choice(key, a.shape[0], (n,), replace=True, p=p)
    choices = a[inds]
    return state, choices[0] if n == 1 else choices


@dispatch
def choice(a: JAXNumeric, n: Int, *, p: Union[JAXNumeric, None] = None):
    state, res = choice(global_random_state(a), a, n, p=p)
    B.jax_global_random_state = state
    return res


@dispatch
def randint(
    state: JAXRandomState,
    dtype: JAXDType,
    *shape: Int,
    lower: Int = 0,
    upper: Int,
):
    dtype = B.dtype_int(dtype)
    state, key = jax.random.split(state)
    return state, B.to_active_device(
        jax.random.randint(key, shape, lower, upper, dtype=dtype)
    )


@dispatch
def randint(
    dtype: JAXDType,
    *shape: Int,
    lower: Int = 0,
    upper: Int,
):
    state, res = randint(
        global_random_state(dtype),
        dtype,
        *shape,
        lower=lower,
        upper=upper,
    )
    B.jax_global_random_state = state
    return res


@dispatch
def randperm(state: JAXRandomState, dtype: JAXDType, n: Int):
    dtype = B.dtype_int(dtype)
    state, key = jax.random.split(state)
    return state, B.to_active_device(B.cast(dtype, jax.random.permutation(key, n)))


@dispatch
def randperm(dtype: JAXDType, n: Int):
    state, res = randperm(global_random_state(dtype), dtype, n)
    B.jax_global_random_state = state
    return res
