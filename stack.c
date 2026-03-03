#include "evalexpr.h"

int stack_mul(struct token *tok, struct fifo *fifo, struct fifo *rpn,
              struct token **stack)
{
    if (fifo_head(fifo) == 0 && (tok->type == DIV || tok->type == MOD))
    {
        free_stack(*stack);
        return 3;
    }
    if (fifo->head != NULL
        && (fifo->head->type == MUL || fifo->head->type == MOD
            || fifo->head->type == DIV || fifo->head->type == ADD
            || fifo->head->type == SUB))
    {
        free_stack(*stack);
        return 2;
    }
    while (*stack != NULL && (*stack)->type != PAO && (*stack)->type != ADD
           && (*stack)->type != SUB)
    {
        struct token *h = *stack;
        fifo_push(rpn, h);
        *stack = (*stack)->next;
    }
    tok->next = *stack;
    *stack = tok;
    return -1;
}

int stack_exp(struct token *tok, struct fifo *fifo, struct token **stack)
{
    if (fifo->head->type == MUL || fifo->head->type == MOD
        || fifo->head->type == DIV)
    {
        free_stack(*stack);
        return 2;
    }
    if (fifo_head(fifo) < 0)
    {
        free_stack(*stack);
        return 2;
    }
    tok->next = *stack;
    *stack = tok;
    return -1;
}

int m(struct token *tok)
{
    if (tok->type == UAD || tok->type == USU || tok->type == MUN
        || tok->type == PAO)
    {
        return 1;
    }
    return 0;
}
