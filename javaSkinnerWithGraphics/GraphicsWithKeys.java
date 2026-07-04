//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//imports for keyboard input
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


class ShapeDrawing extends JComponent implements KeyListener
{
    //adding variables to track position for movement
    private double xOffset = 0;
    private double yOffset = 0;
    private final double speed = 60.0; //how many pixels to move per click
    //rotation in radians
    private double angle = 0;
    
    //actually drawing all the shapes
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
        g2.drawOval(xcoords[2], ycoords[2]-4, 8, 8);
        
        //restore the triangle back to normal so that we can keep 
        //applying the appropriate rotations
        g2.setTransform(oldTransform);
    }
    
    //responding to keyboard input
    @Override
    public void keyPressed(KeyEvent e)
    {
        int keyCode = e.getKeyCode();
        
        //rotation keys: 1=Left 2=Right
        if (keyCode == KeyEvent.VK_1)
        {
            angle -= Math.PI / 2; 
        }
        if (keyCode == KeyEvent.VK_2)
        {
            angle += Math.PI / 2; 
        }
        
        //moving will calculate the x and y offset w trig based on angle
        if (keyCode == KeyEvent.VK_3)
        {
            //Math.cos for horizontal forward movement
            xOffset += (int) (speed * Math.cos(angle));
            
            //Math.sin for vertical forward movement
            yOffset += (int) (speed * Math.sin(angle));
        }
        
        //rerun paint method with new offsets
        repaint();
    }
    //methods we're required to override
    @Override
    public void keyReleased(KeyEvent e){}
    @Override
    public void keyTyped(KeyEvent e) {}
}

public class GraphicsWithKeys
{
    public static void main(String[] args)
    {
        JFrame f = new JFrame();
        int w = 640;
        int h = 480;
        f.setSize(w, h);
        f.setTitle("Skinner Graphics");
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        //creating an instance of our class above
        ShapeDrawing drawing = new ShapeDrawing();
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        //connect the window frame's keyboard to the drawing
        f.addKeyListener(drawing);
        
        f.setVisible(true);
    }
}
