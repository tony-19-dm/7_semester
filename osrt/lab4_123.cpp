#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <signal.h>
#include <pthread.h>
#include "plates.h"

// Определение пользовательских сигналов для межпоточного взаимодействия
#define SIG_LOCATOR SIGUSR1    // Сигнал от локатора при обнаружении тарелки
#define SIG_TIMER (SIGUSR1 + 1) // Сигнал от таймера для периодического опроса

// Класс для отслеживания состояния тарелок между потоками
class PlateTracker {
public:
    static int t1, t2;     // Время обнаружения первой и второй тарелок (мс)
    static int loc1, loc2; // Номера линий обнаруженных тарелок (1-4)
    static int v;          // Вычисленная скорость тарелки (единиц/секунду)
};

// Инициализация статических переменных класса PlateTracker
int PlateTracker::t1 = 0;
int PlateTracker::t2 = 0;
int PlateTracker::loc1 = 0;
int PlateTracker::loc2 = 0;
int PlateTracker::v = 0;

// Функция потока для отслеживания скорости тарелок
void* handle_plate(void* arg) {
    (void)arg; // Неиспользуемый параметр
    
    struct sigevent event;
    struct itimerspec timer_spec;
    timer_t timer_id;
    sigset_t set;

    // Настройка таймера для генерации сигнала SIG_TIMER
    SIGEV_SIGNAL_INIT(&event, SIG_TIMER);
    if (timer_create(CLOCK_MONOTONIC, &event, &timer_id) == -1) {
        perror("handle_plate: timer_create");
        return NULL;
    }

    // Настройка маски сигналов для ожидания SIG_TIMER
    sigemptyset(&set);
    sigaddset(&set, SIG_TIMER);

    // Установка таймера на срабатывание каждые 10 мс (10000000 наносекунд)
    timer_spec.it_value.tv_sec = 0;
    timer_spec.it_value.tv_nsec = 10000000;
    timer_spec.it_interval = timer_spec.it_value; // Периодическое срабатывание
    
    if (timer_settime(timer_id, 0, &timer_spec, NULL) == -1) {
        perror("handle_plate: timer_settime");
        timer_delete(timer_id);
        return NULL;
    }

    // Основной цикл потока отслеживания тарелок
    while (1) {
        siginfo_t si;
        sigwaitinfo(&set, &si); // Ожидание сигнала таймера
        
        // Чтение данных с локатора
        int locNum = getreg(RG_LOCN); // Номер линии (1-4)
        if (locNum < 0) continue;     // Если ошибка - пропуск итерации
        
        int y = getreg(RG_LOCY); // Координата Y тарелки
        int w = getreg(RG_LOCW); // Тип/ширина тарелки (1=нет, 2=медленная, 3=быстрая)
        
        if (w != 1) { // Если обнаружена реальная тарелка (не шум)
            if (PlateTracker::loc1 == 0) {
                // Первое обнаружение тарелки - запоминаем позицию и время
                PlateTracker::loc1 = locNum;
                struct timespec ts;
                clock_gettime(CLOCK_MONOTONIC, &ts);
                PlateTracker::t1 = (int)(ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
            } else if (PlateTracker::loc2 == 0 && locNum != PlateTracker::loc1) {
                // Второе обнаружение другой тарелки - вычисляем скорость
                PlateTracker::loc2 = locNum;
                struct timespec ts;
                clock_gettime(CLOCK_MONOTONIC, &ts);
                PlateTracker::t2 = (int)(ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
                
                // Преобразование номеров линий в координаты X
                int x1 = (PlateTracker::loc1 == 1) ? XL1 :
                         (PlateTracker::loc1 == 2) ? XL2 :
                         (PlateTracker::loc1 == 3) ? XL3 : XL4;
                int x2 = (PlateTracker::loc2 == 1) ? XL1 :
                         (PlateTracker::loc2 == 2) ? XL2 :
                         (PlateTracker::loc2 == 3) ? XL3 : XL4;
                
                // Вычисление скорости: расстояние / время × 1000 (для перевода в мс)
                if (PlateTracker::t2 != PlateTracker::t1) {
                    PlateTracker::v = abs(x2 - x1) * 1000 / (PlateTracker::t2 - PlateTracker::t1);
                } else {
                    PlateTracker::v = 0; // Защита от деления на ноль
                }
            }
        }
    }

    timer_delete(timer_id);
    return NULL;
}

// Обработчик прерываний от локатора - генерирует сигнал SIG_LOCATOR
const struct sigevent *intrHandler(void *area, int id) {
    static struct sigevent event;
    SIGEV_SIGNAL_INIT(&event, SIG_LOCATOR);
    return &event;
}

int main() {
    sigset_t blockset;
    
    // Блокировка сигналов в главном потоке перед созданием дочерних потоков
    sigemptyset(&blockset);
    sigaddset(&blockset, SIG_LOCATOR);
    sigaddset(&blockset, SIG_TIMER);
    if (pthread_sigmask(SIG_BLOCK, &blockset, NULL) != 0) {
        perror("main: pthread_sigmask");
    }

    // Запуск игры на уровне 3 (с быстрыми и медленными тарелками)
    StartGame(3);

    // Подключение обработчика прерываний от локатора
    int id = InterruptAttach(LOC_INTR, intrHandler, NULL, 0, 0);
    if (id < 0) {
        perror("main: InterruptAttach");
        EndGame();
        return 1;
    }

    // Создание потока для отслеживания скорости тарелок
    pthread_t plate_thread;
    if (pthread_create(&plate_thread, NULL, handle_plate, (void*)0) != 0) {
        perror("main: pthread_create");
        InterruptDetach(id);
        EndGame();
        return 1;
    }

    // Настройка маски сигналов для ожидания в основном цикле
    sigset_t waitset;
    sigemptyset(&waitset);
    sigaddset(&waitset, SIG_LOCATOR);

    // Основной цикл обработки обнаруженных тарелок
    while (1) {
        int sig;
        sigwait(&waitset, &sig); // Ожидание сигнала от локатора
        
        if (sig != SIG_LOCATOR) continue; // Проверка что это наш сигнал
        
        // Чтение данных о обнаруженной тарелке
        int locNum = getreg(RG_LOCN);
        if (locNum < 0) continue;
        
        int y = getreg(RG_LOCY);
        int w = getreg(RG_LOCW);
        
        if (w != 1) { // Если это реальная тарелка
            // Получение текущей позиции пушки
            int gunX = getreg(RG_GUNX);
            int targetX;
            
            // Определение целевой координаты X по номеру линии
            switch (locNum) {
                case 1: targetX = XL1; break; // Линия 1 → координата XL1
                case 2: targetX = XL2; break; // Линия 2 → координата XL2
                case 3: targetX = XL3; break; // Линия 3 → координата XL3
                case 4: targetX = XL4; break; // Линия 4 → координата XL4
                default: continue; // Неизвестная линия - пропуск
            }
            
            // Расчет направления и расстояния для поворота пушки
            int dir = (targetX > gunX) ? GUNM_RIGHT : GUNM_LEFT;
            int steps = abs(targetX - gunX);
            
            // Поворот пушки в направлении цели
            putreg(RG_GUNM, dir);
            
            // Расчет времени поворота: расстояние × задержка_на_шаг
            struct timespec ts;
            ts.tv_sec = 0;
            long ns = (long)steps * (long)GunDelay * 1000000L;
            
            // Преобразование наносекунд в структуру timespec
            if (ns > 999999999L) {
                ts.tv_sec = ns / 1000000000L;
                ts.tv_nsec = ns % 1000000000L;
            } else {
                ts.tv_nsec = ns;
            }
            
            // Ожидание завершения поворота пушки
            nanosleep(&ts, NULL);
            putreg(RG_GUNM, GUNM_STOP); // Остановка пушки
            
            // ВЫБОР ТИПА ОРУЖИЯ НА ОСНОВЕ СКОРОСТИ ТАРЕЛКИ:
            if (w == 3 && PlateTracker::v >= 100) {
                // БЫСТРАЯ ТАРЕЛКА (тип 3 со скоростью ≥100) - используем управляемый снаряд
                int rcmNum = 0;
                putreg(RG_RCMN, rcmNum); // Выбор снаряда
                
                // Формирование команды для управляемого снаряда
                union {
                    signed char c[4];
                    int i;
                } cmd;
                cmd.c[0] = (targetX > gunX) ? 1 : -1; // Направление к цели
                cmd.c[1] = 0;  // Нет движения по Y
                cmd.c[2] = 0;  // Резерв
                cmd.c[3] = 1;  // Флаг выполнения команды
                putreg(RG_RCMC, cmd.i); // Запуск снаряда
            } else {
                // МЕДЛЕННАЯ ТАРЕЛКА - обычный выстрел из пушки
                putreg(RG_GUNS, GUNS_SHOOT);
            }
            
            // СБРОС СОСТОЯНИЯ ТРЕКЕРА для следующей тарелки
            PlateTracker::loc1 = 0;
            PlateTracker::loc2 = 0;
            PlateTracker::v = 0;
        }
    }

    // Очистка ресурсов (этот код никогда не выполнится из-за бесконечного цикла)
    InterruptDetach(id);
    EndGame();
    return 0;
}