/*
 * Blackboard support functions
 */

#include <sys/time.h>
#include <pthread.h>
#include <stdlib.h>
#include "bb.h"

pthread_mutex_t bb_lock = PTHREAD_MUTEX_INITIALIZER ;

struct bb_item {
   long label ;
   int size ;
   void *data ;
   struct timeval stamp ;
   struct bb_item *next ;
} ;

struct bb_wait {
   pthread_cond_t cond ;
   long *labels ;
   struct timeval **stamps ;
   int nlabel ;
   struct bb_wait *next ;
} ;

static struct bb_item *bb_lookup( long label ) ;

struct bb_item *bb_head = NULL ;
struct bb_wait *bb_whead = NULL ;

/*
 * Add an item to the blackboard.  If we've already
 * got one with that label, we just replace it.
 */
int bb_post( long label, int n, void *data )
{
   struct bb_item *p ;
   struct bb_wait *q ;
   int i ;

   pthread_mutex_lock( &bb_lock ) ;
   p = bb_lookup( label ) ;
   if( p == NULL ) {
      p = malloc( sizeof( struct bb_item )) ;
      if( p == NULL ) {
         pthread_mutex_unlock( &bb_lock ) ;
         return( 0 ) ;
      }
      p->label = label ;
      p->next = bb_head ;
      bb_head = p ;
   }
   p->size = n ;
   p->data = data ;
   gettimeofday( &p->stamp, NULL ) ;
   for( q = bb_whead; q; q = q->next ) {
      for( i = 0; i < q->nlabel && q->labels[i] != p->label; ++i ) ;
      if( i < q->nlabel )
         pthread_cond_signal( &q->cond ) ;
   }
   pthread_mutex_unlock( &bb_lock ) ;
   return( 1 ) ;
}

/*
 * Get a pointer to the data belonging to the
 * given label.
 */
void *bb_read( long label, int *n, struct timeval *stamp )
{
   struct bb_item *p ;

   pthread_mutex_lock( &bb_lock ) ;
   p = bb_lookup( label ) ;
   if( p == NULL ) {
      pthread_mutex_unlock( &bb_lock ) ;
      return( NULL ) ;
   }
   if( n )
      *n = p->size ;
   if( stamp )
      memcpy( stamp, &p->stamp, sizeof( struct timeval )) ;
   pthread_mutex_unlock( &bb_lock ) ;
   return( p->data ) ;
}

/*
 * Return a copy of the data belonging to the
 * given label.
 */
void *bb_copy( long label, int *n, struct timeval *stamp )
{
   struct bb_item *p ;
   void *q ;

   pthread_mutex_lock( &bb_lock ) ;
   p = bb_lookup( label ) ;
   if( p == NULL ) {
      pthread_mutex_unlock( &bb_lock ) ;
      return( NULL ) ;
   }
   if( n )
      *n = p->size ;
   if( stamp )
      memcpy( stamp, &p->stamp, sizeof( struct timeval )) ;
   q = malloc( p->size ) ;
   if( q == NULL )
      return( NULL ) ;
   memcpy( q, p->data, p->size ) ;
   pthread_mutex_unlock( &bb_lock ) ;
   return( q ) ;
}

/*
 * Block until we have interesting data posted.
 */
long bb_wait( long *labels, struct timeval **stamps, int nlabel )
{
   struct bb_item *p ;
   struct bb_wait *q, *r ;
   int i ;

   pthread_mutex_lock( &bb_lock ) ;
   for( i = 0; i < nlabel; ++i ) {
      p = bb_lookup( labels[i] ) ;
      if( p != NULL ) {
         if( stamps == NULL || stamps[i] == NULL
               || timercmp( stamps[i], &(p->stamp), < )) {
            pthread_mutex_unlock( &bb_lock ) ;
            return( p->label ) ;
         }
      }
   }
   q = malloc( sizeof( struct bb_wait )) ;
   if( q == NULL ) {
      pthread_mutex_unlock( &bb_lock ) ;
      return( -1 ) ;
   }
   pthread_cond_init( &q->cond, NULL ) ;
   q->labels = labels ;
   q->stamps = stamps ;
   q->nlabel = nlabel ;
   q->next = bb_whead ;
   bb_whead = q ;
   pthread_cond_wait( &q->cond, &bb_lock ) ;
   if( q == bb_whead )
      bb_whead = q->next ;
   else {
      for( r = bb_whead; r && r->next != q; r = r->next ) ;
      if( r )
         r->next = q->next ;
   }
   for( i = 0; i < nlabel; ++i ) {
      p = bb_lookup( labels[i] ) ;
      if( p != NULL ) {
         if( stamps == NULL || stamps[i] == NULL
               || timercmp( stamps[i], &(p->stamp), < )) {
            pthread_mutex_unlock( &bb_lock ) ;
            return( p->label ) ;
         }
      }
   }
   return( -1 ) ;
}

/*
 * Find a blackboard item with a given label
 */
static struct bb_item *bb_lookup( long label )
{
   struct bb_item *p ;

   for( p = bb_head; p && p->label != label; p = p->next ) ;
   return( p ) ;
}
