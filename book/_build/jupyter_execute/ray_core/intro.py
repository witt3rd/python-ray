#!/usr/bin/env python
# coding: utf-8

# # Ray Core
# 
# A [pattern language](https://patterns.eecs.berkeley.edu/) for distibuted systems as a library in Python, Java, and C++.
# 
# - [remote functions: tasks](tasks.ipynb) - stateless, data independence
# - [remote objects](remote_objects.ipynb) - key/value store
# - [remote classes: actor pattern](actors.ipynb) - messages among classes, managing state
# - **parallel iterators** - lazy, infinite sequences
# - `multiprocessing.Pool` - drop-in replacement
# - `joblib` - e.g., _scikit-learn_ back-end
# - Dask, Modin, Mars, etc.
# 
# Mix and match as needed, without tight coupling to framework

# ## Just Six API Methods
# 
# Almost everything you do with Ray is done with just six API methods:
# 
# - [`ray.init()`](https://docs.ray.io/en/latest/package-ref.html#ray-init)
# - [`ray.get()`](https://ray.readthedocs.io/en/latest/package-ref.html#ray.get)
# - [`ray.put()`](https://ray.readthedocs.io/en/latest/package-ref.html#ray.put)
# - [`ray.remote()`](https://ray.readthedocs.io/en/latest/package-ref.html#ray.remote)
# - [`ray.wait()`](https://ray.readthedocs.io/en/latest/package-ref.html#ray.wait)
# - [`ray.shutdown()`](https://ray.readthedocs.io/en/latest/package-ref.html#ray.shutdown)

# ## Background
# 
# Ray makes use of:
# - [closures and decorators in Python](https://towardsdatascience.com/closures-and-decorators-in-python-2551abbc6eb6) ([PEP 318](https://www.python.org/dev/peps/pep-0318/))
# - [futures and promises in Python](http://dist-prog-book.com/chapter/2/futures.html#introduction)
# - [asyncio in Python](https://docs.python.org/3/library/asyncio-task.html)

# ## References
# 
# - [Ray Core Tutorial](https://youtu.be/_KOlq2C-568) ([source code](https://github.com/derwenai/ray_tutorial)) ([slides](https://github.com/DerwenAI/ray_tutorial/blob/main/slides/slides.pdf))
# - [Modern Parallel and Distributed Python: A Quick Tutorial on Ray](https://towardsdatascience.com/modern-parallel-and-distributed-python-a-quick-tutorial-on-ray-99f8d70369b8)
# - [Anyscale Academy: Ray Crash Course - 03 Why Ray](https://github.com/anyscale/academy/blob/main/ray-crash-course/03-Why-Ray.ipynb)
# 
