#include <vingraph.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <stdlib.h>
#include <time.h>

// Глобальные переменные для управления потоками
volatile int running = 1;
pthread_t threads[6];

// Обработчик сигнала для корректного завершения
void signal_handler(int sig) {
    running = 0;
}

// Поток для движущегося прямоугольника
void* moving_rect_thread(void* arg) {
    int x = 100, y = 100;
    int dx = 3, dy = 2;
    int color = RGB(255, 0, 0);
    int size = 40;
    
    int rect = Rect(x, y, size, size, color);
    Fill(rect, color);
    
    while (running) {
        x += dx;
        y += dy;
        
        // Отскок от границ экрана
        if (x <= 0 || x >= 800 - size) {
            dx = -dx;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(rect, color);
            Fill(rect, color);
        }
        if (y <= 0 || y >= 600 - size) {
            dy = -dy;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(rect, color);
            Fill(rect, color);
        }
        
        MoveTo(x, y, rect);
        usleep(30000); // 30ms
    }
    
    Delete(rect);
    return NULL;
}

// Поток для движущегося круга
void* moving_circle_thread(void* arg) {
    int x = 400, y = 300;
    int dx = -2, dy = 3;
    int color = RGB(0, 255, 0);
    int radius = 30;
    
    int circle = Ellipse(x, y, radius * 2, radius * 2, color);
    Fill(circle, color);
    
    while (running) {
        x += dx;
        y += dy;
        
        // Отскок от границ с изменением размера
        if (x <= radius || x >= 800 - radius) {
            dx = -dx;
            radius = 20 + rand() % 40;
            EnlargeTo(x - radius, y - radius, radius * 2, radius * 2, circle);
        }
        if (y <= radius || y >= 600 - radius) {
            dy = -dy;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(circle, color);
            Fill(circle, color);
        }
        
        MoveTo(x - radius, y - radius, circle);
        usleep(40000); // 40ms
    }
    
    Delete(circle);
    return NULL;
}

// Поток для пульсирующего треугольника
void* pulsating_triangle_thread(void* arg) {
    int center_x = 600, center_y = 150;
    int size = 30;
    int growth = 1;
    int color = RGB(0, 0, 255);
    
    while (running) {
        tPoint triangle[] = {
            {center_x, center_y - size},
            {center_x - size, center_y + size},
            {center_x + size, center_y + size}
        };
        
        int poly = Polygon(triangle, 3, color);
        Fill(poly, color);
        
        // Пульсация размера
        size += growth;
        if (size > 50 || size < 10) {
            growth = -growth;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
        }
        
        usleep(100000); // 100ms
        Delete(poly);
    }
    
    return NULL;
}

// Поток для летающей линии
void* flying_line_thread(void* arg) {
    int x1 = 50, y1 = 400;
    int x2 = 150, y2 = 450;
    int dx1 = 4, dy1 = -3;
    int dx2 = 3, dy2 = -4;
    int color = RGB(255, 255, 0);
    
    int line = Line(x1, y1, x2, y2, color);
    
    while (running) {
        x1 += dx1;
        y1 += dy1;
        x2 += dx2;
        y2 += dy2;
        
        // Отскок от границ
        if (x1 <= 0 || x1 >= 800) dx1 = -dx1;
        if (y1 <= 0 || y1 >= 600) dy1 = -dy1;
        if (x2 <= 0 || x2 >= 800) dx2 = -dx2;
        if (y2 <= 0 || y2 >= 600) dy2 = -dy2;
        
        // Изменение цвета при столкновении с границей
        if (x1 <= 0 || x1 >= 800 || y1 <= 0 || y1 >= 600 ||
            x2 <= 0 || x2 >= 800 || y2 <= 0 || y2 >= 600) {
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(line, color);
        }
        
        // Перерисовываем линию с новыми координатами
        Delete(line);
        line = Line(x1, y1, x2, y2, color);
        
        usleep(50000); // 50ms
    }
    
    Delete(line);
    return NULL;
}

// Поток для прыгающего шара
void* bouncing_ball_thread(void* arg) {
    int x = 300, y = 80;
    int dx = 2, dy = 4;
    int color = RGB(255, 165, 0);  // Оранжевый
    int radius = 25;
    
    int ball = Ellipse(x, y, radius * 2, radius * 2, color);
    Fill(ball, color);
    
    while (running) {
        x += dx;
        y += dy;
        
        // Гравитация
        if (y < 550) {
            dy += 1;  // Ускорение падения
        }
        
        // Отскок от границ
        if (x <= radius || x >= 800 - radius) {
            dx = -dx;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(ball, color);
            Fill(ball, color);
        }
        if (y <= radius) {
            dy = -dy;
        }
        if (y >= 600 - radius) {
            dy = -dy * 0.8;  // Потеря энергии при ударе о землю
            y = 600 - radius;
            color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetColor(ball, color);
            Fill(ball, color);
        }
        
        MoveTo(x - radius, y - radius, ball);
        usleep(30000); // 30ms
    }
    
    Delete(ball);
    return NULL;
}

// Поток для обработки времени (завершение через 30 секунд)
void* timer_thread(void* arg) {
    sleep(30);  // Ждем 30 секунд
    running = 0;
    return NULL;
}

int main() {
    // Устанавливаем обработчик сигналов
    signal(SIGINT, signal_handler);
    
    // Подключаемся к графической системе
    ConnectGraph();
    Clear(0);
    Fill(0, RGB(0, 0, 64));  // Темно-синий фон
    
    // Инициализация случайных чисел
    srand(time(NULL));
    
    // Статический текст
    Text(300, 20, "Parallel Threads Animation", RGB(255, 255, 255));
    Text(320, 40, "Program will exit after 30 seconds", RGB(200, 200, 100));
    Text(320, 60, "Press Ctrl+C to exit immediately", RGB(200, 200, 255));
    
    // Создаем потоки для каждого движущегося элемента
    pthread_create(&threads[0], NULL, moving_rect_thread, NULL);
    pthread_create(&threads[1], NULL, moving_circle_thread, NULL);
    pthread_create(&threads[2], NULL, pulsating_triangle_thread, NULL);
    pthread_create(&threads[3], NULL, flying_line_thread, NULL);
    pthread_create(&threads[4], NULL, bouncing_ball_thread, NULL);
    pthread_create(&threads[5], NULL, timer_thread, NULL);
    
    // Главный поток ждет завершения всех потоков
    for (int i = 0; i < 6; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // Очищаем экран
    Clear(0);
    Text(350, 300, "Animation finished", RGB(255, 255, 255));
    sleep(1);
    
    CloseGraph();
    return 0;
}