#include <iostream>

using namespace std;

char board[3][3] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'}
};

void drawBoard() {
    cout << "\n";
    for (int i = 0; i < 3; i++) {
        cout << " " << board[i][0] << " | " << board[i][1] << " | " << board[i][2] << endl;
        if (i < 2) cout << "---|---|---\n";
    }
    cout << "\n";
}

bool checkWin() {
    // Rows and Columns
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2]) return true;
        if (board[0][i] == board[1][i] && board[1][i] == board[2][i]) return true;
    }
    // Diagonals
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2]) return true;
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0]) return true;

    return false;
}

bool isDraw() {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i][j] != 'X' && board[i][j] != 'O')
                return false;
    return true;
}

int main() {
    char currentPlayer = 'X';
    int choice;
    bool gameOver = false;

    cout << "TIC-TAC-TOE\n";
    cout << "Player 1: X\nPlayer 2: O\n";

    while (!gameOver) {
        drawBoard();
        cout << "Player " << currentPlayer << ", enter a number (1-9): ";
        cin >> choice;

        int row = (choice - 1) / 3;
        int col = (choice - 1) % 3;

        if (choice < 1 || choice > 9 || board[row][col] == 'X' || board[row][col] == 'O') {
            cout << "Invalid move! Try again.\n";
            continue;
        }

        board[row][col] = currentPlayer;

        if (checkWin()) {
            drawBoard();
            cout << "Player " << currentPlayer << " wins!\n";
            gameOver = true;
        }
        else if (isDraw()) {
            drawBoard();
            cout << "It's a draw!\n";
            gameOver = true;
        }
        else {
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        }
    }

    return 0;
}
