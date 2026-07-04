#include <stdio.h>
#include <testVision.h>

//get input from ca on what it sees and post it

bb_post(VISION_DATA, sizeof(struct vision_data), &vision_data);
