#!/usr/bin/env python
# coding: utf-8

# # Ray Core
# 
# A [pattern language](https://patterns.eecs.berkeley.edu/) for distibuted systems as a library in Python, Java, and C++.
# 
# - [task-parallel](01_tasks.ipynb) - stateless, data independence
# - [remote objects](02_remote_objects.ipynb) - key/value store
# - [actor pattern](03_actors.ipynb) - messages among classes, managing state
# - **parallel iterators** - lazy, infinite sequences
# - `multiprocessing.Pool` - drop-in replacement
# - `joblib` - e.g., _scikit-learn_ back-end
# - Dask, Modin, Mars, etc.
# 
# Mix and match as needed, without tight coupling to framework

# ## Background
# 
# Ray makes use of:
# - [closures and decorators in Python](https://towardsdatascience.com/closures-and-decorators-in-python-2551abbc6eb6) ([PEP 318](https://www.python.org/dev/peps/pep-0318/))
# - [futures and promises in Python](http://dist-prog-book.com/chapter/2/futures.html#introduction)
# - [asyncio in Python](https://docs.python.org/3/library/asyncio-task.html)
