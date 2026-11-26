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
    cout << "         THE HOLLOW SAINT\n";
    cout << "   a medieval legend, told in choices\n";
    cout << "========================================\n\n";

    cout << "The village of Ashmere has not rung its bell in nine nights.\n";
    cout << "Old women say the Hollow Saint walks the marsh when the bell is silent.\n";
    cout << "He was a holy man once. He gave his name to the fen so the children\n";
    cout << "would not be taken. The fen kept the name, and then it kept him.\n\n";
    cout << "You are a traveling scribe. The reeve paid you a silver penny to write\n";
    cout << "down what is true, and to bring back proof the Saint is only a story.\n\n";

    bool hasSalt = false;
    bool hasName = false;
    bool blessed = false;
    int dread = 0;

    int c = ask(
        "Dusk. The village gate is barred from the inside. A boy watches you\n"
        "through a crack and will not open it.\n"
        "  1. Offer the silver penny for shelter\n"
        "  2. Ask the way to the chapel on the marsh\n"
        "  3. Walk the fen road alone before full dark\n"
        "> ",
        1, 3);

    if (c == 1) {
        cout << "\nThe boy shakes his head. \"Silver won't buy a night. Salt might.\"\n";
        cout << "An old woman unbars a side door. She presses a twist of coarse salt\n";
        cout << "into your palm. \"Put it on the tongue if something speaks kindly.\"\n";
        hasSalt = true;
    } else if (c == 2) {
        cout << "\n\"Chapel's drowned,\" the boy says. \"Saint's still in it.\"\n";
        cout << "He points toward a line of willows. He will not say the Saint's name.\n";
        cout << "\"Names are doors,\" he whispers, and shuts the crack.\n";
    } else {
        cout << "\nYou take the fen road. The reeds are taller than a man.\n";
        cout << "Something walks parallel to you, not on the path, matching your steps.\n";
        dread++;
        cout << "When you stop, it stops. When you go on, it goes on.\n";
    }

    pause();

    cout << "\nYou reach a standing stone half-sunk in black water. Carved on it,\n";
    cout << "almost worn away, is a single word in church Latin. A name.\n\n";

    c = ask(
        "  1. Read the name aloud\n"
        "  2. Copy it into your book, but do not speak it\n"
        "  3. Scrape the letters out with your knife\n"
        "> ",
        1, 3);

    if (c == 1) {
        cout << "\nThe name tastes like iron. The reeds go still.\n";
        cout << "A voice, very near, very gentle, answers with your own name.\n";
        cout << "You never told it to anyone in Ashmere.\n";
        hasName = true;
        dread += 2;
    } else if (c == 2) {
        cout << "\nYou copy the letters carefully. The ink beads, as if the page is wet.\n";
        cout << "You have the name. You have not given it breath.\n";
        hasName = true;
    } else {
        cout << "\nThe knife skids. The stone bleeds a dark sap that is not water.\n";
        cout << "Far off, the village bell rings once, though no one pulls the rope.\n";
        dread++;
        cout << "You have angered an old courtesy.\n";
    }

    pause();

    cout << "\nFog takes the path. Lanterns appear ahead: three of them, low,\n";
    cout << "like someone walking with a light held at the knee. Will-o'-wisps,\n";
    cout << "the legends say, or the Saint's altar boys, who never grew up.\n\n";

    c = ask(
        "  1. Follow the lights\n"
        "  2. Turn your back and walk toward the village bell\n"
        "  3. Sprinkle salt in a circle and wait\n"
        "> ",
        1, 3);

    bool atChapel = false;

    if (c == 1) {
        atChapel = true;
        cout << "\nThe lights lead you to a chapel sunk to its windows in the fen.\n";
        cout << "The door is open. Inside, water covers the floor. The pews are gone.\n";
        cout << "A figure in a rotted alb stands where the altar was, face hollow\n";
        cout << "as a chapel niche. He does not breathe. He is waiting to be named.\n";
        dread++;
    } else if (c == 3) {
        if (!hasSalt) {
            cout << "\nYou have no salt. You only have your hands.\n";
            cout << "The lights drift closer until one rests on your boot like a moth.\n";
            cout << "Your foot goes numb. You stumble, and the fen takes the path.\n";
            dread += 2;
            atChapel = true;
            cout << "When you can feel your foot again, you are at the drowned chapel.\n";
        } else {
            cout << "\nYou pour the salt in a ring. The lights stop at its edge.\n";
            cout << "One flares, annoyed, and gutters out. The other two flee.\n";
            cout << "In the quiet, you hear hymn-singing under the water.\n";
            blessed = true;
            cout << "\nAt dawn-gray, the fog thins. The chapel roof shows itself.\n";
            atChapel = true;
        }
    } else {
        cout << "\nYou walk toward the memory of the bell. The village is closer\n";
        cout << "than it should be. Every door is open. Every hearth is cold.\n";
        cout << "On the green, the villagers stand in a circle, facing outward,\n";
        cout << "eyes shut, mouths moving in a prayer with no sound.\n\n";

        int v = ask(
            "  1. Shake the reeve awake\n"
            "  2. Slip through them toward the church\n"
            "  3. Leave Ashmere and never write the tale\n"
            "> ",
            1, 3);

        if (v == 3) {
            if (dread >= 3 || (hasName && !blessed)) {
                ending(
                    "THE ROAD REMEMBERS",
                    "You leave at a walk, then a run. The milestones change.\n"
                    "Each one bears the Saint's worn name, and under it, yours,\n"
                    "freshly cut. By the third stone you understand the bargain\n"
                    "the holy man made: the fen does not want a saint.\n"
                    "It wants a replacement. The road ends at standing water.\n"
                    "Your book is already open on a sunken pew.");
            } else {
                ending(
                    "UNWRITTEN",
                    "You do not look back. In the next town you spend the penny\n"
                    "on bread and say you found nothing worth ink. That is almost\n"
                    "true. Some nights your shadow kneels when you do not.\n"
                    "You never correct it. Ashmere is not on any map you trust.");
            }
            return 0;
        }

        if (v == 1) {
            cout << "\nThe reeve's eyes open all white. He smiles with your mouth's shape.\n";
            cout << "\"You brought it a scribe,\" he says. \"It likes things written true.\"\n";
            dread += 2;
        } else {
            cout << "\nThey do not grab you. They lean, very slightly, to let you pass,\n";
            cout << "as a congregation leans for a priest. You hate that.\n";
            dread++;
        }

        cout << "The church door is barred with a rosary of finger-bones.\n";
        atChapel = false;
    }

    pause();

    if (!atChapel) {
        cout << "\nInside the village church, the altar cloth is pulled back.\n";
        cout << "Under it is not stone. It is fen water, black and level,\n";
        cout << "and a hand in a rotted sleeve rests on the surface like a bookmark.\n\n";

        c = ask(
            "  1. Take the hand, as if helping a man from a well\n"
            "  2. Read the name from your book over the water\n"
            "  3. Burn the book and the altar cloth\n"
            "> ",
            1, 3);

        if (c == 1) {
            ending(
                "THE SECOND SAINT",
                "The hand is cold and grateful. It pulls only a little.\n"
                "You kneel, because that is what the stories say a good man does.\n"
                "The water takes you to the chest, then the throat.\n"
                "When the villagers open their eyes, a new figure stands\n"
                "where the altar was, face kind, mouth hollow, already holy.\n"
                "They will not ring the bell. They have no need.\n"
                "The marsh has its saint again.");
            return 0;
        }

        if (c == 2) {
            if (!hasName) {
                ending(
                    "EMPTY PRAYER",
                    "You have no name to give. You speak a psalm instead.\n"
                    "The hand closes on your wrist with a drowning man's strength.\n"
                    "The legend was never about salvation. It was about a trade.\n"
                    "By morning the pews are dry, and the book on the lectern\n"
                    "is written in your hand, though you did not write it:\n"
                    "a life of the saint, and the last page is still wet.");
                return 0;
            }
            if (blessed || hasSalt) {
                ending(
                    "NAMED AND BOUND",
                    "You speak the worn Latin once. The water flinches.\n"
                    "You speak it again, and the salt on your skin stings like truth.\n"
                    "The hand sinks. A sigh moves through the church, old and tired,\n"
                    "the sound of a bargain finally kept to the letter.\n"
                    "At dawn the villagers wake sore and ashamed and alive.\n"
                    "They ring the bell until the rope blisters their palms.\n"
                    "You write the tale, but you leave the name out.\n"
                    "Some doors should stay shut, even in a true account.");
                return 0;
            }
            ending(
                "THE NAME ANSWERS",
                "You speak the name. The water speaks yours back, fondly.\n"
                "Names are doors, the boy said. You opened both.\n"
                "The Hollow Saint rises wearing your traveling cloak.\n"
                "He thanks you, gently, for the loan of a life.\n"
                "Your book fills itself with a kinder version of the night,\n"
                "in which the scribe went home, and the saint stayed buried.\n"
                "Neither of those sentences is true.");
            return 0;
        }

        if (dread >= 3) {
            ending(
                "ASH ON THE WATER",
                "The book catches. The cloth catches. The water does not.\n"
                "Flame sits on it like oil. The villagers begin to sing at last,\n"
                "and the hymn is your handwriting read aloud.\n"
                "You burn with the altar, and the fen keeps the cinders,\n"
                "which is another way of keeping a saint.");
        } else {
            ending(
                "A RUDE MERCY",
                "Fire eats the book, the cloth, the finger-bone rosary.\n"
                "The hand withdraws, offended, like a guest turned from the door.\n"
                "It is not destroyed. Old legends rarely are.\n"
                "But it is no longer invited. Ashmere rings its bell at dusk\n"
                "for a year and a day. You leave poorer, unpublished, alive.\n"
                "In the marshes, something walks without a name.\n"
                "That is safer than walking with yours.");
        }
        return 0;
    }

    cout << "\nThe drowned chapel smells of incense and rot. The Hollow Saint\n";
    cout << "turns his empty face toward you. When he speaks, it is the voice\n";
    cout << "from the standing stone, polite as a priest at a deathbed.\n\n";
    cout << "  \"Write me true,\" he says, \"or take my place. Those are the rites.\"\n\n";

    c = ask(
        "  1. Write his legend exactly as he tells it\n"
        "  2. Speak his name and command him back under the water\n"
        "  3. Offer yourself, so the village will be spared\n"
        "  4. Refuse both rites and walk out\n"
        "> ",
        1, 4);

    if (c == 1) {
        if (dread >= 3) {
            ending(
                "GOSPEL OF THE FEN",
                "You write until your fingers split. He tells you the children\n"
                "he did not save, the names he ate to stay holy, the bell\n"
                "he silenced so no one would call him back. When the book closes,\n"
                "it is scripture. Ashmere will read it every winter.\n"
                "You leave with clean hands and a stained soul, which is the\n"
                "ordinary end of men who make a living from other people's fear.\n"
                "The Saint bows. He has what he wanted: to be believed.");
        } else {
            ending(
                "A TRUE ACCOUNT",
                "You write only what you saw, not what he wishes.\n"
                "The ink steams. He grows thin, a story losing believers.\n"
                "\"Cruel,\" he says, almost admiring. \"Truth without worship.\"\n"
                "He sinks to the chest, then the throat, then the hollow face.\n"
                "Your book holds one honest page and many that stay blank.\n"
                "The reeve will not like it. The fen, for once, does not argue.");
        }
        return 0;
    }

    if (c == 2) {
        if (!hasName) {
            ending(
                "NO AUTHORITY",
                "You invent a holy word. He inclines his head, patient.\n"
                "\"That is not my name.\" The water rises over the threshold.\n"
                "You are still searching your memory when it covers your mouth.\n"
                "Below, the pews are full of scribes who also guessed.");
            return 0;
        }
        if (blessed || hasSalt) {
            ending(
                "THE RITE REVERSED",
                "You speak the name you copied and did not give away.\n"
                "Salt burns on your tongue. The Saint kneels, not you.\n"
                "\"A fair clerk,\" he murmurs, and the fen closes over him\n"
                "like a book. In Ashmere the bell rings by living hands.\n"
                "You do not stay to be thanked. Legends get hungry again\n"
                "when gratitude turns into worship.");
        } else {
            ending(
                "SPOKEN TOO LOUD",
                "The name is correct. Your right to speak it is not.\n"
                "It leaps from your mouth into his hollow face and fills it.\n"
                "He becomes solid, heavy, smiling. \"Now I can leave,\" he says.\n"
                "He walks toward the village wearing a body the marsh no longer needs.\n"
                "You remain in the chapel, name-empty, which is a kind of peace\n"
                "and a kind of grave.");
        }
        return 0;
    }

    if (c == 3) {
        ending(
            "THE BARGAIN KEPT",
            "You step into the water of your own will. It is colder than sin\n"
            "and kinder than you expected. The Saint sets a hand on your head\n"
            "in blessing, and for a moment he is only a tired man again.\n"
            "Then he is gone into the fog, released, and you are the one\n"
            "standing at the altar with a hollow face and a gentle voice.\n"
            "Ashmere's children sleep safely. That was always the price.\n"
            "Someone, years from now, will be paid a penny to prove you\n"
            "are only a story. You will be polite when they arrive.");
        return 0;
    }

    if (hasSalt && dread < 3) {
        ending(
            "NO RITE",
            "You turn your back on the altar. Old things hate that.\n"
            "The Saint calls your name once. You put salt on your tongue\n"
            "and do not answer. The chapel falls behind you like a bad dream\n"
            "that cannot cross a threshold. By the road, dawn is a thin blade.\n"
            "You throw the silver penny into the fen. Some wages are too expensive.\n"
            "Your book stays empty. Empty is not the same as safe,\n"
            "but it is the best ending a living scribe gets.");
    } else {
        ending(
            "THE FEN KEEPS THE PAGE",
            "You walk out. The door is polite and lets you. The marsh is not.\n"
            "Every path returns to the chapel step. On the ninth return,\n"
            "your book is already inside, open, and the first line reads:\n"
            "There once was a scribe who refused the rite.\n"
            "You sit to cross it out. The quill moves in a hand that is\n"
            "almost yours. The legend continues. It no longer needs you awake.");
    }

    return 0;
}
