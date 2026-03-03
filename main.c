#include "evalexpr.h"

int main(int argc, char* argv[])
{
    char* expr = argv[1];
    char* order = calloc(argc - 1, 1);
    for (int i = 2; i < argc; i++)
    {
        order[i - 2] = argv[i];
    }
    struct fifo* fifo = fifo_init();
    struct fifo* rpn = fifo_init();
    int e;
    e = split_token(expr, fifo, order);
    if (e == 5)
    {
        e = convert_std(fifo, rpn);
        if (e == 0)
        {
            printf("%d\n", eval_expr(rpn));
            free_all(expr, fifo, rpn);
            return 0;
        }
    }
    else
    {
        free_all(fifo, rpn);
        return e;
    }
    free_all(fifo, rpn);
    return e;
}
