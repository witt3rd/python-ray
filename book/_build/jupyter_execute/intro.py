#!/usr/bin/env python
# coding: utf-8

# # Ray: Cloud Native Distributed Computing Platform

# ##### Core Links
# - [ray.io](https://www.ray.io/)
# - [docs.ray.io](https://docs.ray.io/)
# - [github/ray-project](github.com/ray-project/ray)
# 
# ##### Papers and Posts
# - [Cloud Programming Simplified: A Berkeley View on Serverless Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2019/EECS-2019-3.pdf)
# - [Ray 1.x Architecture](https://docs.google.com/document/d/1lAy0Owi-vPz2jEqBSaHNQcy2IBSDEHyXNOQZlGuj93c/preview)
# - [Modern Parallel and Distributed Python: A Quick Tutorial on Ray](https://towardsdatascience.com/modern-parallel-and-distributed-python-a-quick-tutorial-on-ray-99f8d70369b8)
# - [Combine the development experience of a laptop with the scale of the cloud](https://gradientflow.com/combine-the-development-experience-of-a-laptop-with-the-scale-of-the-cloud/)
# 
# ##### Videos
# - [Ray Core Tutorial](https://youtu.be/_KOlq2C-568) ([source code](https://github.com/derwenai/ray_tutorial)) ([slides](papers/Ray_Core_Tutorial.pdf))

# ## Ray is:
# 
# 1. A simple and flexible framework for distributed cloud computing
#     - Simple: simple annotation to make functions & classes distribute.
#     - Flexible: create new distributed function calls & instances.  No batching required.
# 2. A cloud-provider independent compute launcher/autoscaler
# 3. An ecosystem of distributed computation libraries build with #1

# ## How does it "fit" with ML?
# 
# [3rd generation ML architecture](https://www.anyscale.com/blog/the-third-generation-of-production-ml-architectures): tackling the problem of production ML architecure by making it programmable.
# 
# Moves the focus to libraries instead of worried about distributed computation and underlying clusters.

# ## A simpler way to build 1st/2nd generation ML pipelines
# 
# - Flexibility of a programming language to define pipelines
# - More easily allows for shared components (e.g., feature transformation during training vs real-time)
# - "Out of the box" support for distributed ML

# ## Ray Core
# 
# A [pattern language](https://patterns.eecs.berkeley.edu/) for distibuted systems as a library in Python, Java, and C++.
# 
# - **task-parallel** - stateless, data independence
# - **remote objects** - key/value store
# - **actor pattern** - messages among classes, managing state
# - **parallel iterators** - lazy, infinite sequences
# - `multiprocessing.Pool` - drop-in replacement
# - `joblib` - e.g., _scikit-learn_ back-end
# - Dask, Modin, Mars, etc.
# 
# Mix and match as needed, without tight coupling to framework

# ### Background
# 
# Ray makes use of:
# - [closures and decorators in Python](https://towardsdatascience.com/closures-and-decorators-in-python-2551abbc6eb6) ([PEP 318](https://www.python.org/dev/peps/pep-0318/))
# - [futures and promises in Python](http://dist-prog-book.com/chapter/2/futures.html#introduction)
# - [asyncio in Python](https://docs.python.org/3/library/asyncio-task.html)

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


# ### Pattern: task-parallel (remote functions)
# 
# - add `@ray.remote` decorator on a regular Python function
# - properties: _data independence_, _stateless_
# - patterns: [Task Parallelism](https://patterns.eecs.berkeley.edu/?page_id=208), [Task Graph](https://patterns.eecs.berkeley.edu/?page_id=609)
# - [Ray Internals: A Peek at `ray.get` - Stephanie Wang, Anyscale](https://www.youtube.com/watch?v=a1kNnQu6vGw)
# - [Ray Internals: Object Management with the Ownership Model](https://youtu.be/1oSBxTayfJc) ([slides](https://speakerdeck.com/anyscale/ray-internals-object-management-with-the-ownership-model-stephanie-wang-and-yi-cheng-anyscale))
# - reference: [Patterns for Parallel Programming](https://www.goodreads.com/book/show/85053.Patterns_for_Parallel_Programming)

# #### Example 1
# 
# Simple remote function (task).

# In[6]:


# A regular Python function can be decorated with @ray.remote
@ray.remote
def f(x):
    return x * x

# The function can be invoked by using the `remote` method
futures = [f.remote(i) for i in range(4)]

# The values it returns can be collected using the `get` method.
print(ray.get(futures))  # [0, 1, 4, 9]


# #### Example 2
# 
# Parallel task execution and blocking on futures (object refs).

# In[23]:


# A function simulating a more interesting computation that takes one second.
@ray.remote
def slow_function(i):
    time.sleep(1)
    return i

start_time = time.perf_counter()

results = []
for i in range(4):
  results.append(slow_function.remote(i))

duration = time.perf_counter() - start_time
print('Executing the for loop took {:.3f} seconds.'.format(duration))

results = ray.get(results)
print('The results are:', results)

assert results == [0, 1, 2, 3], 'Did you remember to call ray.get?'

duration = time.perf_counter() - start_time
print('Executing the example took {:.3f} seconds.'.format(duration))


# #### Exercise 
# 
# Use the UI to view the task timeline and to verify that the four tasks were executed in parallel. You can do this as follows.
# 
# 1. Run the following cell to generate a JSON file containing the profiling data.
# 2. Download the timeline file by right clicking on `task_parallel_ex_2.json` in the **Files** tab in the navigator to the left, right clicking, and selecting  **"Download"**.
# 3. Enter **chrome://tracing** into the Chrome web browser, click on the **"Load"** button, and select the downloaded JSON file.
# 
# To navigate within the timeline:
# - Move around by clicking and dragging.
# - Zoom in and out by holding **alt** on Windows or **option** on Mac and scrolling.
# 
# **NOTE:** The timeline visualization will only work in **Chrome**.

# In[5]:


ray.timeline(filename="output/task_parallel_ex_2.json")


# #### Example 3
# 
# Passing object refs between tasks.

# In[ ]:


@ray.remote
def my_function():
    return 1

@ray.remote
def function_with_an_argument(value):
    return value + 1

obj_ref1 = my_function.remote()
assert ray.get(obj_ref1) == 1

# You can pass an object ref as an argument to another Ray remote function.
obj_ref2 = function_with_an_argument.remote(obj_ref1)
assert ray.get(obj_ref2) == 2


# ### Pattern: distributed objects
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

# ##### Example 1
# 
# Simple `put()` / `get()`.

# In[4]:


y = 1
obj_ref = ray.put(y)
assert ray.get(obj_ref) == y


# ##### Example 2
# 
# Parallel `put()` / `get()`.

# In[3]:


result = ray.get([ray.put(i) for i in range(3)])
assert result == [0, 1, 2]


# ### Actor Pattern

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


# ![Ray Head and Worker Nodes](images/ray_head_worker_nodes.jpg)
