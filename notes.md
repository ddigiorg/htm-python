###Inputs

Inputs: 1D binary array 

[0, 1, 1, 0, 0, 0]

#Outputs

Active States: 3D binary array (t, columns, neurons)
Predict States: 3D binary array (t, columns, neurons)

###Spatial Pooling

Inputs
 i0 i1 i2 i3 i4 i5
[0, 1, 1, 0, 0, 0]

Proximal Synapses Addresses 

  a0 a1 a2
c[0, 4, 3]
c[4, 5, 2]
c[5, 3, 1]
c[0, 2, 1]
c[4, 3, 0]

Proximal Synapses Permanances

  p0  p1  p2
c[21, 20, 20]
c[20, 21, 21]
c[21, 21, 20]
c[20, 21, 21]
c[20, 20, 20]

If Proximal Synapse Connected = Proximal Synapses Permanances > Proximal Synapses Threshold

                 p0  p1  p2
c[1, 0, 0]     c[21, 20, 20]
c[0, 1, 1]     c[20, 21, 21]
c[1, 1, 0]  =  c[21, 21, 20]  >  20
c[0, 1, 1]     c[20, 21, 21]
c[0, 0, 0]     c[20, 20, 20]

Proximal Synapse Values = Inputs[Proximal Synaspes Addresses] & If Proximal Synapse Connected

c[0, 0, 0]     c[0, 0, 0]     c[1, 0, 0]
c[0, 0, 1]     c[0, 0, 1]     c[0, 1, 1]
c[0, 0, 0]  =  c[0, 0, 1]  &  c[1, 1, 0]
c[0, 1, 1]     c[0, 1, 1]     c[0, 1, 1]
c[0, 0, 0]     c[0, 0, 1]     c[0, 0, 0]

Overlaps = sum(Proximal Synapse Values)

c[0]
c[1]
c[0]
c[2]
c[0]

Active Column Addresses = [3, 1]

###Temporal Memory

Predict States(t-1)

  n  n  n  n  n
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]

Active States(t) = zeros

  n  n  n  n  n
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]

Active States(t)[Active Column Addresses] = Predict States(t-1)[Active Column Addresses]

   n  n  n  n  n        n  n  n  n  n
 c[0, 0, 0, 0, 0]
ac[0, 0, 0, 0, 0]    ac[0, 0, 0, 0, 0]
 c[0, 0, 0, 0, 0] = 
ac[0, 0, 0, 0, 0]    ac[0, 0, 0, 0, 0]
 c[0, 0, 0, 0, 0]

If No Active Neurons = !any( Active States(t)[Active Column Addresses], axis=1 )[:,None]

                  n  n  n  n  n
                c[0, 0, 0, 0, 0]
ac[1]     !any ac[0, 0, 0, 0, 0]
       =        c[0, 0, 0, 0, 0]
ac[1]     !any ac[0, 0, 0, 0, 0]
                c[0, 0, 0, 0, 0]

Active States(t)[Active Column Addresses] = Full Column of Active Neurons * If No Active Neurons

   n  n  n  n  n
 c[0, 0, 0, 0, 0]
ac[1, 1, 1, 1, 1]     [1, 1, 1, 1, 1] * ac[1]
 c[0, 0, 0, 0, 0]  =
ac[1, 1, 1, 1, 1]     [1, 1, 1, 1, 1]   ac[1]
 c[0, 0, 0, 0, 0]






Learn Neuron Address

[c, n]


Active States(t-1)

  n  n  n  n  n
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]
c[0, 0, 0, 0, 0]


