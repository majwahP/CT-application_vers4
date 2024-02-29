import numpy as np
import odl
import matplotlib.pyplot as plt


reco_space = odl.uniform_discr(min_pt=[-20, -20], max_pt=[20, 20], shape=[2, 2], dtype='float32')
angle_partition = odl.uniform_partition(0, np.pi, 180)
detector_partition = odl.uniform_partition(-30, 30, 512)
geometry = odl.tomo.Parallel2dGeometry(angle_partition, detector_partition)
ray_trafo = odl.tomo.RayTransform(reco_space, geometry, impl='astra_cpu')
phantom = odl.phantom.shepp_logan(reco_space, modified=True)
phantom_data = np.array([[1, 2],[3, 4]])
phantom = reco_space.element(phantom_data)
proj_data = ray_trafo(phantom)
backproj = ray_trafo.adjoint(proj_data)
phantom.show(title='Phantom')
proj_data.show(title='Projection Data (sinogram)')
backproj.show(title='Back-projection', force_show=True)
#plt.imshow(phantom.asarray(), cmap='gray')
#plt.title('Phantom')
#plt.show()

