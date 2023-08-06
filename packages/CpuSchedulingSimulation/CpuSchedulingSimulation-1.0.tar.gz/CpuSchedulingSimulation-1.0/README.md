# CPU Scheduling Simulation
  CPU use may algorithms such as 

  + First Come First Served(FCFS)
  + Shortest Job First(SJF)
  + Round Robin

  These are used to schedule which process or task must be done **first** when many 
process are waiting. In this package I have created a simulation of these three algorithms to understand them more easier.

## FCFS 

The first process which come will be processed by the CPU before processing the next process.

## SJF

The process which have least time of execution will be processed first.

## Round Robin

The process is processed in multiple steps hence giving an equal chance to all processes

# Installing with pip
 You can easily install this using pip. The package name is *CpuSchedulingSimulation* and the module is named **Cpu_schdeuling_algorithms** 
```
pip install CpuSchedulingSimulation
```
> Note: This will also install pygame(2.1.2)
## Examples

Then just import the module and run the functions named as algorithms to see the simulation in action.
```python
import Cpu_scheduling_algorithms as css
css.FCFS()
```

```python
css.SJF()
```

```python
css.Round_Robin()
```

# Packages used 
  **Pygame** a popular game library in pyton is used in this project to create simulation of the scheduling process



> Note: These simultaion can be used to understand CPU scheduling effectively, if you have basic knowledge of 
> CPU scheduling algorithms

Please refer to project on github for more details.