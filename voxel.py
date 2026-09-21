from math import sqrt, cos, sin, tan, radians

import pygame
from pygame import Surface

import sys


def voxel():
    vertices = [
        [+0.5, +0.5, +0.5],
        [+0.5, +0.5, -0.5],
        [+0.5, -0.5, +0.5],
        [+0.5, -0.5, -0.5],
        [-0.5, +0.5, +0.5],
        [-0.5, +0.5, -0.5],
        [-0.5, -0.5, +0.5],
        [-0.5, -0.5, -0.5],
    ]
    faces = [
        [0, 1, 3, 2],  # +X face
        [4, 6, 7, 5],  # -X face
        [0, 2, 6, 4],  # +Z face
        [1, 5, 7, 3],  # -Z face
        [0, 4, 5, 1],  # +Y face
        [2, 3, 7, 6],  # -Y face
    ]

    return vertices, faces


# Maps each face index to the normal direction (offset to place a new voxel)
FACE_NORMALS = {
    0: (1, 0, 0),   # +X
    1: (-1, 0, 0),  # -X
    2: (0, 0, 1),   # +Z
    3: (0, 0, -1),  # -Z
    4: (0, 1, 0),   # +Y
    5: (0, -1, 0),  # -Y
}


def get_face_index(faces, face_tuple):
    """Find the index of a face in the faces list by matching its tuple."""
    for i, f in enumerate(faces):
        if tuple(f) == face_tuple:
            return i
    return None


def order_voxel_positions(voxel_positions, camera_position):
    def distance_squared(voxel):
        dx = voxel[0] - camera_position[0]
        dy = voxel[1] - camera_position[1]
        dz = voxel[2] - camera_position[2]
        return dx * dx + dy * dy + dz * dz

    return sorted(voxel_positions, key=distance_squared, reverse=True)


def matrix_multiplication(matrix, vector):
    return [sum(matrix[row][i] * vector[i] for i in range(3)) for row in range(3)]


def get_visible_faces(vertices, faces, position, camera_position):
    visible_faces = []

    for face in faces:
        pointO = face[0]
        pointA = face[1]
        pointB = face[-1]

        vectorO = [
            vertices[pointO][0] + position[0],
            vertices[pointO][1] + position[1],
            vertices[pointO][2] + position[2],
        ]
        vectorA = [
            vertices[pointA][0] + position[0],
            vertices[pointA][1] + position[1],
            vertices[pointA][2] + position[2],
        ]
        vectorB = [
            vertices[pointB][0] + position[0],
            vertices[pointB][1] + position[1],
            vertices[pointB][2] + position[2],
        ]

        lineA = [
            vectorA[0] - vectorO[0],
            vectorA[1] - vectorO[1],
            vectorA[2] - vectorO[2],
        ]
        lineB = [
            vectorB[0] - vectorO[0],
            vectorB[1] - vectorO[1],
            vectorB[2] - vectorO[2],
        ]

        normal = [
            lineA[1] * lineB[2] - lineA[2] * lineB[1],
            lineA[2] * lineB[0] - lineA[0] * lineB[2],
            lineA[0] * lineB[1] - lineA[1] * lineB[0],
        ]

        view_vector = [
            camera_position[0] - vectorO[0],
            camera_position[1] - vectorO[1],
            camera_position[2] - vectorO[2],
        ]

        dot_product = (
            normal[0] * view_vector[0]
            + normal[1] * view_vector[1]
            + normal[2] * view_vector[2]
        )

        if dot_product < 0:
            visible_faces.append(face)

    return visible_faces


def rotate_point(point, pitch, yaw):
    rotation_x = [
        [1, 0, 0],
        [0, cos(pitch), -sin(pitch)],
        [0, sin(pitch), cos(pitch)],
    ]

    rotation_y = [
        [cos(yaw), 0, sin(yaw)],
        [0, 1, 0],
        [-sin(yaw), 0, cos(yaw)],
    ]

    rotated_point = matrix_multiplication(rotation_y, point)
    rotated_point = matrix_multiplication(rotation_x, rotated_point)

    return rotated_point


def get_camera_space_vertices(
    vertices, voxel_position, camera_position, camera_rotation
):
    camera_space = []
    for vertex in vertices:
        world_vertex = [
            vertex[0] + voxel_position[0],
            vertex[1] + voxel_position[1],
            vertex[2] + voxel_position[2],
        ]
        relative_vertex = [
            world_vertex[0] - camera_position[0],
            world_vertex[1] - camera_position[1],
            world_vertex[2] - camera_position[2],
        ]
        rotated = rotate_point(
            relative_vertex, -camera_rotation[0], -camera_rotation[1]
        )
        camera_space.append(rotated)
    return camera_space


