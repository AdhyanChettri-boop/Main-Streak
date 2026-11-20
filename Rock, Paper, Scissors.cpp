#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {
    srand(time(0));
    string options[3] = {"Rock", "Paper", "Scissors"};
    int userChoice, computerChoice;
    char playAgain;

    do {
        cout << "\nRock Paper Scissors\n";
        cout << "1. Rock\n2. Paper\n3. Scissors\n";
        cout << "Enter your choice (1-3): ";
        cin >> userChoice;

        if (userChoice < 1 || userChoice > 3) {
            cout << "Invalid choice!\n";
            continue;
        }

        computerChoice = rand() % 3 + 1;

        cout << "You chose: " << options[userChoice - 1] << endl;
        cout << "Computer chose: " << options[computerChoice - 1] << endl;

        if (userChoice == computerChoice)
            cout << "It's a Draw!\n";
        else if ((userChoice == 1 && computerChoice == 3) ||
                 (userChoice == 2 && computerChoice == 1) ||
                 (userChoice == 3 && computerChoice == 2))
            cout << "You Win!\n";
        else
            cout << "Computer Wins!\n";

        cout << "Play again? (y/n): ";
        cin >> playAgain;

    } while (playAgain == 'y' || playAgain == 'Y');

    return 0;
}
