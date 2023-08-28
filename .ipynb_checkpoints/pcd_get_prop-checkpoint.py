import open3d as o3d
import numpy as np
import glob
import os
import sys

from open3d.web_visualizer import draw

#data_set= 'palm' or 'coconut'


#list property of point cloud
if len(sys.argv) > 1:
    data_set = sys.argv[1]
else:
    data_set= 'palm'
    

if data_set == 'coconut':
    file_list = glob.glob("/media/hdd10T/3D-dataset/data/coconut/row*.ply")
    f = open('coconut_pcd_prop.csv','w')
else:

    file_list = glob.glob("/media/hdd10T/3D-dataset/data/palm/p?.ply")+glob.glob("/media/hdd10T/t3D-dataset/data/palm/p??.ply")
    f = open('palm_pcd_prop.csv','w')

f.write('name # points# aabb_max # aabb_min # obb_max # obb_min # abb_vol# obb_vol # center # voxel_grid # avg_dist # bpa_mesh #  poison_mesh # poison_avg_density  # convex_hull # convex_hull_pts  ')
f.write('\n')
for file in file_list:
    _,filename = os.path.split(file)
    
    pcd = o3d.io.read_point_cloud(file)
    aabb = pcd.get_axis_aligned_bounding_box()
    #print('axis aligned bounding box ')
    #print(aabb)
    
    aabb.color = (1, 0, 0)
    obb = pcd.get_oriented_bounding_box()
    #print('oriented bounding box ')
    #print(obb)
    #print('max bound, min bound')
    #print(obb.get_max_bound())
    #print(obb.get_min_bound)
    obb.color = (0, 1, 0)
    #draw([origin,pcd, aabb,obb])
    #print(aabb.get_print_info())
    pts = np.array(aabb.get_box_points())
    pts2 = np.array(obb.get_box_points())
    
    print('filename '+filename+ ' align axis max_bound=')
    f.write(filename+'#')
    
    f.write(str(len(pcd.points)))
    f.write('#')
    f.flush()
    
    print(aabb.get_max_bound())
        
     
    f.write(str(aabb.get_max_bound()))
    f.write('#')
    print('min bound')
    print(aabb.get_min_bound())
    f.write(str(aabb.get_min_bound()))
    f.write('#')
    print('oriented axis max_bound')
    print(obb.get_max_bound())
    f.write(str(obb.get_max_bound()))
    f.write('#')
    
    print('min bound')
    print(obb.get_min_bound())
    f.write(str(obb.get_min_bound()))
    f.write('#')
    

    print('axis-aligned volume =',aabb.volume())
    f.write(str(aabb.volume()))
    f.write('#')
    print('oriented volume = ',obb.volume())
    f.write(str(obb.volume()))
    f.write('#')
    print('num_points cloud ', len(np.asarray(pcd.points)))
   
    
    print('covarinace')
    print(np.asarray(pcd.covariances) )
    
    
    print('center')
    print(np.asarray(pcd.get_center()))
    f.write(str(np.asarray(pcd.get_center())))
    f.write('#')
    
    print('voxel grid value')
    print(pcd.VoxelGrid.value)    
    
    f.write(str(pcd.VoxelGrid.value) )
    f.write('#')
    
    
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    
    print('avg nearest distance ',avg_dist)
    
    f.write(str(avg_dist) )
    f.write('#')
    
    pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    
    
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 0.3]))
    print(bpa_mesh)
    
    f.write(str(bpa_mesh))
    f.write('#')
    
    bpa_mesh.compute_vertex_normals()
    print('adj list')
    print(bpa_mesh.compute_adjacency_list())
   
    
    mesh,densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9)
    print(mesh)
    print(len(densities))
    print(np.average(np.asarray(densities)))
    

    f.write(str(mesh))
    f.write('#')
    
    f.write(str(np.average(np.asarray(densities))))
    f.write('#')
    
    #o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius]))
    #normal = bpa_mesh.compute_vertex_normals()
    
   # print('normal')
    #print(normal)
    
    print('convex hull')
    convex_hull, out2= bpa_mesh.compute_convex_hull()
    f.write(str(convex_hull))
    f.write('#')
    print(convex_hull)
    
    print(out2)
    
    f.write(str(out2))
    f.write('#')
    
    f.write('\n')

     
    
    #if set_break:
    #    draw([pcd, origin,bpa_mesh])
    #    break
    


f.close()