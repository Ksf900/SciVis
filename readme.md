# General Information

In this directory, you find four data sets for simulation structural plasticity in the (human) brain. Our simulation treats neurons as points in 3D-space with directed synapses between them. During the simulation, the synapses (the connectome) changes.

## File Overview

For a given simulation data set, you can find the neurons in the file **positions/rank_0_positions.txt**. This file contains some comments (starting with '#') and a list of neurons. Each column represents one neuron, the format is:
(\<neuron id\> + 1) \<x position\> \<y position\> \<z position\> \<area name\> "ex"   
For the purpose of this contest, you can ignore the "ex" marker.

You can find the network for some fixed simulation steps in the files **network/rank_0_step_XXX_{in, out}_network.txt**. Due to the nature of the simulation, we save the outgoing and incoming synapses in different files. The file also contains some comments (starting with '#'). The format in both files is:
\<target MPI rank\> (\<target neuron id\> + 1) \<source MPI rank\> (\<source neuron id\> + 1) \<synapse weight\>
We have used only one MPI rank, so in all files, the respective ranks are 0. Between some neurons multiple synapses exist. Instead of storing those seperately, we just increase the weight.

Furthermore, we have four general information files. In **rank_0_timers.txt** are timing results of various parts of the simulation. Usually, this contains the minimum, average, and maximum across all MPI ranks. For our purpose, those three values are equal.
In **rank_0_plasticity_changes.txt** is a summary of the changes in plasticity for some simulation steps. The format is (the last value is just the sum of the previous two):
\<simulation step\>: \<number created synapses\> \<number deleted synapses\> \<total change in this step\>
**rank_0_neurons_overview.txt** contains some easily accessible overview of different neuron metircs. That is, for a given simulation step, it contains the average, minimum, maximum, variance, and standard deviation of each of the current calcium value (*C*), the grown axons (*axons*), the connected axons (*axons.c*), the grown (excitatory -- ignore this adjective) dendrites (*den.ex*), and the connected excitatory dendrites (*den.ex.c*). These metrics are calculated for all *alive* neurons.
Lastly, in **rank_0_essentials.txt** is a brief overview of some simulation-specific attributes. 

**monitors.zip** contains information for each neuron (in the respective file name "0\_\<neuron di\>.csv"). The seperator is ';' to avoid language issues. Each column has the following format:
\<step\> ; \<fired\> ; \<fired fraction\> ; \<activity\> ; \<dampening\> ; \<current calcium\> ; \<target calcium\> ; \<synaptic input\> ; \<background input\> ; \<grown axons\> ; \<connected axons\> ; \<grown dendrites\> ; \<connected dendrites\>
 - \<step\> indicates the stimulation step in which these values were captured (**integer**)
 - \<fired\> indicates if a neuron fired in the current stip (**0/1**)
 - \<fired fraction\> indicates how often a neuron fired since the last column (**[0, 1]**)
 - \<activity\> indicates the current electrical activity of the neuron (**float**)
 - \<dampening\> in the Izhikevich model for neuronal activity, this values dampens the neuron firing and thus hinders a neuron to fire in every simulation step (**float**)
 - \<current calcium\> indicates the current calcium concentration (a filtered version of the activity -- acts as proxy for it) (**float**)
 - \<target calcium\> indicates the target calcium for the neuron (**float**)
 - \<synaptic input\> indicates how much input the neuron received via synapses in the update step (i.e., other neurons fired and transfered this via their axon to the current neuron's dendrite) (**float**)
 - \<background input\> indicates how much input the neuron received via background noise (**float**)
 - \<grown axons\> indicates how many axons the neuron has grown (**float**)
 - \<connected axons\> indicates how many outgoing synapses the neuron has (**integer**)
 - \<grown dendrites\> indicates how many dendrites the neuron has grown (**float**)
 - \<connected dendrites\> indicates how many incoming synapses the neuron has (**integer**)

## Simulations

We have four different simulation scenarios -- some of them have specific files to them.
However, they all share the same basic settings. We simulate 50,000 neurons for 1,000,000 simulations steps. Each neuron receives a background input ~ N(4,1). If a neuron fires, it transfers 1.5 activity to each neuron it connects to (via its own axon). If a neuron fires, it increases its calcium by 0.002.

#### viz-no-network

Here, we have no initial connectivity and let the network find a steady state by itself. Each neuron has a target calcium of 0.7. There is no additional files.

#### viz-stimulus

Here, we use the connectivity from **viz-no-network** as input. Each neuron has a target calcium of 0.7. The first plasticity update is in step 50,000 to account for the cold start. We stimulate three areas (8, 30, 34) and want the network to *learn* a connection between area 8 and 30 (34 acts as a control group).
We provide the additional file **stimulus.txt** which firstly lists the areas with the included neurons, and then provides stimulation in the form of:
\<first step of stimulus\>-\<last step of stimulus\>:\<frequency of stimulus\> \<intensity of stimulus\> \<neuron ids\>

#### viz-disable

Here, we use the connectivity from **viz-no-network** as input. Each neuron has a target calcium of 0.7. The first plasticity update is in step 50,000 to account for the cold start. In simulation step 100,000, we disable the neurons from areas 5 and 8, so they will no longer participate in any connectivity. Neurons, that were connected to newly-disabled ones loose their connections but still keep their grown axons/dendrites. We provide **disable.txt** which has just one line of interest that indicates the neuron ids.

#### viz-calcium

Here, we use the connectivity from **viz-no-network** as input. The first plasticity update is in step 50,000 to account for the cold start. We set the calcium targets on a per-neuron basis, which should alter the network significantly (and deprive some neurons of input alltogether).
We provide **calcium_targets.txt** which has the following format:
\<neuron id + 1\> \<calcium at the start of the simulation\> \<target calcium\>
The first line: "*0 0 0*" is the default -- required, but not used. 