#include <iostream>
#include <string>
#include <limits>

using namespace std;

void clearInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

int ask(const string& prompt, int minOpt, int maxOpt) {
    int choice = 0;
    while (true) {
        cout << prompt;
        if (cin >> choice && choice >= minOpt && choice <= maxOpt) {
            clearInput();
            return choice;
        }
        cout << "  (Choose a number between " << minOpt << " and " << maxOpt << ".)\n";
        clearInput();
    }
}

void pause() {
    cout << "\n[Press Enter to continue]";
    cin.get();
}

void ending(const string& title, const string& text) {
    cout << "\n========== " << title << " ==========\n\n";
    cout << text << "\n";
    cout << "\n========================================\n";
}

int main() {
    cout << "========================================\n";
    cout << "          THE LAST PLATFORM\n";
    cout << "     a choice-based horror story\n";
    cout << "========================================\n\n";
    cout << "You are alone on the last train of the night.\n";
    cout << "The car is empty. The lights flicker. Your phone has no signal.\n";
    cout << "The next stop is not on the map.\n\n";

    int sanity = 3;
    bool hasKey = false;
    bool sawName = false;

    cout << "A speaker crackles. A voice that sounds almost like yours says:\n";
    cout << "  \"Do not get off. Do not look at the windows.\"\n\n";

    int c = ask(
        "What do you do?\n"
        "  1. Stay in your seat and keep your eyes down\n"
        "  2. Look at the window anyway\n"
        "  3. Walk to the next car\n"
        "> ",
        1, 3);

    if (c == 2) {
        cout << "\nYour reflection is a half-second late. It smiles before you do.\n";
        sanity--;
        sawName = true;
        cout << "It mouths a name. It might be yours.\n";
    } else if (c == 3) {
        cout << "\nThe connecting door sticks. When it opens, the next car is identical.\n";
        cout << "Same empty seats. Same flickering light. Same wet footprint trail.\n";
    } else {
        cout << "\nYou stare at your shoes. The train does not stop when it should.\n";
        cout << "Something sits down across from you. You do not look up.\n";
    }

    pause();

    cout << "\nThe lights die for three seconds. When they return, a paper ticket\n";
    cout << "is in your hand. You did not buy one. It reads:\n";
    cout << "  DESTINATION: HOME\n";
    cout << "  CONDITION: DO NOT ANSWER IF IT KNOWS YOUR NAME\n\n";

    c = ask(
        "The train brakes. A station appears that was not there before.\n"
        "  1. Get off\n"
        "  2. Stay on the train\n"
        "  3. Hide under the seats\n"
        "> ",
        1, 3);

    bool onTrain = true;
    if (c == 1) {
        onTrain = false;
        cout << "\nThe platform is tiled in cracked white. A single bench. A locked door\n";
        cout << "marked STAFF ONLY. The train doors stay open, breathing warm air.\n";
    } else if (c == 3) {
        cout << "\nYou crawl under the seat. Something's shoes stop beside your face.\n";
        cout << "They are yours. The laces are wet.\n";
        sanity--;
        cout << "The shoes walk away. A small iron key is left on the floor.\n";
        hasKey = true;
    } else {
        cout << "\nThe doors slam. The station slides backward into fog.\n";
        cout << "A passenger is now sitting three rows ahead, facing away.\n";
    }

    pause();

    if (onTrain) {
        cout << "\nThe passenger speaks without turning.\n";
        cout << "  \"You can leave if you say your name. Just once.\"\n\n";

        c = ask(
            "  1. Stay silent\n"
            "  2. Say your name\n"
            "  3. Ask what it wants\n"
            "> ",
            1, 3);

        if (c == 2) {
            if (sawName) {
                ending(
                    "IT KNOWS",
                    "The moment the name leaves your mouth, every window shows your face\n"
                    "already home, already sitting at your table, already not blinking.\n"
                    "The train never stops again. You are the announcement now.");
                return 0;
            }
            cout << "\nYou say a name. It is not quite right. The passenger flinches.\n";
            cout << "  \"Close,\" it says. \"Try again later.\"\n";
            sanity--;
        } else if (c == 3) {
            cout << "\n  \"A seat that stays warm,\" it says. \"Yours is almost ready.\"\n";
            sanity--;
        } else {
            cout << "\nSilence stretches. The passenger stands and walks into the next car.\n";
            cout << "It leaves the iron key on the seat.\n";
            hasKey = true;
        }

        pause();

        cout << "\nThe train slows at a second station: your street, underwater-dark,\n";
        cout << "your building with every window lit except yours.\n\n";

        c = ask(
            "  1. Get off and go to your building\n"
            "  2. Use the key on the driver's cabin\n"
            "  3. Pull the emergency brake\n"
            "> ",
            1, 3);

        if (c == 2) {
            if (!hasKey) {
                ending(
                    "NO KEY",
                    "The cabin door is locked. While you rattle it, the lights go out\n"
                    "for good. Hands that feel like your own guide you back to a seat.\n"
                    "The train keeps the schedule you no longer remember agreeing to.");
                return 0;
            }
            cout << "\nThe key turns. The cabin is empty. The throttle is already forward.\n";
            cout << "A handwritten note is taped to the glass:\n";
            cout << "  IF YOU STOP THE TRAIN, IT GETS OFF WITH YOU.\n\n";

            int d = ask(
                "  1. Stop the train\n"
                "  2. Keep it moving past your stop\n"
                "> ",
                1, 2);

            if (d == 1) {
                ending(
                    "SHARED EXIT",
                    "The brakes scream. You step onto a platform that is your hallway.\n"
                    "Something steps off behind you and matches your pace exactly.\n"
                    "Your apartment door is already unlocked. Both of you go inside.");
            } else if (sanity <= 1) {
                ending(
                    "THE LONG ROUTE",
                    "You push the throttle. Stations blur into ones that were never built.\n"
                    "You are still driving when morning should have come.\n"
                    "Your reflection in the cabin glass is finally on time.\n"
                    "It waves. You do not.");
            } else {
                ending(
                    "DAWN SOMEWHERE ELSE",
                    "You ride until the fog thins. The next platform is ordinary, ugly,\n"
                    "and real. Your phone finds a signal. A text from yourself, sent\n"
                    "four minutes ago: \"Don't come home tonight.\"\n"
                    "You don't.");
            }
            return 0;
        }

        if (c == 3) {
            ending(
                "BETWEEN STOPS",
                "The brake snaps. The train halts in a tunnel with no ends.\n"
                "Every door opens onto brick. From the dark ahead, footsteps\n"
                "approach in perfect time with your heartbeat, then stop\n"
                "when you hold your breath. You cannot hold it forever.");
            return 0;
        }

        // got off toward building
        onTrain = false;
    }

    // Platform / building path
    cout << "\nYou leave the train. The doors close like a mouth.\n";
    if (!onTrain) {
        cout << "Your building's lobby smells like rain and old coins.\n";
        cout << "The elevator is waiting. The stairs are dark.\n\n";
    }

    c = ask(
        "  1. Take the elevator\n"
        "  2. Take the stairs\n"
        "  3. Turn around and wait for the next train\n"
        "> ",
        1, 3);

    if (c == 3) {
        ending(
            "NO NEXT TRAIN",
            "You wait on the platform until your legs ache. The timetable\n"
            "is blank. When you finally look back, the lobby is gone.\n"
            "There is only track, and something walking it toward you\n"
            "without needing the rails.");
        return 0;
    }

    if (c == 1) {
        cout << "\nThe elevator rises without you pressing a button.\n";
        cout << "The floor indicator skips numbers: 2, 4, 7, HOME.\n";
        if (sanity <= 1) {
            ending(
                "WRONG FLOOR",
                "The doors open on your apartment, except you are already inside,\n"
                "sitting at the table, not looking up. The you in the chair says,\n"
                "without moving its mouth, \"Close the door. You're letting it in.\"\n"
                "You were the one in the hallway the whole time.");
            return 0;
        }
        cout << "It stops. The doors open on your floor. Your door is ajar.\n\n";
    } else {
        cout << "\nThe stairs go up longer than your building is tall.\n";
        cout << "On the landing that should be yours, a wet footprint faces down,\n";
        cout << "as if someone descended while you climbed.\n";
        if (hasKey) {
            cout << "The iron key is warm in your pocket. It fits a door you have not reached.\n";
        }
        cout << "\n";
    }

    c = ask(
        "Your apartment door is ahead.\n"
        "  1. Go inside\n"
        "  2. Knock first\n"
        "  3. Leave the building and walk until morning\n"
        "> ",
        1, 3);

    if (c == 3) {
        if (sanity >= 2) {
            ending(
                "UNTIL MORNING",
                "You walk. Streetlights behave. A bakery opens. The clerk does not\n"
                "know your name, which is the kindest thing anyone has done tonight.\n"
                "You do not go home. Not today. Maybe not ever.\n"
                "Somewhere, a train keeps your seat warm.");
        } else {
            ending(
                "THE LONG WALK",
                "Every street bends back to your building. Your shoes are wet.\n"
                "When you finally stop, you are standing in your own lobby again,\n"
                "and the elevator is still waiting, patient as a held breath.");
        }
        return 0;
    }

    if (c == 2) {
        cout << "\nYou knock. From inside, you hear yourself say, \"It's open.\"\n";
        cout << "The voice is a little late, like the reflection was.\n\n";
        int d = ask(
            "  1. Go in anyway\n"
            "  2. Run\n"
            "> ",
            1, 2);
        if (d == 2) {
            ending(
                "DOWN THE STAIRS",
                "You run. The footsteps above you run too, perfectly matched.\n"
                "You burst onto the street just as the sun edges the roofs.\n"
                "Behind you the building is dark, all windows empty.\n"
                "Your phone buzzes. One new voicemail. You do not play it.");
            return 0;
        }
    }

    // entered apartment
    if (hasKey && sanity >= 2 && !sawName) {
        ending(
            "LOCK IT FROM INSIDE",
            "The apartment is empty and cold and yours. You lock the door with\n"
            "the iron key. It only turns one way. Outside, something tries the\n"
            "handle once, politely, then walks away down the stairs.\n"
            "In the morning the key is gone. The lock remains. You sleep with\n"
            "the lights on, and for now, that is enough.");
    } else if (sawName) {
        ending(
            "ALREADY HOME",
            "You step inside. The table is set for one. Your name is written\n"
            "on the napkin in your handwriting, over and over, until the letters\n"
            "stop meaning anything. You sit down. Across the city, a train\n"
            "announces a destination nobody else can hear.");
    } else {
        ending(
            "A SEAT THAT STAYS WARM",
            "The rooms are correct. The photos are correct. You are not sure\n"
            "you are. In the dark of the bedroom, the mattress dips as if\n"
            "someone sat on the edge to wait. You do not turn on the light.\n"
            "You lie down anyway. The train schedule in your pocket is blank.\n"
            "You will not need it.");
    }

    return 0;
}
