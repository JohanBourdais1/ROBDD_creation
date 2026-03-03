#include "evalexpr.h"

void fifo_push(struct fifo *fifo, struct token *tok)
{
    if (tok == NULL)
    {
        return;
    }
    if (fifo->tail == NULL)
    {
        fifo->tail = tok;
        fifo->head = tok;
    }
    else
    {
        fifo->tail->next = tok;
        fifo->tail = tok;
    }
    fifo->size += 1;
}

int fifo_head(struct fifo *fifo)
{
    return fifo->head->value;
}

struct token *fifo_pop(struct fifo *fifo)
{
    if (fifo->head == NULL)
    {
        return NULL;
    }
    struct token *q = fifo->head;
    fifo->head = q->next;
    fifo->size -= 1;
    return q;
}

void _stack(struct token **stack, struct fifo *rpn)
{
    while (*stack != NULL && (*stack)->type != PAO)
    {
        struct token *h = *stack;
        fifo_push(rpn, h);
        *stack = (*stack)->next;
    }
}

void _stack_n(struct token **stack, struct token *tok)
{
    struct token *q = *stack;
    *stack = (*stack)->next;
    free(q);
    free(tok);
}
