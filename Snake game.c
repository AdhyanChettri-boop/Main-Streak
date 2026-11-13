#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>
#include <time.h>

#define WIDTH  40
#define HEIGHT 20
#define MAX_LENGTH 100

int snakeX[MAX_LENGTH], snakeY[MAX_LENGTH];
int snakeLength = 3;
int foodX, foodY;
int dirX = 1, dirY = 0;   // starts moving right
int score = 0;
int gameOver = 0;

void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void hideCursor() {
    CONSOLE_CURSOR_INFO cursor;
    cursor.dwSize = 1;
    cursor.bVisible = FALSE;
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor);
}

void draw() {
    system("cls");

    // Draw top border
    for (int i = 0; i < WIDTH + 2; i++) printf("#");
    printf("\n");

    for (int y = 0; y < HEIGHT; y++) {
        printf("#");  // left border
        for (int x = 0; x < WIDTH; x++) {
            int isSnake = 0;

            // Check if current position is snake
            for (int i = 0; i < snakeLength; i++) {
                if (snakeX[i] == x && snakeY[i] == y) {
                    if (i == 0) printf("O");  // head
                    else printf("o");         // body
                    isSnake = 1;
                    break;
                }
            }

            if (!isSnake) {
                if (x == foodX && y == foodY)
                    printf("*");
                else
                    printf(" ");
            }
        }
        printf("#\n");  // right border
    }

    // Draw bottom border
    for (int i = 0; i < WIDTH + 2; i++) printf("#");
    printf("\n");

    printf("Score: %d\n", score);
    printf("Controls: W A S D   |   Press X to quit\n");
}

void setup() {
    // Initial snake position
    snakeX[0] = 10; snakeY[0] = 10;
    snakeX[1] = 9;  snakeY[1] = 10;
    snakeX[2] = 8;  snakeY[2] = 10;

    // Place first food
    srand(time(NULL));
    foodX = rand() % WIDTH;
    foodY = rand() % HEIGHT;

    hideCursor();
}

void input() {
    if (_kbhit()) {
        char key = _getch();
        switch (key) {
            case 'w': case 'W':
                if (dirY != 1) { dirX = 0; dirY = -1; }
                break;
            case 's': case 'S':
                if (dirY != -1) { dirX = 0; dirY = 1; }
                break;
            case 'a': case 'A':
                if (dirX != 1) { dirX = -1; dirY = 0; }
                break;
            case 'd': case 'D':
                if (dirX != -1) { dirX = 1; dirY = 0; }
                break;
            case 'x': case 'X':
                gameOver = 1;
                break;
        }
    }
}

void logic() {
    // Move the body
    for (int i = snakeLength - 1; i > 0; i--) {
        snakeX[i] = snakeX[i - 1];
        snakeY[i] = snakeY[i - 1];
    }

    // Move the head
    snakeX[0] += dirX;
    snakeY[0] += dirY;

    // Wall collision
    if (snakeX[0] < 0 || snakeX[0] >= WIDTH ||
        snakeY[0] < 0 || snakeY[0] >= HEIGHT) {
        gameOver = 1;
        return;
    }

    // Self collision
    for (int i = 1; i < snakeLength; i++) {
        if (snakeX[0] == snakeX[i] && snakeY[0] == snakeY[i]) {
            gameOver = 1;
            return;
        }
    }

    // Eat food
    if (snakeX[0] == foodX && snakeY[0] == foodY) {
        score += 10;
        snakeLength++;

        // New food position
        foodX = rand() % WIDTH;
        foodY = rand() % HEIGHT;
    }
}

int main() {
    setup();

    while (!gameOver) {
        draw();
        input();
        logic();
        Sleep(100);   // control speed (milliseconds)
    }

    system("cls");
    printf("\n\n========== GAME OVER ==========\n");
    printf("Final Score: %d\n", score);
    printf("Press any key to exit...\n");
    _getch();

    return 0;
}
