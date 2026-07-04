//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//imports for keyboard import
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


class ShapeDrawing_ram extends JComponent implements KeyListener
{
    //adding variables to track position for movement
    private int xOffset = 0;
    private int yOffset = 0;
    private final int speed = 10; //how many pixels to move per click
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
        int[] xcoords = {120+xOffset,120+xOffset,180+xOffset};
        int[] ycoords = {160+yOffset, 220+yOffset,190+yOffset};
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
        if(keyCode == KeyEvent.VK_UP || keyCode == KeyEvent.VK_W)
        {
            yOffset -= speed;
        }
        if(keyCode == KeyEvent.VK_DOWN || keyCode == KeyEvent.VK_S)
        {
            yOffset += speed;
        }
        if(keyCode == KeyEvent.VK_LEFT || keyCode == KeyEvent.VK_A)
        {
            xOffset -= speed;
        }
        if(keyCode == KeyEvent.VK_RIGHT || keyCode == KeyEvent.VK_D)
        {
            xOffset += speed;
        }
        
        //rotation keys: 1=Left 2=Right
        if (keyCode == KeyEvent.VK_1)
        {
            angle -= Math.PI / 2; 
        }
        if (keyCode == KeyEvent.VK_2)
        {
            angle += Math.PI / 2; 
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

public class RotateAndMove
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
        ShapeDrawing_ram drawing = new ShapeDrawing_ram();
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        //connect the window frame's keyboard to the drawing
        f.addKeyListener(drawing);
        
        f.setVisible(true);
    }
}
