#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define DEFAULT_LENGTH 16

const char *lowercase = "abcdefghijklmnopqrstuvwxyz";
const char *uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const char *digits    = "0123456789";
const char *symbols   = "!@#$%^&*()-_=+[]{}|;:,.<>?";

void print_usage(const char *prog) {
    printf("Usage: %s [options]\n", prog);
    printf("  -l <num>   Length of password (default: %d)\n", DEFAULT_LENGTH);
    printf("  -u         Include uppercase letters\n");
    printf("  -d         Include digits\n");
    printf("  -s         Include symbols\n");
    printf("  -h         Show this help\n");
    printf("\nExample: %s -l 20 -u -d -s\n", prog);
}

int main(int argc, char *argv[]) {
    int length = DEFAULT_LENGTH;
    int use_upper = 0, use_digits = 0, use_symbols = 0;
    int opt;

    while ((opt = getopt(argc, argv, "l:udsh")) != -1) {
        switch (opt) {
            case 'l': length = atoi(optarg); break;
            case 'u': use_upper = 1; break;
            case 'd': use_digits = 1; break;
            case 's': use_symbols = 1; break;
            case 'h': print_usage(argv[0]); return 0;
            default:  print_usage(argv[0]); return 1;
        }
    }

    if (length < 4 || length > 128) {
        fprintf(stderr, "Length must be between 4 and 128\n");
        return 1;
    }

    char charset[256] = {0};
    strcat(charset, lowercase);
    if (use_upper)   strcat(charset, uppercase);
    if (use_digits)  strcat(charset, digits);
    if (use_symbols) strcat(charset, symbols);

    size_t charset_len = strlen(charset);
    if (charset_len == 0) {
        fprintf(stderr, "No character sets selected\n");
        return 1;
    }

    srand((unsigned)time(NULL) ^ getpid());

    char *password = malloc(length + 1);
    if (!password) {
        perror("malloc");
        return 1;
    }

    for (int i = 0; i < length; i++) {
        password[i] = charset[rand() % charset_len];
    }
    password[length] = '\0';

    printf("%s\n", password);
    free(password);
    return 0;
}
