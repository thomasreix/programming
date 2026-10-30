#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#define EMPTY -1
#define NONE -1

#define O 0
#define X 1

#define RESET "\033[0m"
#define BOLD  "\033[1m"

void help(const char *program){
    printf("Usage: %s [-g] [-b] [-gb] [-h]\n\n", program);
    printf("Options:\n");
    printf("  -g    Enable graphics mode\n");
    printf("  -b    Play against the bot\n");
    printf("  -gb   Enable graphics and play against the bot\n");
    printf("  -h    Display this help message\n");
}

int flags(int argc, char *argv[], bool *graphics, bool *bot_mode){
    for(int i = 1; i < argc; i++){
        if(strcmp(argv[i], "-gb") == 0){
            *graphics = true;
            *bot_mode = true;
        }
        else if(strcmp(argv[i], "-g") == 0){
            *graphics = true;
        }
        else if(strcmp(argv[i], "-b") == 0){
            *bot_mode = true;
        }
        else if(strcmp(argv[i], "-h") == 0){
            help(argv[0]);
            return 1;
        }
        else{
            fprintf(stderr, "Unknown option: %s\n\n", argv[i]);
            help(argv[0]);
            return -1;
        }
    }

    return 0;
}

void display(int size, int board[size][size], bool graphics,
             const char *message){
    if(graphics){
        printf("\033[u");
    }

    for(int y = 0; y < size; y++){
        if(graphics){
            printf("\r\033[2K");
        }

        for(int x = 0; x < size; x++){
            int cell = board[y][x];

            if(cell == EMPTY){
                printf(" %d", y * size + x + 1);
            }
            else if(cell == O){
                printf(graphics ? " %sO%s" : " O",
                       graphics ? BOLD : "",
                       graphics ? RESET : "");
            }
            else if(cell == X){
                printf(graphics ? " %sX%s" : " X",
                       graphics ? BOLD : "",
                       graphics ? RESET : "");
            }
        }

        printf(graphics ? "\r\n" : "\n");
    }

    if(graphics){
        printf("\r\033[2K%s", message ? message : "");
        fflush(stdout);
    }
}

bool ask(int *move, bool graphics){
    char input[100];

    if(!graphics){
        printf("Selected cell: ");
    }

    fflush(stdout);

    if(fgets(input, sizeof(input), stdin) == NULL){
        return false;
    }

    if(sscanf(input, "%d", move) != 1){
        *move = 0;
    }

    return true;
}

void empty(int size, int board[size][size]){
    for(int y = 0; y < size; y++){
        for(int x = 0; x < size; x++){
            board[y][x] = EMPTY;
        }
    }
}

bool valid(int move, int size, int board[size][size]){
    if(move < 1 || move > size * size){
        return false;
    }

    int x = (move - 1) % size;
    int y = (move - 1) / size;

    return board[y][x] == EMPTY;
}

void update(int size, int board[size][size], int move, int player){
    int x = (move - 1) % size;
    int y = (move - 1) / size;

    board[y][x] = player;
}

int bot(int board[3][3]){
    const int win_combinations[8][3] = {
        {0, 1, 2},
        {0, 3, 6},
        {3, 4, 5},
        {6, 7, 8},
        {1, 4, 7},
        {2, 5, 8},
        {0, 4, 8},
        {2, 4, 6}
    };

    const int priority_cells[9] = {
        4, 0, 2, 6, 8, 1, 3, 5, 7
    };

    for(int i = 0; i < 8; i++){
        int a = win_combinations[i][0];
        int b = win_combinations[i][1];
        int c = win_combinations[i][2];

        int A = board[a / 3][a % 3];
        int B = board[b / 3][b % 3];
        int C = board[c / 3][c % 3];

        if(A != EMPTY && A == B && C == EMPTY){
            return c + 1;
        }
        else if(B != EMPTY && B == C && A == EMPTY){
            return a + 1;
        }
        else if(C != EMPTY && C == A && B == EMPTY){
            return b + 1;
        }
    }

    for(int i = 0; i < 9; i++){
        int cell = priority_cells[i];

        if(board[cell / 3][cell % 3] == EMPTY){
            return cell + 1;
        }
    }
}

bool check_win(int size, int board[size][size], int player){
    for(int i = 0; i < size; i++){
        bool row = true;
        bool column = true;

        for(int j = 0; j < size; j++){
            if(board[i][j] != player){
                row = false;
            }

            if(board[j][i] != player){
                column = false;
            }
        }

        if(row || column){
            return true;
        }
    }

    bool diagonal_A = true;
    bool diagonal_B = true;

    for(int i = 0; i < size; i++){
        if(board[i][i] != player){
            diagonal_A = false;
        }

        if(board[i][size - 1 - i] != player){
            diagonal_B = false;
        }
    }

    return diagonal_A || diagonal_B;
}

bool full(int size, int board[size][size]){
    for(int y = 0; y < size; y++){
        for(int x = 0; x < size; x++){
            if(board[y][x] == EMPTY){
                return false;
            }
        }
    }

    return true;
}

int main(int argc, char *argv[]){
    bool graphics = false;
    bool bot_mode = false;

    int result = flags(argc, argv, &graphics, &bot_mode);

    if(result != 0){
        return result > 0 ? 0 : 1;
    }

    int size = 3;
    int board[size][size];

    empty(size, board);

    if(graphics){
        printf("\033[s");
        fflush(stdout);
    }

    int player = O;
    int winner = NONE;
    bool finished = false;

    while(!finished){
        int move;

        if(bot_mode && player == X){
            if(!graphics){
                display(size, board, false, NULL);
            }

            move = bot(board);

            if(!graphics){
                printf("Bot selects cell %d\n", move);
            }
        }
        else{
            bool invalid = false;

            do{
                if(graphics){
                    display(size, board, true,
                            invalid
                            ? "Invalid move. Selected cell: "
                            : "Selected cell: ");
                }
                else if(!invalid){
                    display(size, board, false, NULL);
                }

                if(!ask(&move, graphics)){
                    printf("\n");
                    return 0;
                }

                invalid = !valid(move, size, board);

                if(invalid && !graphics){
                    printf("Invalid move. Try again.\n");
                }
            } while(invalid);
        }

        update(size, board, move, player);

        if(check_win(size, board, player)){
            winner = player;
            finished = true;
        }
        else if(full(size, board)){
            finished = true;
        }

        if(!finished){
            player = !player;
        }
    }

    display(size, board, graphics, "");

    if(winner != NONE){
        printf("Player %c has won the game!\n",
               winner == O ? 'O' : 'X');
    }
    else{
        printf("There is a draw!\n");
    }

    return 0;
}