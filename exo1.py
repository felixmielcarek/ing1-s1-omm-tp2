import pyray as pr
import numpy as np
from pyray import Vector3

from tp1_functions import *
from basic_drawing_functions import *
from mesh_functions import *

def scaling_matrix(axis, k):
    """Génère une matrice de mise à l'échelle le long d'un axe arbitraire."""
    # TODO : mettre en œuvre 
    axis = vector_normalize(axis)
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

def rotation_matrix(axis, theta):
    """Génère une matrice de rotation autour d'un axe arbitraire."""
    # TODO : mettre en œuvre 
    axis = vector_normalize(axis)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

def orthographic_projection_matrix(axis):
    """Génère une matrice de projection orthographique pour la projection sur un plan normal à un axe donné."""
    # TODO : mettre en œuvre 
    axis = vector_normalize(axis)
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])


def main():
    pr.init_window(1000, 800, "3D Viewer with Rotation, Scaling, and Projection Control")
    pr.set_window_min_size(800, 600)
    camera = initialize_camera()
    pr.set_target_fps(60)
    movement_speed = 0.1

    ply_file_path = "dolphin.ply"
    mesh = load_ply_file(ply_file_path)
    
    initialize_mesh_for_transforming(mesh)

    scale_factor_ptr = pr.ffi.new('float *', 1.0)
    angle_ptr = pr.ffi.new('float *', 0.0)
    axis_x_ptr = pr.ffi.new('float *', 1.0)
    axis_y_ptr = pr.ffi.new('float *', 0.0)
    axis_z_ptr = pr.ffi.new('float *', 0.0)
    projection_ptr = pr.ffi.new('bool *', 0)

    while not pr.window_should_close():
        update_camera_position(camera, movement_speed)
        
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        
        pr.begin_mode_3d(camera)
        
        axis = Vector3(axis_x_ptr[0], axis_y_ptr[0], axis_z_ptr[0])
        angle = angle_ptr[0]
        scale_factor = scale_factor_ptr[0]
        
        rotation_mat = rotation_matrix(axis, np.radians(angle))
        scaling_mat = scaling_matrix(axis, scale_factor)
        projection_mat = np.eye(3)
        if projection_ptr[0]:
            projection_mat = orthographic_projection_matrix(axis)
            
        # Dessiner les axes de coordonnées standard
        draw_coordinate_axes(Vector3(0, 0, 0), scale=3)
        
        # Obtenir l'axe de transformation en fonction des valeurs du curseur
        axis = Vector3(axis_x_ptr[0], axis_y_ptr[0], axis_z_ptr[0])
        # Tracer l'axe de transformation à partir de l'origine
        draw_transformation_axis(Vector3(0, 0, 0), axis, scale=3)            
        
        apply_transformations(mesh, rotation_mat, scaling_mat, projection_mat)
        
        draw_plane(axis, 10)
        draw_mesh(mesh)
        pr.end_mode_3d()

        pr.draw_text("Échelle:", 750, 50, 20, pr.BLACK)
        pr.gui_slider_bar(pr.Rectangle(750, 80, 200, 20), "0.5", "10", scale_factor_ptr, 0.4, 10.0)
        pr.draw_text("Angle (degrés):", 750, 110, 20, pr.BLACK)
        pr.gui_slider_bar(pr.Rectangle(750, 140, 200, 20), "0", "360", angle_ptr, 0.0, 360.0)        
        
        pr.draw_text("Axe de transformation X:", 750, 170, 20, pr.BLACK)
        pr.gui_slider_bar(pr.Rectangle(750, 200, 200, 20), "-1.0", "1.0", axis_x_ptr, -1.0, 1.0)
        pr.draw_text("Axe de transformation Y:", 750, 230, 20, pr.BLACK)
        pr.gui_slider_bar(pr.Rectangle(750, 260, 200, 20), "-1.0", "1.0", axis_y_ptr, -1.0, 1.0)
        pr.draw_text("Axe de transformation Z:", 750, 290, 20, pr.BLACK)
        pr.gui_slider_bar(pr.Rectangle(750, 320, 200, 20), "-1.0", "1.0", axis_z_ptr, -1.0, 1.0)

        pr.draw_text("Projection orthographique:", 750, 350, 20, pr.BLACK)
        pr.gui_check_box(pr.Rectangle(750, 380, 20, 20), "Activer", projection_ptr)

        pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()