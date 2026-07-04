//stuff to connect to c++ if necessary
#ifdef CPLUSPLUS
extern "C" {
#endif

//externally visible function 
void *testVision_init(void *dummy);

//symbolic name for the data that will be posted to the blackboard
#define VISION_DATA 0x00020001 
//numbers??????????????????????????
//numbers??????????????????????????
//numbers??????????????????????????

//encoding what we actually send to the blackboard
enum VISION_SCENARIO
{
    VISION_SCENARIO_CORNER_FL = 0,
    VISION_SCENARIO_CORNER_FR = 1,
    VISION_SCENARIO_WALL_L = 2,
    VISION_SCENARIO_WALL_R = 3,
    VISION_SCENARIO_WALL_F = 4,
    VISION_SCENARIO_NONE = 5,
    VISION_SCENARIO_BAR_F = 6,
    VISION_SCENARIO_BAR_L = 7,
    VISION_SCENARIO_BAR_R = 8
}

//defining the structure to post to blackboard
struct vision_data
{
    enum VISION_SCENARIO scenario;
};

//stuff to connect to c++ if necessary
#ifdef CPLUSPLUS
}
#endif
