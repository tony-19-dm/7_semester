#include <stdio.h>
#include <pthread.h>
#include <sched.h>
#include <sys/neutrino.h>
#include <unistd.h>

volatile int counter1 = 0;
volatile int counter2 = 0;
volatile int running = 1;

void* worker_thread(void* arg) {
    while (running) {
        counter1++;
    }
    return NULL;
}

void* priority_test_thread(void* arg) {
    struct sched_param param;
    int policy;
    
    pthread_getschedparam(pthread_self(), &policy, &param);
    
    while (running) {
        // Устанавливаем тот же приоритет
        pthread_setschedparam(pthread_self(), policy, &param);
        counter2++;
    }
    return NULL;
}

int main() {
    pthread_t worker, tester;
    
    printf("Test of redeployment when setting the same priority\n");
    
    pthread_create(&worker, NULL, worker_thread, NULL);
    pthread_create(&tester, NULL, priority_test_thread, NULL);
    
    sleep(1); // Работаем 1 секунду
    
    running = 0;
    
    pthread_join(worker, NULL);
    pthread_join(tester, NULL);
    
    printf("Working thread: %d iterations\n", counter1);
    printf("Test thread: %d iterations\n", counter2);
    
    if (counter2 > 0) {
        printf("OUTPUT: Rescheduling occurs when the same priority is set\n");
    } else {
        printf("OUTPUT: Rescheduling does NOT occur when the same priority is set\n");
    }
    
    return 0;
}