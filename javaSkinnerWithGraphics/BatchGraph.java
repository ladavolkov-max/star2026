//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//ASK ABOUT TRIAL AND STEP NUMBERS W 0 INDEXING OR NO????
//WHAT COORD TO START AT???
class GraphDrawing extends JComponent
{
    //storing the array of points as an instance variable
    private int[] points;
    //constructor initializes it
    public GraphDrawing(int[] p)
    {
        points = p;
    }
    
    @Override
    public void paint(Graphics g)
    {
        Graphics2D g2 = (Graphics2D) g;
        
        //variables allow us to control the visual scaling and placement of the graph
        int startX = 100;
        int startY = 300;
        int spacePerX = 2; //how many pixels 1 trial takes up (4)
        int spacePerY = 5; //how many pixels 1 step takes up
        int height = 50 * spacePerY; 
        int width = 300 * spacePerX;
         
        //y axis
        g2.setFont(new Font("Arial", Font.PLAIN, 12));
        g2.drawLine(startX, startY, startX, startY - height);
        g2.drawString("number", 15, 150);
        g2.drawString("of steps", 15, 165);
        //generating the number labels and dashes to show where they are
        g2.setFont(new Font("Arial", Font.PLAIN, 6));
        for(int i = 0; i <= 50; i += 5)
        {
            g2.drawString(Integer.toString(i), startX - 10, startY + 2 - spacePerY * i);
            g2.drawLine(startX - 2, startY - spacePerY * i, startX, startY - spacePerY * i);
        }
        
        //x axis
        g2.setFont(new Font("Arial", Font.PLAIN, 12));
        g2.drawLine(startX, startY, startX + width, startY);
        g2.drawString("trial number", 330, 340);
        //generating the number labels and dashes to show where they are
        g2.setFont(new Font("Arial", Font.PLAIN, 6));
        for(int i = 0; i <= 300; i += 10)
        {
            g2.drawString(Integer.toString(i), startX - 5 + spacePerX * i, startY + 10);
            g2.drawLine(startX + spacePerX * i, startY, startX + spacePerX * i, startY + 2);
        }
         
        //graphing the lines between all the points
        int[] previousCoordinate = {0, 50};
        for(int i = 0; i < points.length; i++)
        {
            int prevX = previousCoordinate[0];
            int currX = i + 1;
            int prevY = previousCoordinate[1];
            int currY = points[i];
            
            int lineStartX = startX + prevX * spacePerX; 
            int lineEndX = startX + currX * spacePerX;
            int lineStartY = startY - prevY * spacePerY;
            int lineEndY = startY - currY * spacePerY;
            
            g2.drawLine(lineStartX, lineStartY, lineEndX, lineEndY);
            
            previousCoordinate[0] = currX;
            previousCoordinate[1] = currY;
        }
        
        //least squares linear regression--------------------------------------------
        //calculating all necessary sums
        double sumX = 0; //first manual coord - 0
        double sumY = 50; //first manual coord - 50
        double sumXY = 0; //first manual coord - 0*50=0
        double sumXsq = 0; //first manual coord - 0^2=0
        double n = points.length + 1;
        double m = 0;
        double b = 0;
        
        for(int i = 0; i < points.length; i++)
        {
            double x = i + 1;
            double y = points[i];
            sumX += x; 
            sumY += y;
            sumXY += (x * y);
            sumXsq += (x * x);
        }
        
        //slope
        m = (n * sumXY - sumX * sumY) / (n * sumXsq - Math.pow(sumX, 2));
        //y intercept
        b = (sumY - m * sumX) / n;
        //y = mx + b, we need points at x = 0 and x = endpt
        double startXmath = 0;
        double endXmath = points.length;
        double startYmath = b;
        double endYmath = m * endXmath + b;
        int startXpixel = (int)(startX + (startXmath * spacePerX));
        int endXpixel = (int)(startX + (endXmath * spacePerX));
        int startYpixel = (int)(startY - (startYmath * spacePerY));
        int endYpixel = (int)(startY - (endYmath * spacePerY));
        g2.drawLine(startXpixel, startYpixel, endXpixel, endYpixel);
        
        
        
        
        return;
    }
}

public class BatchGraph
{
    public static void main(String[] args)
    {
        //getting the points from the program (running it here ensures it runs 1 time)
        //BatchForGraphing trials = new BatchForGraphing();
        //Batch3x3ForG trials = new Batch3x3ForG();
        Batch2x2ForG trials = new Batch2x2ForG();
        int[] points;
        try
        {
            points = trials.runBatch();
        }
        catch (Exception e)
        {
            System.out.println("Error: " + e);
            return;
        }
        //fixing the zero indexing issue by adding 1 to everything
        for(int i = 0; i < points.length; i++)
        {
            points[i]++;
        }
        
        
        JFrame f = new JFrame();
        int w = 2000;
        int h = 500;
        f.setSize(w, h);
        f.setTitle("Graphing Batch of Skinner Trials");
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        //creating an instance of our class above
        GraphDrawing drawing = new GraphDrawing(points);
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        f.setVisible(true);
        
        System.out.println("DONE");
    }
}