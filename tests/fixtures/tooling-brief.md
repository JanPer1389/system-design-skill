# HarborDesk maintenance brief

I run a small booking service and do not have a software background. Please assess its architecture and how we can reproduce development and CI environments. I suggested Redis because I saw it mentioned online, but it is not a company requirement. A single server currently meets our needs; duplicate confirmations must never allocate the same room twice. Our deployment vendor accepts an exported requirements file. Avoid new paid infrastructure.

Inspected workflow snippets supplied for this exercise:

`requirements.txt`: `fastapi>=0.100` and `pytest` with no exact pins.
CI: create a fresh Python environment, install that file and run pytest.
No lock/constraints file, project metadata or alternative dependency workflow is supplied. These are the only sources, not proof that no other files exist.
