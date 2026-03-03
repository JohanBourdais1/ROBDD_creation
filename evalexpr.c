#include "evalexpr.h"

char* read_stdin(void)
{
    char* expr = malloc(32 * sizeof(char));
    int i = 0;
    int r;
    while ((r = fread(expr, sizeof(char), 32, stdin)) > 0)
    {
        if (r == -1)
        {
            return NULL;
        }
        expr = realloc(expr, (i + r + 1) * sizeof(char));
        i += r;
    }
    expr[i] = 0;
    return expr;
}

struct token* create_tok(int value, int i)
{
    struct token* tok = malloc(sizeof(struct token));
    tok->value = -1;
    if (i == 1)
    {
        tok->value = value;
        tok->type = INT;
    }
    else if (value == '+')
    {
        tok->type = OR;
    }
    else if (value == '.')
    {
        tok->type = AND;
    }
    else if (value == '!')
    {
        tok->type = NOT;
    }
    else if (value == '*')
    {
        tok->type = XOR;
    }
    else
    {
        free(tok);
        return NULL;
    }
    tok->next = NULL;
    return tok;
}

int split_tok(char* expr, struct fifo* fifo)
{
    if (expr == NULL || expr[1] == 0)
    {
        return 0;
    }
    size_t i = 0;
    while (expr[i] != 0)
    {
        struct token* tok = NULL;
        if ((expr[i] >= 'a' && expr[i] <= 'z')
            || (expr[i] >= 'A' && expr[i] <= 'Z'))
        {
            return 1;
        }
        else if (expr[i] == ' ' || expr[i] == '\n')
        {
            i++;
            continue;
        }
        int v = 0;
        if (expr[i] >= '0' && expr[i] <= '9')
        {
            while (expr[i] != 0 && expr[i] >= '0' && expr[i] <= '9')
            {
                v = v * 10;
                v += expr[i] - '0';
                i++;
            }
            tok = create_tok(v, 1);
        }
        else
        {
            tok = create_tok(expr[i], 0);
            i++;
        }
        if (tok == NULL)
        {
            return 1;
        }
        fifo_push(fifo, tok);
    }
    return 5;
}

int my_pow(int a, int n)
{
    int i = 1;
    while (n != 0)
    {
        i *= a;
        n--;
    }
    return i;
}

int eval_(int n1, int n2, struct token* tok)
{
    if (tok->type == ADD)
    {
        return n1 + n2;
    }
    else if (tok->type == SUB)
    {
        return n2 - n1;
    }
    else if (tok->type == MUL || tok->type == MUN)
    {
        return n1 * n2;
    }
    else if (tok->type == DIV)
    {
        return n2 / n1;
    }
    else if (tok->type == MOD)
    {
        return n2 % n1;
    }
    return my_pow(n2, n1);
}

void free_stack(struct token* stack)
{
    while (stack != NULL)
    {
        struct token* tmp = stack->next;
        free(stack);
        stack = tmp;
    }
}

int eval_expr(struct fifo* fifo)
{
    struct token* stack = NULL;
    while (fifo->size > 0)
    {
        struct token* tok = fifo_pop(fifo);
        if (tok->type == INT)
        {
            tok->next = stack;
            stack = tok;
        }
        else
        {
            if (tok->type == USU)
            {
                stack->value = -stack->value;
            }
            else if (tok->type != UAD)
            {
                struct token* n1 = stack;
                if ((n1 == NULL || n1->next == NULL || n1->next->type != INT
                     || n1->type != INT)
                    || (tok->type == EXP && stack->value < 0))
                {
                    free(tok);
                    free_stack(stack);
                    return 2;
                }
                if (tok->type == DIV || tok->type == MOD)
                {
                    if (stack->value == 0)
                    {
                        free(tok);
                        free_stack(stack);
                        return 3;
                    }
                }
                stack = stack->next;
                stack->value = eval_(n1->value, stack->value, tok);
                free(n1);
            }
            free(tok);
        }
    }
    int res = stack->value;
    free_stack(stack);
    return res;
}

void free_all(char* expr, struct fifo* fifo, struct fifo* rpn)
{
    if (expr != NULL)
    {
        free(expr);
    }
    if (fifo != NULL)
    {
        fifo_clear(fifo);
        free(fifo);
    }
    if (rpn != NULL)
    {
        fifo_clear(rpn);
        free(rpn);
    }
}
