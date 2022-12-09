#include <stdbool.h>
#include "service_layer/app.h"

int
main(int argc, char *argv[])
{
    App app = app_create();
    app_run(app);

    app_destroy(app);
    return 0;
}
