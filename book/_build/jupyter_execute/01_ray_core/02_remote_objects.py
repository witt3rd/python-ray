#!/usr/bin/env python
# coding: utf-8

# In[1]:





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

# Start Ray. If you're connecting to an existing cluster, you would use
# ray.init(address=<cluster-address>) instead.
ray.init(
    num_cpus=4,
    ignore_reinit_error=True,              # Don't print error messages if a Ray instance is already running. Attach to it
    logging_level=logging.ERROR,           
)
ray.cluster_resources()                    # get the cluster resources


# ## Example 1
# 
# Simple `put()` / `get()`.

# In[4]:


y = 1
obj_ref = ray.put(y)
assert ray.get(obj_ref) == y


# ## Example 2
# 
# Parallel `put()` / `get()`.

# In[3]:


result = ray.get([ray.put(i) for i in range(3)])
assert result == [0, 1, 2]

