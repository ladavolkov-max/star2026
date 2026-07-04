//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//imports for keyboard import
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


class ShapeDrawing_csm extends JComponent implements KeyListener
{
    //adding variables to track position for movement
    private double xOffset = 0;
    private double yOffset = 0;
    private final double speed = 50.0; //how many pixels to move per click
    //rotation in radians
    private double angle = 0;
    
    //actually drawing all the shapes
    public void paint(Graphics g)
    {
        Graphics2D g2 = (Graphics2D) g;
        g2.drawRect(100, 150, 100, 100);
        g2.drawRect(200, 150, 100, 100);
        
        //saving the old unrotated polygon
        java.awt.geom.AffineTransform oldTransform = g2.getTransform();
        
        //calculate the center of the triangle
        //(take avg of all x vals and all y vals and add offset)
        double centerX = 140 + xOffset;
        double centerY = 190 + yOffset;
        
        //applying the rotaiton to the triangle around its center point
        g2.rotate(angle, centerX, centerY);
        
        //drawing the triangle
        int[] xcoords = {(int)(120+xOffset),(int)(120+xOffset),(int)(180+xOffset)};
        int[] ycoords = {(int)(160+yOffset), (int)(220+yOffset),(int)(190+yOffset)};
        int numPoints = 3;
        g2.drawPolygon(xcoords, ycoords, numPoints);
        
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

public class CompleteSkinnerMovement
{
    public static void main(String[] args)
    {
        JFrame f = new JFrame();
        int w = 640;
        int h = 480;
        f.setSize(w, h);
        f.setTitle("Drawing in Java");
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        //creating an instance of our class above
        ShapeDrawing_csm drawing = new ShapeDrawing_csm();
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        //connect the window frame's keyboard to the drawing
        f.addKeyListener(drawing);
        
        f.setVisible(true);
    }
}
