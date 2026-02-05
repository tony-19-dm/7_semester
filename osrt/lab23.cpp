#include <vingraph.h>
#include <unistd.h>
#include <process.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <math.h>
#include <time.h>

// Структура для разделяемой памяти
typedef struct {
    double a;
    double b;
    int running;
} shared_data_t;

shared_data_t *shared;

// Обработчик сигнала для корректного завершения
void signal_handler(int sig) {
    shared->running = 0;
}

int main() {
    // Создаем разделяемую память
    shared = (shared_data_t*)mmap(NULL, sizeof(shared_data_t), 
                                PROT_READ | PROT_WRITE, 
                                MAP_SHARED | MAP_ANON, -1, 0);
    
    if (shared == MAP_FAILED) {
        printf("mmap failed\n");
        exit(1);
    }
    
    // Инициализируем разделяемую память
    shared->a = 50.0;
    shared->b = 30.0;
    shared->running = 1;
    
    // Устанавливаем обработчик сигналов
    signal(SIGINT, signal_handler);
    
    // Подключаемся к графической системе
    ConnectGraph();
    Clear(0);
    Fill(0, RGB(0, 0, 64));  // Темно-синий фон
    
    // Статический текст с инструкциями
    Text(250, 20, "Curve Animation with Shared Memory", RGB(255, 255, 255));
    Text(280, 40, "Program demonstrates shared memory concept", RGB(200, 200, 100));
    Text(300, 60, "Watch the yellow circle move", RGB(200, 200, 255));
    
    // Создаем объект для движения (желтый круг)
    int obj = Ellipse(0, 0, 30, 30, RGB(255, 255, 0));
    Fill(obj, RGB(255, 255, 0));
    
    double phi = 0.0;
    time_t start_time = time(NULL);
    char info[100];
    
    // Главный цикл анимации
    while (shared->running && (time(NULL) - start_time < 30)) {
        // Вычисляем координаты по Улитке Паскаля
        double rho = shared->a * cos(phi) + shared->b;
        double x = rho * cos(phi) + 400;  // Центр экрана
        double y = rho * sin(phi) + 300;
        
        // Перемещаем объект
        MoveTo((int)x - 15, (int)y - 15, obj);
        
        // Увеличиваем угол
        phi += 0.02;
        if (phi > 2 * M_PI) phi -= 2 * M_PI;
        
        // Обновляем отображение параметров
        sprintf(info, "a = %.1f, b = %.1f", shared->a, shared->b);
        
        // Очищаем область и рисуем новый текст
        SetColor(0, RGB(0, 0, 64));
        Fill(Rect(350, 100, 200, 20, 0), RGB(0, 0, 64));
        Text(350, 100, info, RGB(255, 255, 0));
        
        
        delay(30);
    }
    
    // Завершаем программу
    shared->running = 0;
    
    // Очищаем экран
    Delete(obj);
    Clear(0);
    Text(350, 300, "Animation finished", RGB(255, 255, 255));
    delay(1000);
    
    // Освобождаем разделяемую память
    munmap(shared, sizeof(shared_data_t));
    
    CloseGraph();
    return 0;
}