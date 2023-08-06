# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['just_jobs', 'just_jobs.brokers']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0', 'redis>=4.3.1,<5.0.0']

setup_kwargs = {
    'name': 'just-jobs',
    'version': '1.1.0',
    'description': 'A lightweight asynchronous Python job executor backed by Redis.',
    'long_description': '# just-jobs\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/thearchitector/just-jobs/CI?label=tests&style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/just-jobs?style=flat-square)\n![GitHub](https://img.shields.io/github/license/thearchitector/just-jobs?style=flat-square)\n[![Buy a tree](https://img.shields.io/badge/Treeware-%F0%9F%8C%B3-lightgreen?style=flat-square)](https://ecologi.com/eliasgabriel?r=6128126916bfab8bd051026c)\n\nA lightweight asynchronous Python job executor. Using Redis by default (but not exclusivly, via custom adapters), it is a smaller and production-ready alternative to Celery for applications where distributed microservices are overkill.\n\n## Usage\n\nDocumentation: <https://justjobs.thearchitector.dev>.\n\nThe entire execution structure consists of 3 things:\n\n- The `Manager`, which is responsible for managing the broker and all job queues.\n- The `Broker`, which is responsible for integrating into a storage interface and executing jobs.\n- A `job`, which is any non-dynamic function or coroutine that performs some task.\n\nIn general, the process for enqueue jobs for execution is always the same:\n\n1. Create a Manager and tell it to start listening for jobs via `await manager.startup()`.\n2. Anywhere in your application, enqueue a job via `manager.enqueue(job, *args, **kwargs)`.\n3. Ensure to properly shutdown your manager with `await manager.shutdown()`.\n\n### Example\n\nA common use case for delayed jobs is a web application, where milliseconds are important. Here is an example using FastAPI, whose startup and shutdown hooks make it easier for us to manage the state of our Manager.\n\n```py\nfrom fastapi import FastAPI\nfrom just_jobs import Manager\n\napp = FastAPI()\n\nasync def _essential_task(a, b):\n    """render a movie, or email a user, or both"""\n\n@app.on_event("startup")\nasync def startup():\n    # the default broker is backed by Redis via aioredis. Managers\n    # will always pass any args and kwargs it doesn\'t recognize to\n    # their brokers during startup.\n    manager = Manager(url="redis://important-redis-server/0")\n    app.state.manager = manager\n    await manager.startup()\n\n@app.on_event("shutdown")\nasync def shutdown():\n    # this is absolutely essential to allow the manager to shutdown\n    # all the listening workers, as well as for the broker to do any\n    # cleanup or disconnects it should from its backing storage inferface.\n    await app.state.manager.shutdown()\n\n@app.get("/do_thing")\nasync def root():\n    # enqueue the task so it gets run in a worker\'s process queue\n    await app.state.manager.enqueue(_essential_task, 2, 2)\n    return {"message": "The thing is being done!"}\n```\n\n## License\n\nThis software is licensed under the [BSD 2-Clause “Simplified” License](LICENSE).\n\nThis package is [Treeware](https://treeware.earth). If you use it in production, consider [**buying the world a tree**](https://ecologi.com/eliasgabriel?r=6128126916bfab8bd051026c) to thank me for my work. By contributing to my forest, you’ll be creating employment for local families and restoring wildlife habitats.\n',
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thearchitector/just-jobs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
