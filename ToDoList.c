#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TASKS 100
#define MAX_LEN   256
#define FILENAME  "todos.txt"

typedef struct {
    char text[MAX_LEN];
    int done;
} Task;

Task tasks[MAX_TASKS];
int task_count = 0;

void load_tasks() {
    FILE *f = fopen(FILENAME, "r");
    if (!f) return;

    char line[MAX_LEN + 10];
    while (fgets(line, sizeof(line), f) && task_count < MAX_TASKS) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) < 3) continue;

        tasks[task_count].done = (line[0] == '1');
        strncpy(tasks[task_count].text, line + 2, MAX_LEN - 1);
        task_count++;
    }
    fclose(f);
}

void save_tasks() {
    FILE *f = fopen(FILENAME, "w");
    if (!f) {
        perror("Cannot save");
        return;
    }
    for (int i = 0; i < task_count; i++) {
        fprintf(f, "%d %s\n", tasks[i].done, tasks[i].text);
    }
    fclose(f);
}

void list_tasks() {
    if (task_count == 0) {
        printf("No tasks yet.\n");
        return;
    }
    printf("\n===== TODO LIST =====\n");
    for (int i = 0; i < task_count; i++) {
        printf("%2d. [%c] %s\n", i + 1, tasks[i].done ? 'X' : ' ', tasks[i].text);
    }
    printf("=====================\n");
}

void add_task(const char *text) {
    if (task_count >= MAX_TASKS) {
        printf("Task list is full!\n");
        return;
    }
    strncpy(tasks[task_count].text, text, MAX_LEN - 1);
    tasks[task_count].done = 0;
    task_count++;
    printf("Added: %s\n", text);
}

void mark_done(int index) {
    if (index < 1 || index > task_count) {
        printf("Invalid task number\n");
        return;
    }
    tasks[index - 1].done = 1;
    printf("Marked as done: %s\n", tasks[index - 1].text);
}

void delete_task(int index) {
    if (index < 1 || index > task_count) {
        printf("Invalid task number\n");
        return;
    }
    printf("Deleted: %s\n", tasks[index - 1].text);
    for (int i = index - 1; i < task_count - 1; i++) {
        tasks[i] = tasks[i + 1];
    }
    task_count--;
}

int main() {
    char command[32];
    char arg[MAX_LEN];

    load_tasks();
    printf("Simple Todo Manager (type 'help' for commands)\n");

    while (1) {
        printf("\n> ");
        if (scanf("%31s", command) != 1) break;

        if (strcmp(command, "list") == 0 || strcmp(command, "ls") == 0) {
            list_tasks();
        }
        else if (strcmp(command, "add") == 0) {
            getchar(); // consume space
            if (fgets(arg, sizeof(arg), stdin)) {
                arg[strcspn(arg, "\n")] = 0;
                if (strlen(arg) > 0) add_task(arg);
            }
        }
        else if (strcmp(command, "done") == 0) {
            int num;
            if (scanf("%d", &num) == 1) mark_done(num);
        }
        else if (strcmp(command, "delete") == 0 || strcmp(command, "rm") == 0) {
            int num;
            if (scanf("%d", &num) == 1) delete_task(num);
        }
        else if (strcmp(command, "help") == 0) {
            printf("Commands:\n");
            printf("  list / ls          - Show all tasks\n");
            printf("  add <text>         - Add a new task\n");
            printf("  done <number>      - Mark task as done\n");
            printf("  delete / rm <num>  - Delete a task\n");
            printf("  save               - Save and exit\n");
            printf("  quit / exit        - Exit without saving\n");
        }
        else if (strcmp(command, "save") == 0) {
            save_tasks();
            printf("Saved. Goodbye!\n");
            break;
        }
        else if (strcmp(command, "quit") == 0 || strcmp(command, "exit") == 0) {
            printf("Exiting without saving.\n");
            break;
        }
        else {
            printf("Unknown command. Type 'help'.\n");
        }
    }
    return 0;
}
