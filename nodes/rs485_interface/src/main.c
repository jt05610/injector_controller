#include "app.h"

int
main(int argc, char *argv[])
{
    App app = app_create();
    app_init(app);
    app_run(app);
    app_destroy(app);
    return 0;
}