def clip_face(face_vertices, near_plane):
    clipped = []
    n = len(face_vertices)

    for i in range(n):
        current = face_vertices[i]
        next = face_vertices[(i + 1) % n]

        current_inside = current[2] >= near_plane
        next_inside = next[2] >= near_plane

        if current_inside:
            clipped.append(current)

        if current_inside != next_inside:
            crossed_edge = (near_plane - current[2]) / (next[2] - current[2])
            intersection = [
                current[0] + crossed_edge * (next[0] - current[0]),
                current[1] + crossed_edge * (next[1] - current[1]),
                near_plane,
            ]
            clipped.append(intersection)

    return clipped


def project_face(face_vertices, focal_length, width, height, near_plane):
    clipped = clip_face(face_vertices, near_plane)

    if len(clipped) < 3:
        return None

    face_points = []
    for vertex in clipped:
        px = (vertex[0] * focal_length) / vertex[2]
        py = (vertex[1] * focal_length) / vertex[2]
        x = px * height + width / 2
        y = -py * height + height / 2
        face_points.append([x, y])

    return face_points


def ray_intersects_face(vertices, face, position):
    face_vertices_3d = [vertices[i] for i in face]

    if all(v[2] < 0.1 for v in face_vertices_3d):
        return None

    for i in range(1, len(face_vertices_3d) - 1):
        v0 = face_vertices_3d[0]
        v1 = face_vertices_3d[i]
        v2 = face_vertices_3d[i + 1]

        result = ray_triangle_intersection(v0, v1, v2)
        if result is not None:
            return result

    return None


def ray_triangle_intersection(v0, v1, v2):
    edge1 = [v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]]
    edge2 = [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]]

    h = [-edge2[1], edge2[0], 0.0]

    a = edge1[0] * h[0] + edge1[1] * h[1] + edge1[2] * h[2]

    if -1e-8 < a < 1e-8:
        return None

    f = 1.0 / a
    s = [-v0[0], -v0[1], -v0[2]]

    u = f * (s[0] * h[0] + s[1] * h[1] + s[2] * h[2])
    if u < 0.0 or u > 1.0:
        return None

    q = [
        s[1] * edge1[2] - s[2] * edge1[1],
        s[2] * edge1[0] - s[0] * edge1[2],
        s[0] * edge1[1] - s[1] * edge1[0],
    ]

    v = f * q[2]
    if v < 0.0 or u + v > 1.0:
        return None

    t = f * (edge2[0] * q[0] + edge2[1] * q[1] + edge2[2] * q[2])

    if t > 0.1:
        return t

    return None


def find_looked_at_face(voxel_positions_set, voxel_positions, vertices, faces, camera_position, camera_rotation):
    best_distance = float('inf')
    best_voxel = None
    best_face_idx = None
    best_face_tuple = None

    for voxel_position in voxel_positions:
        camera_space_verts = get_camera_space_vertices(
            vertices, voxel_position, camera_position, camera_rotation
        )
        visible_faces = get_visible_faces(
            vertices, faces, voxel_position, camera_position
        )

        for face in visible_faces:
            dist = ray_intersects_face(camera_space_verts, face, voxel_position)
            if dist is not None and dist < best_distance:
                best_distance = dist
                best_voxel = voxel_position
                best_face_tuple = tuple(face)
                best_face_idx = get_face_index(faces, best_face_tuple)

    return best_voxel, best_face_tuple, best_face_idx


def get_placement_position(voxel_pos, face_index):
    """Calculate the position where a new voxel should be placed
    based on which face is being looked at."""
    if face_index is None or voxel_pos is None:
        return None

    normal = FACE_NORMALS.get(face_index)
    if normal is None:
        return None

    new_pos = (
        voxel_pos[0] + normal[0],
        voxel_pos[1] + normal[1],
        voxel_pos[2] + normal[2],
    )
    return new_pos


def display(
    screen: Surface,
    camera_space_vertices: list,
    faces: list[list[int]],
    width: int,
    height: int,
    line_width: int,
    color: list[int],
    focal_length: float,
    fov_degrees,
    highlighted_face=None,
):
    near_plane = 0.1

    for face in faces:
        face_vertices = [camera_space_vertices[i] for i in face]
        face_points = project_face(
            face_vertices, focal_length, width, height, near_plane
        )

        if face_points is None:
            continue

        if highlighted_face is not None and tuple(face) == highlighted_face:
            fill_color = "#2fdf8f"
        else:
            fill_color = color[1]

        pygame.draw.polygon(screen, fill_color, face_points)
        pygame.draw.polygon(screen, color[0], face_points, line_width)


