#include <stdio.h>
#include <pthread.h>
#include <sched.h>
#include <sys/neutrino.h>
#include <unistd.h>

volatile int counter = 0;
volatile int running = 1;

void* worker_thread(void* arg) {
    int priority = *(int*)arg;
    struct sched_param param;
    param.sched_priority = priority;
    
    pthread_setschedparam(pthread_self(), SCHED_RR, &param);
    
    while (running) {
        counter++;
    }
    
    return NULL;
}

void* priority_changer(void* arg) {
    pthread_t target = *(pthread_t*)arg;
    struct sched_param param;
    int policy;
    int i;
    
    pthread_getschedparam(target, &policy, &param);
    
    for (i = 0; i < 1000; i++) {
        // Устанавливаем тот же приоритет
        pthread_setschedparam(target, policy, &param);
    }
    
    return NULL;
}

int main() {
    pthread_t worker, changer;
    int priority = 10;
    
    printf("Запуск теста перепланирования...\n");
    
    pthread_create(&worker, NULL, worker_thread, &priority);
    usleep(100000); // Даем поработать
    
    uint64_t start_count = counter;
    
    pthread_create(&changer, NULL, priority_changer, &worker);
    pthread_join(changer, NULL);
    
    running = 0;
    pthread_join(worker, NULL);
    
    uint64_t end_count = counter;
    
    printf("Счетчик: %llu\n", (unsigned long long)end_count);
    printf("Разница: %llu\n", (unsigned long long)(end_count - start_count));
    
    return 0;
}