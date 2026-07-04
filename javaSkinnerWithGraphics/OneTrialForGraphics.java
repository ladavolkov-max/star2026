//setup = same imports but also scanner for user input and arraylist for return to graphics
import java.io.*;
import java.util.Random;
import java.util.Scanner;
import java.util.ArrayList;

public class OneTrialForGraphics
{
    //setup to launch the external ca program----------------------------
    //now since the setup is in the class and not a method, all the details are instance vars
    private Process pid;
    private OutputStream stdin;
    private BufferedReader stdout;
    private Random random;
    private int trialCount;
    
    //constructor method for the setup
    public OneTrialForGraphics() throws IOException
    {
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
        pid = pb.start();
        //gets the pipe for sending commands to the ca, stuff written here goes into ca's input
        stdin = pid.getOutputStream();
        //gets the pipe for receiving commands to the ca
        //pid.getInputStream gets the data of ca's output in bytes
        //new InputStreamReader translates the bytes into characters
        //new BufferedReader groups characters so that we can read them line by line
        stdout = new BufferedReader(new InputStreamReader(pid.getInputStream()));
        
        //creating a random generator
        random = new Random();
        
        trialCount = 0;
    }
    
    //method to run one trial with the same logic as the translation inner loop
    //returns an arraylist of int[] for the graphics to then interpret
    //each int[] is: [location, direction, response, frame type]
    public ArrayList<int[]> runOneTrial() throws IOException
    {
        ArrayList<int[]> steps = new ArrayList<>();
        
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
        
        //handle CA's responses
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
            
            //adding our information to the array list to return
            //before position change (0)
            steps.add(new int[] {loc, dir, (int)response, 0});
            
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
                    //adding our information to the array list to return
                    //after position change (1)
                    steps.add(new int[] {loc, dir, (int)response, 1}); //for last frame before break
                    break;
                }
            }
            //adding our information to the array list to return
            //after position change (1)
            steps.add(new int[] {loc, dir, (int)response, 1});
        }
        //send reset command to set up the next trial
        stdin.write("0/1\n".getBytes("UTF-8"));
        //send it immediately
        stdin.flush();
        //read CA's response line
        stdout.readLine();
        
        //printing results for the trial and updating for next time
        System.out.println(
        "Trial " + (trialCount + 1) + " finished in " +
        (successfulPress ? (j + 1) : 50) + " steps. " +
        (successfulPress ? "Lever pressed!" : "Lever not pressed."));
        trialCount++;
        return steps;
    }
    
    //method to stop the trials for this CA 
    public void shutdown()
    {
        pid.destroy();
        System.out.println("CA process shut down.");
    }
    
    //main method takes user input and runs one trial at a time
    public static void main(String[] args) throws IOException
    {
        //creating a CA to run our trials on
        OneTrialForGraphics bot = new OneTrialForGraphics();
        
        Scanner scanner = new Scanner(System.in);
        System.out.println("enter = run trial, q then enter = quit");
        while(true)
        {
            //reading user input
            String input = scanner.nextLine();
            //sees if input = q (case insensitive) to quit
            if(input.equalsIgnoreCase("q"))
            {
                bot.shutdown();
                break;
            }
            bot.runOneTrial();
        }
    }
}
