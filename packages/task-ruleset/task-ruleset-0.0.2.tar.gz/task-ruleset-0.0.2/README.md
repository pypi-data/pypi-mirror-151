# task-ruleset

A scheduler for task and ruleset based parallel computation. Useful for highly parallel applications.

Any algorithm can be devided into a set of steps, called Tasks. Some Tasks may need to be run in a particular order, and some may be run in any order.

We define Tasks of several types, and a Rule for acting on each type of Task. These Rules may perform some computation and end their Task, and then may create one or more new Tasks of same or different types, or may not create any new Tasks and end the chain. All Tasks which exist at a given point in time must not depend on each other and will run in parallel.

Paralellism is achieved by creating a fixed number of sub-processes and scheduling the Tasks on those sub-processes.

### Usage Example

A simple example of how this package can be used is shown below:

```python
import task_ruleset as Lib
import os, sys, time

def rule_init(TaskKey, TaskData):
    return [Lib.Task("get", "get_" + str(i), [i]) for i in range(16)]

def rule_get(TaskKey, TaskData):
    time.sleep(1)
    print(TaskKey, TaskData)

Lib.NGuests = 8
Lib.Rules["init"] = (0, rule_init)
Lib.Rules["get"] = (1, rule_get)

Lib.InitTask = Lib.Task("init", "init", [])

def main():
    print("Starting Execution")
    Lib.main()
    print(Lib.TasksAssignedToProcess)

if __name__ == '__main__':
    main()
```

Here we first set the number of sub-processes being used to 8.<br>
We define Tasks of 2 types:
* `"init"`: acted on by `rule_init`, requires `0` parameters<br>Creates 16 new tasks, all of type `"get"`, with keys as `"get_0"`, `"get_1"` ... `"get_15"`, and parameters as `0`, `1` ... `15`.
* `"get"`: acted on by `rule_get`, requires `1` parameters<br>Waits for 1 second, then prints key of the Task and its parameters, then ends.

When run, this program creates 8 sub-processes and runs 1 Task of type `"init"` on one sub-process. This creates 16 new tasks which needs to be schedules on 8 sub-processes. Each sub-process gets 2 Tasks. None of these Tasks create new Tasks, so the program ends.