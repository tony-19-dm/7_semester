#include <vingraph.h>
#include <unistd.h>

int main() {
    ConnectGraph();
    Clear(0);
    Fill(0, RGB(135, 206, 235));

    // Горы 
    tPoint mountains[] = {{0, 300}, {100, 150}, {200, 250}, {300, 100}, 
                        {400, 200}, {500, 120}, {600, 180}, {700, 80}, {800, 250}};
    Polygon(mountains, 9, RGB(120, 120, 120));
    Fill(Polygon(mountains, 9, RGB(120, 120, 120), 0), RGB(120, 120, 120));
    
    // Озеро
    tPoint lake[] = {{0, 400}, {0, 600}, {800, 600}, {800, 450}, 
                    {700, 400}, {600, 380}, {500, 390}, {400, 370}, 
                    {300, 390}, {200, 370}, {100, 380}};
    Polygon(lake, 11, RGB(30, 144, 255));
    Fill(Polygon(lake, 11, RGB(30, 144, 255), 0), RGB(30, 144, 255));
    
    // Лодка
    tPoint boat[] = {{400, 380}, {500, 380}, {550, 350}, {350, 350}};
    Polygon(boat, 4, RGB(139, 69, 19));
    Fill(Polygon(boat, 4, RGB(139, 69, 19), 0), RGB(139, 69, 19));
    
    // Мачта лодки
    Line(450, 350, 450, 300, RGB(101, 67, 33));
    
    // Парус
    tPoint sail[] = {{450, 300}, {490, 340}, {450, 340}};
    Polygon(sail, 3, RGB(255, 255, 255));
    Fill(Polygon(sail, 3, RGB(255, 255, 255), 0), RGB(255, 255, 255));
    
    // Солнце
    int sun = Ellipse(650, 80, 60, 60, RGB(255, 215, 0));
    Fill(sun, RGB(255, 215, 0));
    
    // Птицы 
    Arc(200, 100, 30, 20, 0, 1800, RGB(0, 0, 0));
    Arc(230, 100, 30, 20, 0, 1800, RGB(0, 0, 0));
    Arc(300, 150, 25, 15, 0, 1800, RGB(0, 0, 0));
    Arc(325, 150, 25, 15, 0, 1800, RGB(0, 0, 0));
    
    
    // Облака
    int cloud1 = Ellipse(100, 70, 70, 40, RGB(255, 255, 255));
    Fill(cloud1, RGB(255, 255, 255));
    int cloud2 = Ellipse(500, 50, 80, 35, RGB(255, 255, 255));
    Fill(cloud2, RGB(255, 255, 255));
    
    delay(30000);
    
    CloseGraph();
    return 0;
}