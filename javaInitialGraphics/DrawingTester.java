import javax.swing.*;

public class DrawingTester
{
    public static void main(String[] args)
    {
        JFrame f = new JFrame();
        int w = 640;
        int h = 480;
        f.setSize(w, h);
        f.setTitle("Drawing in Java");
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}
