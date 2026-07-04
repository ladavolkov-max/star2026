//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//imports for keyboard input
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

//handle interaction w OneTrialForGraphics class
import java.io.*;
import java.util.ArrayList;

class Drawing extends JComponent implements KeyListener
{
    //variables for triangle
    private double xOffset = 0;
    private double yOffset = 0;
    private final double speed = 60.0;
    private double angle = 0;
    
    //grid layout constants
    private final int StartX = 100;
    private final int StartY = 100;
    private final int size = 60;
    
    //whether the lever was pressed (for drawing press action)
    private boolean pressed = false;
    //whether the trial ended w a press (for drawing final press)
    private boolean lastPress = false;
    //the bot that will be running the trials
    private OneTrialForGraphics bot;
    //timer that steps through the trial frame by frame
    private Timer timer;
    //list of steps from the current trial
    private ArrayList<int[]> steps;
    //which step we're currently on
    private int currentStep = 0;
    //frame rate in milliseconds between steps
    private final int frameDelay = 400;
    //response display
    private String responseLabel = "";
    
    //constructor for the shape drawing class: makes a new test subject
    public Drawing() throws IOException
    {
        bot = new OneTrialForGraphics();
    }
    
    //translating the numerical codes for location and direction into pixel offsets and rotation angle
    private void applyLocDir(int loc, int dir)
    {
        //loc 1 = left box = no offset, loc 2 = right box = shifted right
        xOffset = (loc - 1) * size;
        yOffset = 0;
        
        //convert direction to angle in radians
        if(dir == 1)
        {
            angle = -Math.PI / 2; //N
        }
        else if(dir == 2)
        {
            angle = 0; //E
        }
        else if(dir == 3)
        {
            angle = Math.PI / 2; //S
        }
        else if(dir == 4)
        {
            angle = Math.PI; //W
        }
    }
    
    //starting a new trial and its playback
    private void startNewTrial()
    {
        //stop any currently running timer
        if(timer != null && timer.isRunning())
        {
            timer.stop();
        }
        
        //resetting relevant variables
        pressed = false;
        currentStep = 0;
        lastPress = false;
        responseLabel = "";
        
        //running the trial to get the array list
        try
        {
            steps = bot.runOneTrial();
        }
        catch(IOException ex)
        {
            System.out.println("Error running trial: " + ex.getMessage());
            return;
        }
        
        //setting up the timer passing it the frame rate and 
        //the actions to do on each tick as a lambda function
        //parameter -> actions replacing the traditional ActionListener
        timer = new Timer(frameDelay,
        e ->
        {
            //still have steps to take
            if(currentStep < steps.size())
            {
                //breaking down the current step we're on
                int[] step = steps.get(currentStep);
                int loc = step[0];
                int dir = step[1];
                int response = step[2];
                int frameType = step[3]; //0=before, 1=after
                
                //processing this information for the graphics to render
                applyLocDir(loc, dir);
                
                //before response = show current state and the action it's about to do
                //after response = show updated position (result of previously displayed response) w/o response label
                if(frameType == 0) //shows what's about to happen
                {
                    pressed = false;
                    //assigning response label
                    switch((char)response)
                    {
                        case '1': responseLabel = "L"; break; // turn left
                        case '2': responseLabel = "R"; break; // turn right
                        case '3': responseLabel = "M"; break; // move
                        case '4': responseLabel = "P"; break; // press
                        default: responseLabel = "--"; break; //do nothing
                    }
                }
                else //shows result of the action
                {
                    responseLabel = "";
                    pressed = (response == (int)'4');
                    if(pressed && currentStep == steps.size() - 1)
                    {
                        lastPress = true;
                    }
                }
                //forces clearing window and render changes
                repaint(); 
                currentStep++;
            }
            else //all steps done
            {
                timer.stop();
                responseLabel = "";
                pressed = lastPress;
                //repaints one more time to end on the state of the last action
                SwingUtilities.invokeLater(() -> repaint());
                System.out.println("End of trial. enter = next trial, q = quit");
            }
        }
        );
        
        //starting the timer
        timer.start();
    }
    
