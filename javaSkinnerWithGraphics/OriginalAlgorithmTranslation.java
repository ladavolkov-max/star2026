//input and output functions
import java.io.*;
//randomizer/generator
import java.util.Random; 

public class OriginalAlgorithmTranslation
{
    //main def and throws = not handling errors ourselves just letting them crash w an error msg
    public static void main(String[] args) throws IOException, InterruptedException
    {
        //setup to launch the external ca program----------------------------
        
        //get the user's home dir path (different file separators for dif OSs)
        String userHome = System.getProperty("user.home");
        
        //checking if the user has a windows cause then you need dif ca file name
        String os = System.getProperty("os.name").toLowerCase();
        //if windows it's ca.exe otherwise just ca
        String caName = os.contains("win") ? "ca.exe" : "ca";
        
        //building the paths to the necessary files
        String caPath = userHome + File.separator + "Desktop" + File.separator + caName;
        String cfgPath = userHome + File.separator + "Desktop" + File.separator + "skinner.cfg";
        
        //sets up external launcher that runs ca w cfg as an argument (like ./ca skinner.cfg in terminal)
        ProcessBuilder pb = new ProcessBuilder(caPath, cfgPath);
        //keeps program's error output separate from it's normal output of results
        pb.redirectErrorStream(false);
        //runs the launcher so the program is going on in the background
        Process pid = pb.start();
        //gets the pipe for sending commands to the ca, stuff written here goes into ca's input
        OutputStream stdin = pid.getOutputStream();
        //gets the pipe for receiving commands to the ca
        //pid.getInputStream gets the data of ca's output in bytes
        //new InputStreamReader translates the bytes into characters
        //new BufferedReader groups characters so that we can read them line by line
        BufferedReader stdout = new BufferedReader(new InputStreamReader(pid.getInputStream()));
        
        //main loop----------------------------------------------------------
        
        //creating a random generator
        Random random = new Random();
        
        //number codes
        //1:1N, 2:1E, 3:1S, 4:1W, 5:2N, 6:2E, 7:2S, 8:2W, 9:F
        //1:Left, 2:Right, 3:Move, 4:Press
        
        //outer loop represents running the CA 300 times (every iteration = 1 trial)
        for(int i = 0; i < 300; i++)
        {
            //choose a random location to start at (tile 1 or 2)
            int loc;
            double d = random.nextDouble();
            if(d > 0.5)
            {
                loc = 2;
            }
            else
            {
                loc = 1;
            }
            
            //choose a random direction to start at (1=N, 2=E, 3=S, 4=W)
            int dir;
            d = random.nextDouble();
            if(d > 0.75)
            {
                dir = 1; //N
            }
            else if(d > 0.5)
            {
                dir = 2; //E
            }
            else if (d > 0.25)
            {
                dir = 3; //S
            }
            else
            {
                dir = 4; //W
            }
            
            //writing which iteration we're on to stderr to track it
            System.err.println("Iteration: " + i);
            
            //inner loop represents the number of actions tha CA takes e/ trial (max 50)
            //if the CA successfully navigates to press for the food, exit loop early
            boolean successfulPress = false;
            //declared outside bc we want to print it later after the loop finishes
            int j = 0;
            for(j = 0; j < 50; j++)
            {
                //encoding our current location and direction into a number and putting it in the expected command format
                String cmd = ((loc - 1) * 4 + dir) + "/1\n";
                //convert the string to bytes and sends it to the CA
                stdin.write(cmd.getBytes("UTF-8"));
                //forces it to send immediately
                stdin.flush();
                
                //read one line of the CA's outputted response
                String x = stdout.readLine();
                //safety check for if the CA crashed/closed unexpectedly
                if(x == null)
                {
                    System.out.println("CA CRASH/STOP");
                    break;
                }
                
                //reading the code of the response action
                char response = x.charAt(0);
                //translating the response code into the appropriate action
                if(response == '1') //turn left
                {
                    //decrement dir, wrap back around if needed
                    dir -= 1;
                    if(dir == 0)
                    {
                        dir = 4;
                    }
                }
                else if(response == '2') //turn right
                {
                    //increment dir, wrap back around if needed
                    dir += 1;
                    if(dir > 4)
                    {
                        dir = 1;
                    }
                }
                else if(response == '3') //move forward
                {
                    //if on tile 1 and facing east, move to tile 2
                    if(loc == 1 && dir == 2)
                    {
                        loc = 2;
                    }
                    //if on tile 2 and facing west, move to tile 1
                    else if(loc == 2 && dir == 4)
                    {
                        loc = 1;
                    }
                    //otherwise can't move
                }
                else if(response == '4') //press
                {
                    //successful press if on tile 2 and facing east
                    if(loc == 2 && dir == 2)
                    {
                        //send the special command for it
                        stdin.write("9/1\n".getBytes("UTF-8"));
                        //send it immediately
                        stdin.flush();
                        //read CA's response line
                        stdout.readLine();
                        successfulPress = true;
                        break;
                    }
                }
            }
            //send reset command to set up the next trial
            stdin.write("0/1\n".getBytes("UTF-8"));
            //send it immediately
            stdin.flush();
            //read CA's response line
            stdout.readLine();
            //print the iteration/trial number and how many steps it took
            //if reached successfulPress then print that, otherwise 50
            System.out.println(i + " " + (successfulPress ? (j+1) : 50));
        }
        //once all trials are done, shut down the CA process so that it doesn't keep running in bg
        pid.destroy();
    }
}





















