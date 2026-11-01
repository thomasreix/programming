
#include <raylib.h>
#include <raymath.h>
#include <math.h>
#include <stdio.h>

typedef struct {
    Vector3 vertices[4];
} VisibleFace;

Color HEX(const char *hex) {
    unsigned int r, g, b;
    if (hex[0] == '#') hex++;
    sscanf(hex, "%2x%2x%2x", &r, &g, &b);
    return (Color){r, g, b, 255};
}

int visible(Vector3 world[], int Blocks, Camera3D camera, VisibleFace faces[]) {
    const Vector3 vertices[8] = {
        {-0.5, -0.5, -0.5},
        { 0.5, -0.5, -0.5},
        { 0.5,  0.5, -0.5},
        {-0.5,  0.5, -0.5},
        {-0.5, -0.5,  0.5},
        { 0.5, -0.5,  0.5},
        { 0.5,  0.5,  0.5},
        {-0.5,  0.5,  0.5}
    };

    const int BlockFaces[6][4] = {
        {1, 2, 6, 5}, // +X
        {0, 4, 7, 3}, // -X
        {3, 7, 6, 2}, // +Y
        {0, 1, 5, 4}, // -Y
        {4, 5, 6, 7}, // +Z
        {0, 3, 2, 1}  // -Z
    };

    const Vector3 normals[6] = {
        { 1,  0,  0},
        {-1,  0,  0},
        { 0,  1,  0},
        { 0, -1,  0},
        { 0,  0,  1},
        { 0,  0, -1}
    };

    Vector3 cameraForward = Vector3Normalize(
        Vector3Subtract(camera.target, camera.position)
    );

    int count = 0;

    for (int block = 0; block < Blocks; block++) {
        for (int face = 0; face < 6; face++) {
            Vector3 normal = normals[face];

            // Neighbor culling
            Vector3 neighbor = Vector3Add(world[block], normal);
            bool covered = false;

            for (int other = 0; other < Blocks; other++) {
                if (fabsf(world[other].x - neighbor.x) < 0.001f &&
                    fabsf(world[other].y - neighbor.y) < 0.001f &&
                    fabsf(world[other].z - neighbor.z) < 0.001f) {
                    covered = true;
                    break;
                }
            }

            if (covered) continue;

            // Face center
            Vector3 center = Vector3Add(
                world[block],
                Vector3Scale(normal, 0.5f)
            );

            Vector3 direction = Vector3Subtract(camera.position, center);

            // Backface culling
            if (Vector3DotProduct(normal, direction) <= 0) continue;

            // Behind-camera culling
            Vector3 toFace = Vector3Subtract(center, camera.position);

            if (Vector3DotProduct(cameraForward, toFace) <= 0) continue;

            // Calculate face vertices and screen bounds
            Vector3 faceVertices[4];

            float minX = INFINITY, maxX = -INFINITY;
            float minY = INFINITY, maxY = -INFINITY;

            for (int vertex = 0; vertex < 4; vertex++) {
                faceVertices[vertex] = Vector3Add(
                    world[block],
                    vertices[BlockFaces[face][vertex]]
                );

                Vector2 screen = GetWorldToScreen(faceVertices[vertex], camera);

                minX = fminf(minX, screen.x);
                maxX = fmaxf(maxX, screen.x);
                minY = fminf(minY, screen.y);
                maxY = fmaxf(maxY, screen.y);
            }

            // Screen culling
            if (maxX < 0 || minX > GetScreenWidth() ||
                maxY < 0 || minY > GetScreenHeight()) continue;

            // Store visible face
            for (int vertex = 0; vertex < 4; vertex++) {
                faces[count].vertices[vertex] = faceVertices[vertex];
            }

            count++;
        }
    }

    return count;
}

void graphics(VisibleFace faces[], int FaceCount, Camera3D camera,
              Color background, Color color) {
    BeginDrawing();
    ClearBackground(background);

    BeginMode3D(camera);

    for (int face = 0; face < FaceCount; face++) {
        for (int vertex = 0; vertex < 4; vertex++) {
            DrawLine3D(
                faces[face].vertices[vertex],
                faces[face].vertices[(vertex + 1) % 4],
                color
            );
        }
    }

    EndMode3D();

    // Debug information
    const int fontSize = 24;
    const int margin = 12;

    char fpsText[32];
    char faceText[32];

    snprintf(fpsText, sizeof(fpsText), "FPS: %d", GetFPS());
    snprintf(faceText, sizeof(faceText), "Faces: %d", FaceCount);

    int fpsWidth = MeasureText(fpsText, fontSize);
    int faceWidth = MeasureText(faceText, fontSize);
    int width = fpsWidth > faceWidth ? fpsWidth : faceWidth;

    int x = GetScreenWidth() - width - margin * 2;

    DrawRectangle(
        x, margin,
        width + margin * 2, 68,
        (Color){0, 0, 0, 180}
    );

    DrawText(fpsText, x + margin, margin + 8, fontSize, WHITE);
    DrawText(faceText, x + margin, margin + 36, fontSize, WHITE);

    EndDrawing();
}

int main(void) {
    const int WindowWidth = 960, WindowHeight = 540;

    InitWindow(WindowWidth, WindowHeight, "raycraft");
    SetTargetFPS(60);
    DisableCursor();

    Color black = HEX("#0f0f0f");
    Color white = HEX("#ffffff");

    Camera3D camera = {0};
    camera.position = (Vector3){0, 0, 1};
    camera.target = (Vector3){1, 1, 2};
    camera.up = (Vector3){0, 0, 1};
    camera.fovy = 90;
    camera.projection = CAMERA_PERSPECTIVE;

    Vector3 world[] = {
        { 0,  0, 0},
        { 1,  0, 0},
        {-1,  0, 0},
        { 0,  1, 0},
        { 1,  1, 0},
        {-1,  1, 0},
        { 0, -1, 0},
        { 1, -1, 0},
        {-1, -1, 0}
    };

    const int WorldLength = sizeof(world) / sizeof(world[0]);
    const float speed = 5.0f;
    const float sensitivity = 0.1f;

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();

        // Movement
        Vector3 movement = {
            (float)IsKeyDown(KEY_W) - IsKeyDown(KEY_S),
            (float)IsKeyDown(KEY_D) - IsKeyDown(KEY_A),
            (float)IsKeyDown(KEY_SPACE) - IsKeyDown(KEY_LEFT_SHIFT)
        };

        // Normalize diagonal movement
        float length = sqrtf(
            movement.x * movement.x +
            movement.y * movement.y +
            movement.z * movement.z
        );

        if (length > 0)
            movement = Vector3Scale(movement, speed * dt / length);

        // Mouse look
        Vector2 mouse = GetMouseDelta();

        Vector3 cameraRotation = {
            mouse.x * sensitivity,
            mouse.y * sensitivity,
            0
        };

        UpdateCameraPro(&camera, movement, cameraRotation, 0);

        // Visible faces
        VisibleFace faces[WorldLength * 6];

        int FaceCount = visible(world, WorldLength, camera, faces);

        graphics(faces, FaceCount, camera, black, white);
    }

    EnableCursor();
    CloseWindow();
    return 0;
}
