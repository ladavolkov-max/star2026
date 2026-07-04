//imports for drawing
import javax.swing.*;
import java.awt.*;
import javax.swing.JComponent;

//imports for keyboard import
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


class ShapeDrawing_mwk extends JComponent implements KeyListener
{
    //adding variables to track position for movement
    private int xOffset = 0;
    private int yOffset = 0;
    private final int speed = 10; //how many pixels to move per click
    
    //actually drawing all the shapes
    public void paint(Graphics g)
    {
        Graphics2D g2 = (Graphics2D) g;
        g2.drawRect(100, 150, 100, 100);
        g2.drawRect(200, 150, 100, 100);
        
        int[] xcoords = {120+xOffset,120+xOffset,180+xOffset};
        int[] ycoords = {160+yOffset, 220+yOffset,190+yOffset};
        int numPoints = 3;
        g.drawPolygon(xcoords, ycoords, numPoints);
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
        
        //rerun paint method with new offsets
        repaint();
    }
    //methods we're required to override
    @Override
    public void keyReleased(KeyEvent e){}
    @Override
    public void keyTyped(KeyEvent e) {}
}

public class MoveWithKeys
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
        ShapeDrawing_mwk drawing = new ShapeDrawing_mwk();
        
        //add the drawing panel to our canvas/window frame
        f.getContentPane().add(drawing);
        
        //connect the window frame's keyboard to the drawing
        f.addKeyListener(drawing);
        
        f.setVisible(true);
    }
}
