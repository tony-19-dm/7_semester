#include <stdio.h>
#include <pthread.h>
#include <sys/neutrino.h>
#include <unistd.h>
#include <stdint.h>

#define ITERATIONS 100000

volatile int flag;
uint64_t total_cycles = 0;

void* thread_func(void* arg) {
    int i;
    for (i = 0; i < ITERATIONS; i++) {
        while (flag == 0) {
            // Ждем, пока главная нить установит флаг
        }
        flag = 0;
    }
    return NULL;
}

int main() {
    pthread_t thread;
    uint64_t start, end;
    int i;
    
    pthread_create(&thread, NULL, thread_func, NULL);
    
    for (i = 0; i < ITERATIONS; i++) {
        flag = 0;
        
        start = ClockCycles();
        flag = 1;
        while (flag == 1) {
            // Ждем, пока вторая нить сбросит флаг
        }
        end = ClockCycles();
        
        total_cycles += (end - start);
    }
    
    pthread_join(thread, NULL);
    
    double avg_cycles = (double)total_cycles / ITERATIONS;
    printf("Среднее время контекстного переключения: %.2f циклов\n", avg_cycles);
    printf("За %d итераций\n", ITERATIONS);
    
    return 0;
}