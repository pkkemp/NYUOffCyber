#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct {
  char *material;
  ssize_t size;
} boot;

#define BOOTS_CAPACITY 20
boot *boots[BOOTS_CAPACITY];
ssize_t boot_index = 0;

void run_cmd(char* arg) {
  system(arg);
}

void new_boot() {
  if (boot_index == BOOTS_CAPACITY) {
    puts("ah we can't have any more new boots :(");
    return;
  }

  printf("Ah a new boot!\n");

  boot *b = malloc(sizeof(boot));

  puts("So nice to meet you! What size is your boot?");

  char buf[0x20];
  fgets(buf, 0x20, stdin);

  b->size = strtoul(buf, NULL, 0); // can be whatever base you desire

  b->material = malloc(b->size);

  puts("What material is your boot made of?");

  fgets(b->material, b->size, stdin);

  printf("Ok, your boot is stored at %lu\n", boot_index);

  boots[boot_index++] = b;
}

void bye_boot() {
  printf("Aw these boots are getting old.\n");

  printf("Which boot do you not want anymore?\n");

  char buf[0x20];
  fgets(buf, 0x20, stdin);

  ssize_t index = strtoul(buf, NULL, 0); // can be whatever base you desire

  if (index >= boot_index) {
    printf("Sorry, we can't throw away imaginary boots...\n");
    return;
  }

  boot *b = boots[index];
  if (boot_index > 0) {
    boots[index] = boots[boot_index - 1];
    boot_index -= 1;
  }

  free(b->material);
  free(b);
}

void read_boot() {
  puts("Ah what fancy boots you have!");

  puts("Which one are we appraising today?");

  char buf[0x20];
  fgets(buf, 0x20, stdin);

  ssize_t index = strtoul(buf, NULL, 0); // can be whatever base you desire

  if (index >= boot_index) {
    puts("Sorry, we can't appraise ghost boots");
    return;
  }

  boot *b = boots[index];
  printf("%s\n", b->material);
}

void edit_boot() {
  puts("Do you not like a boot?");

  puts("Which boot shall we replace today?");

  char buf[0x20];
  fgets(buf, 0x20, stdin);

  ssize_t index = strtoul(buf, NULL, 0); // can be whatever base you desire

  if (index >= boot_index) {
    puts("I wish I could change the fact that you don't have a boot there...");
    return;
  }

  boot *b = boots[index];

  puts("What's the new material of your boot?");
  ssize_t bytes_read = read(0, b->material, b->size);

  b->material[bytes_read] = 0;
}

void menu() {
  puts("1. Create a new boot");
  puts("2. Delete a boot");
  puts("3. Appraise a boot");
  puts("4. Edit a boot");
  puts("5. Exit");
  printf("> ");
}

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  char buf[0x20];

  for (;;) {
    menu();
    fflush(stdout);
    fgets(buf, 0x20, stdin);
    ssize_t choice = strtoul(buf, NULL, 0); // can be whatever base you desire

    switch (choice) {
    case 1:
      new_boot();
      break;
    case 2:
      bye_boot();
      break;
    case 3:
      read_boot();
      break;
    case 4:
      edit_boot();
      break;
    case 5:
      puts("good bye!");
      return 0;
    }
  }
}
