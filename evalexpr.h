#ifndef EVALEXPR_H
#define EVALEXPR_H

#include <assert.h>
#include <ctype.h>
#include <err.h>
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum token_type
{
    INT,
    AND,
    OR,
    XOR,
    NOT
};

struct token
{
    enum token_type type;
    char name;
    int value;
    struct token* next;
};

struct node
{
    char name;
    int value;
    struct node* left;
    struct node* right;
};

struct fifo
{
    struct token* head;
    struct token* tail;
    size_t size;
};

int m(struct token* tok);
void free_stack(struct token* stack);
int g(struct fifo* fifo);
int f(struct fifo* fifo);
int is_operator(char c);
int par(char c);
int stack_exp(struct token* tok, struct fifo* fifo, struct token** stack);
void next_stack(struct token** stack, struct token* tok);
int stack_mul(struct token* tok, struct fifo* fifo, struct fifo* rpn,
              struct token** stack);
void _stack_n(struct token** stack, struct token* tok);
int clear_all(struct token* tok, struct fifo* fifo, struct fifo* rpn, int i);
void _stack(struct token** stack, struct fifo* rpn);
void free_all(char* expr, struct fifo* fifo, struct fifo* rpn);
int split_token(char* expr, struct fifo* fifo);
int convert_std(struct fifo* fifo, struct fifo* rpn);
char* read_stdin(void);
int split_tok(char* expr, struct fifo* fifo);
int eval_expr(struct fifo* fifo);
struct fifo* fifo_init(void);
void fifo_push(struct fifo* fifo, struct token* tok);
int fifo_head(struct fifo* fifo);
struct token* fifo_pop(struct fifo* fifo);
void fifo_clear(struct fifo* fifo);
void fifo_destroy(struct fifo* fifo);

#endif /* !EVALEXPR_H */
