#include "evalexpr.h"

struct fifo *fifo_init(void)
{
    struct fifo *q = malloc(sizeof(struct fifo));
    if (q == NULL)
    {
        return NULL;
    }
    q->head = NULL;
    q->tail = NULL;
    q->size = 0;
    return q;
}

void fifo_clear(struct fifo *fifo)
{
    if (fifo == NULL || fifo->head == NULL || fifo->size == 0)
    {
        return;
    }
    struct token *q = fifo->head;
    while (q != NULL)
    {
        struct token *w = q->next;
        free(q);
        q = w;
    }

    fifo->size = 0;
    fifo->head = NULL;
    fifo->tail = NULL;
}

int is_operator(char c)
{
    if (c == '+' || c == '-' || c == '/' || c == '*' || c == '%' || c == '^'
        || c == '(' || c == ')')
    {
        return 1;
    }
    return 0;
}

int par(char c)
{
    if (c == '(')
    {
        return 1;
    }
    return 0;
}

int f(struct fifo *fifo)
{
    if (fifo->tail != NULL && fifo->tail->type != INT
        && fifo->tail->type != PAF)
    {
        return 1;
    }
    return 0;
}

int g(struct fifo *fifo)
{
    if (fifo->head != NULL
        && (fifo->head->type == MUL || fifo->head->type == MOD
            || fifo->head->type == DIV))
    {
        return 1;
    }
    return 0;
}