def movement(camera_position, camera_rotation, dt):
    move_speed = 5
    mouse_sensitivity = 0.001

    mx, my = pygame.mouse.get_rel()
    camera_rotation[1] += mx * mouse_sensitivity
    camera_rotation[0] += my * mouse_sensitivity
    camera_rotation[0] = max(-1.5, min(1.5, camera_rotation[0]))

    keys = pygame.key.get_pressed()
    yaw = camera_rotation[1]

    forward = [sin(yaw), 0, cos(yaw)]
    right = [cos(yaw), 0, -sin(yaw)]

    if keys[pygame.K_w]:
        camera_position[0] += forward[0] * move_speed * dt
        camera_position[2] += forward[2] * move_speed * dt

    if keys[pygame.K_s]:
        camera_position[0] -= forward[0] * move_speed * dt
        camera_position[2] -= forward[2] * move_speed * dt

    if keys[pygame.K_a]:
        camera_position[0] -= right[0] * move_speed * dt
        camera_position[2] -= right[2] * move_speed * dt

    if keys[pygame.K_d]:
        camera_position[0] += right[0] * move_speed * dt
        camera_position[2] += right[2] * move_speed * dt

    if keys[pygame.K_SPACE]:
        camera_position[1] += move_speed * dt

    if keys[pygame.K_LSHIFT]:
        camera_position[1] -= move_speed * dt

    return camera_position, camera_rotation


def main():
    pygame.init()

    width, height = 960, 540
    pygame.display.set_caption("cube")
    screen = pygame.display.set_mode((width, height))

    camera_position = [0, 0, 0]
    camera_rotation = [0, 0]
    FOV = 120
    focal_length = 1 / tan(radians(FOV) / 2)

    vertices, faces = voxel()
    voxel_positions = []
    voxel_positions_set = set()
    for x in range(-5, 5, 1):
        for z in range(0, 10, 1):
            pos = (x, -1, z)
            voxel_positions.append(pos)
            voxel_positions_set.add(pos)

    color = ["#0f0f0f", "#0faf4f"]
    line_width = 2

    #pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    max_reach = 10  # Maximum distance for placing/looking at voxels

    clock = pygame.time.Clock()
    while True:
        tick = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Left click - place voxel
                    if looked_voxel is not None and looked_face_idx is not None:
                        new_pos = get_placement_position(looked_voxel, looked_face_idx)
                        if new_pos is not None and new_pos not in voxel_positions_set:
                            # Don't place a voxel where the camera is
                            cam_voxel = (
                                round(camera_position[0]),
                                round(camera_position[1]),
                                round(camera_position[2]),
                            )
                            if new_pos != cam_voxel:
                                voxel_positions.append(new_pos)
                                voxel_positions_set.add(new_pos)

                elif event.button == 1:  # Right click - remove voxel
                    if looked_voxel is not None and looked_voxel in voxel_positions_set:
                        voxel_positions.remove(looked_voxel)
                        voxel_positions_set.remove(looked_voxel)

        camera_position, camera_rotation = movement(
            camera_position, camera_rotation, tick
        )

        # Find which face the crosshair is pointing at
        looked_voxel, looked_face, looked_face_idx = find_looked_at_face(
            voxel_positions_set, voxel_positions, vertices, faces, camera_position, camera_rotation
        )

        # Enforce max reach distance
        if looked_voxel is not None:
            dx = looked_voxel[0] - camera_position[0]
            dy = looked_voxel[1] - camera_position[1]
            dz = looked_voxel[2] - camera_position[2]
            dist = sqrt(dx * dx + dy * dy + dz * dz)
            if dist > max_reach:
                looked_voxel = None
                looked_face = None
                looked_face_idx = None

        ordered_voxel_positions = order_voxel_positions(
            voxel_positions, camera_position
        )

        screen.fill("#0f8fcf")

        for voxel_position in ordered_voxel_positions:
            camera_space_vertices = get_camera_space_vertices(
                vertices, voxel_position, camera_position, camera_rotation
            )
            visible_faces = get_visible_faces(
                vertices, faces, voxel_position, camera_position
            )

            highlighted = looked_face if voxel_position == looked_voxel else None

            display(
                screen,
                camera_space_vertices,
                visible_faces,
                width,
                height,
                line_width,
                color,
                focal_length,
                FOV,
                highlighted_face=highlighted,
            )

        # Draw crosshair
        crosshair_pos = (width // 2, height // 2)
        pygame.draw.circle(screen, (255, 0, 0), crosshair_pos, 4)

        pygame.display.flip()


if __name__ == "__main__":
    main()
