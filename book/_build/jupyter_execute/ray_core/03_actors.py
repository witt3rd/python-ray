#!/usr/bin/env python
# coding: utf-8

# # Actor Pattern

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

# In[7]:


@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 1

    def read(self):
        return self.n


counters = [Counter.remote() for i in range(4)]
[c.increment.remote() for c in counters]
futures = [c.read.remote() for c in counters]
print(ray.get(futures))  # [1, 1, 1, 1]


# ![Ray Head and Worker Nodes](../images/ray_head_worker_nodes.jpg)
