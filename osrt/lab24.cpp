#include <vingraph.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

// Глобальные переменные для управления потоками
typedef struct {
    double a;
    double b;
    int running;
} shared_data_t;

shared_data_t shared;
pthread_t anim_thread, key_thread;

// Обработчик сигнала для корректного завершения
void signal_handler(int sig) {
    shared.running = 0;
}

// Функция для потока анимации
void* animation_thread(void* arg) {
    double phi = 0.0;
    
    // Создаем объект для движения (желтый круг)
    int obj = Ellipse(0, 0, 30, 30, RGB(255, 255, 0));
    Fill(obj, RGB(255, 255, 0));
    
    while (shared.running) {
        // Вычисляем координаты по Улитке Паскаля
        double rho = shared.a * cos(phi) + shared.b;
        double x = rho * cos(phi) + 400;  // Центр экрана
        double y = rho * sin(phi) + 300;
        
        // Перемещаем объект
        MoveTo((int)x - 15, (int)y - 15, obj);
        
        // Увеличиваем угол
        phi += 0.02;
        if (phi > 2 * M_PI) phi -= 2 * M_PI;
        
        usleep(30000); // 30ms
    }
    
    Delete(obj);
    return NULL;
}

// Функция для потока обработки клавиш
void* keyboard_thread(void* arg) {
    time_t start_time = time(NULL);
    
    while (shared.running && (time(NULL) - start_time < 30)) {
        // В QNX нет простого способа обработки клавиш, используем задержку
        usleep(100000); // 100ms
    }
    
    shared.running = 0;
    return NULL;
}

// Функция для отображения информации
void* info_thread(void* arg) {
    char info[100];
    
    while (shared.running) {
        // Обновляем отображение параметров
        sprintf(info, "a = %.1f, b = %.1f", shared.a, shared.b);
        
        // Очищаем область и рисуем новый текст
        SetColor(0, RGB(0, 0, 64));
        Fill(Rect(350, 100, 200, 20, 0), RGB(0, 0, 64));
        Text(350, 100, info, RGB(255, 255, 0));
        
        // Показываем время
        time_t current_time = time(NULL);
        sprintf(info, "Time: %ld sec", current_time - *(time_t*)arg);
        SetColor(0, RGB(0, 0, 64));
        Fill(Rect(350, 120, 200, 20, 0), RGB(0, 0, 64));
        Text(350, 120, info, RGB(200, 200, 200));
        
        usleep(100000); // 100ms
    }
    return NULL;
}

int main() {
    // Инициализируем разделяемые данные
    shared.a = 50.0;
    shared.b = 30.0;
    shared.running = 1;
    
    // Устанавливаем обработчик сигналов
    signal(SIGINT, signal_handler);
    
    // Подключаемся к графической системе
    ConnectGraph();
    Clear(0);
    Fill(0, RGB(0, 0, 64));  // Темно-синий фон
    
    // Статический текст с инструкциями
    Text(250, 20, "Curve Animation with Threads", RGB(255, 255, 255));
    Text(280, 40, "Using pthreads in single process", RGB(200, 200, 100));
    Text(300, 60, "Program will exit after 30 seconds", RGB(200, 200, 255));
    Text(320, 80, "Press Ctrl+C to exit immediately", RGB(200, 200, 255));
    
    // Записываем время начала
    time_t start_time = time(NULL);
    pthread_t info_thr;
    
    // Создаем потоки
    pthread_create(&anim_thread, NULL, animation_thread, NULL);
    pthread_create(&key_thread, NULL, keyboard_thread, NULL);
    pthread_create(&info_thr, NULL, info_thread, &start_time);
    
    // Ждем завершения всех потоков
    pthread_join(anim_thread, NULL);
    pthread_join(key_thread, NULL);
    pthread_join(info_thr, NULL);
    
    // Очищаем экран
    Clear(0);
    Text(350, 300, "Animation finished", RGB(255, 255, 255));
    sleep(1);
    
    CloseGraph();
    return 0;
}