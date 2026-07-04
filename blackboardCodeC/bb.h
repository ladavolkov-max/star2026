int bb_post( long label, int n, void *data ) ;
void *bb_read( long label, int *n, struct timeval *stamp ) ;
void *bb_copy( long label, int *n, struct timeval *stamp ) ;
long bb_wait( long *labels, struct timeval **stamps, int nlabel ) ;
