//setup = same imports but also scanner for user input
import java.io.*;
import java.util.Random;
import java.util.Scanner;
import java.util.ArrayList;

public class OneTrialGrid3x3ForG
{
    //setup to launch the external ca program----------------------------
    //now since the setup is in the class and not a method, all the details are instance vars
    private Process pid;
    private OutputStream stdin;
    private BufferedReader stdout;
    private Random random;
    private int trialCount;
    
    //constructor method for the setup
    public OneTrialGrid3x3ForG() throws IOException
    {
        //get the user's home dir path (different file separators for dif OSs)
        String userHome = System.getProperty("user.home");
        
        //checking if the user has a windows cause then you need dif ca file name
        String os = System.getProperty("os.name").toLowerCase();
        //if windows it's ca.exe otherwise just ca
        String caName = os.contains("win") ? "ca.exe" : "ca";
        
        //building the paths to the necessary files
        String caPath = userHome + File.separator + "Desktop" + File.separator + caName;
        String cfgPath = userHome + File.separator + "Desktop" + File.separator + "skinnerVision.cfg";
        
        //sets up external launcher that runs ca w cfg as an argument (like ./ca skinner.cfg in terminal)
        ProcessBuilder pb = new ProcessBuilder(caPath, cfgPath);
        //keeps program's error output separate from it's normal output of results
        pb.redirectErrorStream(false);
        //runs the launcher so the program is going on in the background
        pid = pb.start();
        
        //debug lines
        /*
        System.out.println("ca path: " + caPath);
        System.out.println("cfg path: " + cfgPath);
        System.out.println("Process alive? " + pid.isAlive());
        */
        
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
    public ArrayList<int[]> runOneTrial() throws IOException
    {
        ArrayList<int[]> steps = new ArrayList<>();
        
        //choose a random location to start at (tile 1 - 9)
        int loc;
        double d = random.nextDouble();
        if(d < 1/9.0) loc = 1;
        else if(d < 2/9.0) loc = 2;
        else if(d < 3/9.0) loc = 3;
        else if(d < 4/9.0) loc = 4;
        else if(d < 5/9.0) loc = 5;
        else if(d < 6/9.0) loc = 6;
        else if(d < 7/9.0) loc = 7;
        else if(d < 8/9.0) loc = 8;
        else loc = 9;
            
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
            int visualSymbol = getVisionScenario(loc, dir);
            String cmd = (visualSymbol + "/1\n");
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
            steps.add(new int[] {loc, dir, (int)response, 0, visualSymbol});
            
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
                //(1=N, 2=E, 3=S, 4=W)
                //1 2 3 
                //4 5 6
                //7 8 9
                //detremining if you're allow you to move based on location
                boolean canMoveUp = true;
                boolean canMoveDown = true;
                boolean canMoveLeft = true;
                boolean canMoveRight = true;
                if(loc == 1 || loc == 2 || loc == 3)
                {
                    canMoveUp = false;
                }
                if(loc == 7 || loc == 8 || loc == 9)
                {
                    canMoveDown = false;
                }
                if(loc == 1 || loc == 4 || loc == 7)
                {
                    canMoveLeft = false;
                }
                if(loc == 3 || loc == 6 || loc == 9)
                {
                    canMoveRight = false;
                }
                //actually moving
                if(dir == 1 && canMoveUp)
                {
                    loc -= 3;
                }
                else if(dir == 3 && canMoveDown)
                {
                    loc += 3;
                }
                else if(dir == 4 && canMoveLeft)
                {
                    loc -= 1;
                }
                else if(dir == 2 && canMoveRight)
                {
                    loc += 1;
                }
            }
            else if(response == '4') //press
            {
                //successful press if on tile 9 and facing east
                if(loc == 9 && dir == 2)
                {
                    //send the special command for it FOOD SYMBOL
                    stdin.write("10/1\n".getBytes("UTF-8"));
                    //send it immediately
                    stdin.flush();
                    //read CA's response line
                    stdout.readLine();
                    successfulPress = true;
                    //adding our information to the array list to return
                    //after position change (1)
                    steps.add(new int[] {loc, dir, (int)response, 1, -100});
                    break;
                }
            }
            //adding our information to the array list to return
            //after position change (1)
            steps.add(new int[] {loc, dir, (int)response, 1, -100});
        }
        //send reset command to set up the next trial
        stdin.write("0/1\n".getBytes("UTF-8"));
        //send it immediately
        stdin.flush();
        //read CA's response line
        stdout.readLine();
        
        //printing results for the trial and updating for next time
        System.out.println(
        "Episode " + trialCount + " finished in " +
        (successfulPress ? (j + 1) : 50) + " steps. " +
        (successfulPress ? "Lever pressed!" : "Lever not pressed."));
        trialCount++;
        return steps;
    }
    
    //method for determining what the CA sees
    public int getVisionScenario(int loc, int dir)
    {
        //(1=N, 2=E, 3=S, 4=W)
        //1 2 3 
        //4 5 6
        //7 8 9
        if(//corner front left
        (loc == 1 && dir == 1) ||
        (loc == 3 && dir == 2) ||
        (loc == 7 && dir == 4))
        {
            return 1;
        }
        else if(//corner front left
        (loc == 1 && dir == 4) ||
        (loc == 3 && dir == 1) ||
        (loc == 7 && dir == 3))
        {
            return 2;
        }
        else if(//wall left
        (loc == 1 && dir == 2) ||
        (loc == 2 && dir == 2) ||
        (loc == 3 && dir == 3) ||
        (loc == 6 && dir == 3) ||
        (loc == 9 && dir == 4) ||
        (loc == 8 && dir == 4) ||
        (loc == 7 && dir == 1) ||
        (loc == 4 && dir == 1))
        {
            return 3;
        }
        else if(//wall right
        (loc == 1 && dir == 3) ||
        (loc == 2 && dir == 4) ||
        (loc == 3 && dir == 4) ||
        (loc == 6 && dir == 1) ||
        (loc == 8 && dir == 2) ||
        (loc == 7 && dir == 2) ||
        (loc == 4 && dir == 3))
        {
            return 4;
        }
        else if(//wall front
        (loc == 2 && dir == 1) ||
        (loc == 6 && dir == 2) ||
        (loc == 8 && dir == 3) ||
        (loc == 4 && dir == 4))
        {
            return 5;
        }
        else if(//none
        (loc == 2 && dir == 3) ||
        (loc == 6 && dir == 4) ||
        (loc == 8 && dir == 1) ||
        (loc == 4 && dir == 2) ||
        (loc == 5))
        {
            return 6;
        }
        else if(//bar left
        (loc == 9 && dir == 3))
        {
            return 7;
        }
        else if(//bar right
        (loc == 9 && dir == 1))
        {
            return 8;
        }
        else if(//bar front
        (loc == 9 && dir == 2))
        {
            return 9;
        }
        else
        {
            return -1;
        }
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
        OneTrialGrid3x3ForG bot = new OneTrialGrid3x3ForG();
        
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
