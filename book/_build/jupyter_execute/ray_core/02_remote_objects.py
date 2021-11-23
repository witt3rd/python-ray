#!/usr/bin/env python
# coding: utf-8

# # Pattern: distributed objects
# 
# Remote objects:
# - distributed shared-memory object store
# - think: passing variables across the cluster
# - Ray will do object spilling to disk if needed
# 
# In Ray, we can create and compute on objects. We refer to these objects as remote objects, and we use object refs to refer to them. Remote objects are stored in shared-memory object stores, and there is one object store per node in the cluster. In the cluster setting, we may not actually know which machine each object lives on.
# 
# An object ref is essentially a unique ID that can be used to refer to a remote object. If you’re familiar with futures, our object refs are conceptually similar.
# 
# Object refs can be created in multiple ways:
# - by remote function calls
# - by `ray.put()`

# In[1]:


import ray
import logging
import time

# Start Ray. If you're connecting to an existing cluster, you would use ray.init(address=<cluster-address>) instead.
ray.init(
    num_cpus=4,
    num_gpus=1,
    resources={'Custom': 2},
    ignore_reinit_error=True,
    logging_level=logging.ERROR,
)
ray.cluster_resources()                    # get the cluster resources


# ## Single object refs
# 
# Simple `put()` / `get()`.

# In[8]:


y = 1
obj_ref = ray.put(y)
result = ray.get(obj_ref)
print(f"{result=}")
assert result == y


# ## Multiple object refs
# 
# Parallel `put()` / `get()`.

# In[9]:


result = ray.get([ray.put(i) for i in range(3)])
print(f"{result=}")
assert result == [0, 1, 2]


# ## Timing out
# 
# You can timeout to return early from a `get()` that's blocking for too long.

# In[3]:


from ray.exceptions import GetTimeoutError

@ray.remote
def long_running_function():
    time.sleep(8)

obj_ref = long_running_function.remote()
try:
    ray.get(obj_ref, timeout=4)
except GetTimeoutError:
    print("`get` timed out.")


# ## Waiting without blocking
# 
# After launching a number of tasks, you may want to know which ones have finisihed executing.

# In[7]:


@ray.remote
def long_running_function():

    duration = 1 + 10 * ray.random_uniform.remote()
    time.sleep(duration)
    value = ray.random_uniform.remote() 
    return value


object_refs = [long_running_function.remote() for _ in range(10)]
ready_refs, remaining_refs = ray.wait(
    object_refs, num_returns=len(object_refs))
print(f"{ready_refs=}")
print(f"{remaining_refs=}")