    //actually drawing all the shapes
    @Override
    public void paint(Graphics g)
    {
        Graphics2D g2 = (Graphics2D) g;
        
        //starting settings for the grid
        int startX = 100;
        int startY = 100;
        int size = 60;
        int rowCount = 1;
        int colCount = 2;
        for(int row = 0; row < rowCount;  row++)
        {
            for(int col = 0; col < colCount; col++)
            {
                int currentX = startX + (col * size);
                int currentY = startY + (row * size);
                g2.drawRect(currentX, currentY, size, size);
            }
        }
        g2.drawRect(210, 110, 10, 40);
        
        //drawing the response label inside the triangle
        if(!responseLabel.isEmpty())
        {
            g2.setFont(new Font("Arial", Font.PLAIN, 12));
            g2.drawString(
            responseLabel,
            (int)(startX + 20 + xOffset),
            (int)(startY + 35 + yOffset)
            );
        }
        
        //printing on screen
        /*
        int frameType = responseLabel.isEmpty() ? 0 : 1;
        g2.setFont(new Font("Arial", Font.PLAIN, 12));
        g2.drawString("frame type: " + frameType, 50, 50);
        g2.drawString("press: " + pressed, 50, 65);
        g2.drawString("lastPress: " + lastPress, 50, 80);
        */
        
        //saving the old unrotated polygon
        java.awt.geom.AffineTransform oldTransform = g2.getTransform();
        
        //calculate the center of the triangle
        //(take avg of all x vals and all y vals and add offset)
        double centerX = startX + (size/2.0) + xOffset;
        double centerY = startY + (size/2.0) + yOffset;
        
        //applying the rotaiton to the triangle around its center point
        g2.rotate(angle, centerX, centerY);
        
        //drawing the triangle
        int[] xcoords = {
            (int)(startX + 12 + xOffset),
            (int)(startX + 12 + xOffset),
            (int)(startX + 48 + xOffset)
        };
        int[] ycoords = {
            (int)(startY + 12 +yOffset),
            (int)(startY + 48 +yOffset),
            (int)(startY + 30 +yOffset)
        };
        int numPoints = 3;
        g2.drawPolygon(xcoords, ycoords, numPoints);
        
        //draw the circle either filled or unfilled
        if(pressed || lastPress)
        {
            g2.fillOval(xcoords[2], ycoords[2]-4, 8, 8);
        }
        else
        {
            g2.drawOval(xcoords[2], ycoords[2]-4, 8, 8);
        }
        
        //restore the triangle back to normal so that we can keep 
        //applying the appropriate rotations
        g2.setTransform(oldTransform);
    }
    
    //responding to keyboard input
    @Override
    public void keyPressed(KeyEvent e)
    {
        int keyCode = e.getKeyCode();
        
        //enter starts the trial
        if(keyCode == KeyEvent.VK_ENTER)
        {
            startNewTrial();
        }
        
        //q quits the experiment
        if(keyCode == KeyEvent.VK_Q)
        {
            if(timer != null)
            {
                timer.stop();
                bot.shutdown();
                System.exit(0);
            }
        }
    }
    
    //methods we're required to override
    @Override
    public void keyReleased(KeyEvent e){}
    @Override
    public void keyTyped(KeyEvent e) {}
}

public class GraphicsConnected
{
    public static void main(String[] args) throws IOException
    {
        JFrame f = new JFrame();
        int w = 640;
        int h = 480;
        f.setSize(w, h);
        f.setTitle("Skinner Graphics");
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        //creating an instance of our class above
        Drawing drawing = new Drawing();
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        //connect the window frame's keyboard to the drawing
        f.addKeyListener(drawing);
        
        f.setVisible(true);
        
        System.out.println("Go to graphics window: enter = next trial, q = quit");
    }
}
