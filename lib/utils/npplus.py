import numpy as np

def vector_2d(angle, magnitude):
    return np.multiply((np.cos(angle), np.sin(angle)), magnitude).tolist()

def rotate_vector_2d(vector, angle):
    return (vector[0] * np.cos(angle) - vector[1] * np.sin(angle), vector[0] * np.sin(angle) + vector[1] * np.cos(angle))

def vector_2d_angle(vector):
    if vector[0] == 0:
        if vector[1] == 0:
            return 0
        return np.pi / 2 if vector[1] > 0 else np.pi * 3 / 2
    if vector[0] > 0:
        return np.atan(vector[1] / vector[0])
    if vector[1] > 0:
        return np.atan(vector[1] / vector[0]) + np.pi
    return np.atan(vector[1] / vector[0]) - np.pi

def vector_magnitude(vector):
    return np.linalg.norm(vector)

def distance(p1, p2):
    return vector_magnitude(np.subtract(p2, p1))

def lerp_float(f1, f2, factor, dt, snap_margin=0.1):
    if abs(f1 - f2) <= snap_margin:
        return f2
    return f1 + (f2 - f1) * (1 - np.exp(dt * np.log(1 - factor)))

def lerp_array(a1, a2, factor, dt):
    return np.add(a1, np.multiply(np.subtract(a2, a1), (1 - np.exp(dt * np.log(1 - factor))))).tolist()