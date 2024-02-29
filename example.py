import numpy as np
import odl
import matplotlib.pyplot as plt
import random

reco_space = odl.uniform_discr(min_pt=[-10, -10], max_pt=[10, 10], shape=[300,300], dtype='float32')

angle_partition = odl.uniform_partition(0, np.pi, 180)

detector_partition = odl.uniform_partition(-30, 30, 512)

geometry = odl.tomo.Parallel2dGeometry(angle_partition, detector_partition)

ray_trafo = odl.tomo.RayTransform(reco_space, geometry)


phantom = odl.phantom.shepp_logan(reco_space,modified=True)
#phantom = [[random.randint(0, 1) for _ in range(10)] for _ in range(10)]


print(phantom)
filename = "matrix_output.txt"
with open(filename, 'w') as f:
    for row in phantom:
        f.write('\t'.join(map(str, row)) + '\n')


proj_data = ray_trafo(phantom)

backproj = ray_trafo.adjoint(proj_data)

#phantom.show(title='Phantom')

plt.imshow(phantom.asarray(), cmap='gray')
plt.title('Phantom')
plt.show()



