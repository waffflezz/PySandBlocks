import pyxel
import numpy as np
from src.blocks_3d.obj_to_vf import obj_to_vf
from math import sin, cos


class Pivot:
    def __init__(self):
        self.l_coords = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])


class RotateMatrix:
    @staticmethod
    def z_rotation(rad):
        return np.array([[cos(rad), -sin(rad), 0],
                         [sin(rad), cos(rad), 0],
                         [0, 0, 1]])

    @staticmethod
    def x_rotation(rad):
        return np.array([[cos(rad), 0, -sin(rad)],
                         [0, 1, 0],
                         [sin(rad), 0, cos(rad)]])

    @staticmethod
    def y_rotation(rad):
        return np.array([[1, 0, 0],
                         [0, cos(rad), -sin(rad)],
                         [0, sin(rad), cos(rad)]])


class Camera:
    def __init__(self, coords):
        self.g_coords = coords
        self.orts = np.array([[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])

    def projection(self, dot):

        dot = self.d_to_l(dot)

        if dot[2] <= 0 or dot[2] >= 200:
            return None

        px = dot[0]*70/dot[2] + pyxel.width/2
        py = dot[1]*70/dot[2] + pyxel.height/2

        if px < -70 or px >= pyxel.width + 70:
            return None
        if py < -70 or px >= pyxel.height + 70:
            return None

        return np.array([px, py])

    def d_to_l(self, dot):
        dot = dot - self.g_coords
        dot = self.orts.dot(dot)
        return dot

    def move(self, vec):
        self.g_coords += vec

    def rotate_x(self, rad):
        self.orts = RotateMatrix.x_rotation(rad).dot(self.orts)

    def rotate_y(self, rad):
        self.orts = RotateMatrix.y_rotation(rad).dot(self.orts)

    def rotate_z(self, rad):
        self.orts = RotateMatrix.z_rotation(rad).dot(self.orts)


class Block:
    def __init__(self, coords, scale, block_name):

        self.r_matrix = RotateMatrix()

        self.g_coords = coords

        self.vertex, self.indexes = obj_to_vf(f'src/blocks_3d/blocks/{block_name}.obj')

        for dot in self.vertex:
            dot *= scale
            dot += self.g_coords

    def draw(self, camera: Camera):
        for index in self.indexes:
            pdot1 = camera.projection(self.vertex[index[0]])
            pdot2 = camera.projection(self.vertex[index[1]])
            pdot3 = camera.projection(self.vertex[index[2]])

            if pdot1 is None or pdot2 is None or pdot3 is None:
                return

            pyxel.trib(pdot1[0], pdot1[1],
                       pdot2[0], pdot2[1],
                       pdot3[0], pdot3[1],
                       2)

    def rotation(self, rad, coord: str):
        self.g_to_l()

        if coord.upper() == 'Z':
            for i, vertex in enumerate(self.vertex):
                self.vertex[i] = self.r_matrix.z_rotation(rad).dot(vertex)

        if coord.upper() == 'X':
            for i, vertex in enumerate(self.vertex):
                self.vertex[i] = self.r_matrix.x_rotation(rad).dot(vertex)

        if coord.upper() == 'Y':
            for i, vertex in enumerate(self.vertex):
                self.vertex[i] = self.r_matrix.y_rotation(rad).dot(vertex)

        self.l_to_g()

    def move_global(self, x, y, z):
        self.g_to_l()

        self.g_coords[0] += x
        self.g_coords[1] += y
        self.g_coords[2] += z

        self.l_to_g()

    def g_to_l(self):
        for i, _ in enumerate(self.vertex):
            self.vertex[i] -= self.g_coords

    def l_to_g(self):
        for i, _ in enumerate(self.vertex):
            self.vertex[i] += self.g_coords
