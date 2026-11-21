#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <algorithm>

using namespace std;

int main() {
    vector<string> words = {
        "computer", "programming", "hangman", "developer",
        "keyboard", "monitor", "algorithm", "variable"
    };

    srand(time(0));
    string word = words[rand() % words.size()];
    string guessed(word.length(), '_');
    string usedLetters = "";
    int maxTries = 6;
    int triesLeft = maxTries;

    cout << "HANGMAN\n";
    cout << "Guess the word!\n";

    while (triesLeft > 0 && guessed != word) {
        cout << "\nWord: " << guessed << endl;
        cout << "Tries left: " << triesLeft << endl;
        cout << "Used letters: " << usedLetters << endl;
        cout << "Enter a letter: ";

        char guess;
        cin >> guess;
        guess = tolower(guess);

        if (usedLetters.find(guess) != string::npos) {
            cout << "You already tried that letter!\n";
            continue;
        }

        usedLetters += guess;
        usedLetters += " ";

        bool found = false;
        for (int i = 0; i < word.length(); i++) {
            if (word[i] == guess) {
                guessed[i] = guess;
                found = true;
            }
        }

        if (!found) {
            triesLeft--;
            cout << "Wrong guess!\n";
        } else {
            cout << "Correct!\n";
        }
    }

    if (guessed == word) {
        cout << "\nCongratulations! You won!\n";
        cout << "The word was: " << word << endl;
    } else {
        cout << "\nGame Over! You lost.\n";
        cout << "The word was: " << word << endl;
    }

    return 0;
}
