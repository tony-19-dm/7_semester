#include <iostream>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>
#include <sys/neutrino.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_counter = 0;

void* high_priority_thread(void* arg) {
    pthread_mutex_lock(&mutex);
    std::cout << "A high priority thread has started working" << std::endl;

    // Понижаем приоритет
    struct sched_param param;
    int policy;
    pthread_getschedparam(pthread_self(), &policy, &param);
    std::cout << "Current priority: " << param.sched_priority << std::endl;
    param.sched_priority = 10; // низкий приоритет
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);

    // После понижения приоритета
    std::cout << "Priority is lowered to 10. Counter: " << shared_counter << std::endl;

    pthread_mutex_unlock(&mutex);
    return NULL;
}

void* low_priority_thread(void* arg) {
    // Эта нить будет ждать, пока мьютекс освободится
    pthread_mutex_lock(&mutex);
    std::cout << "A low-priority thread increases the counter" << std::endl;
    shared_counter++;
    pthread_mutex_unlock(&mutex);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    struct sched_param param;

    // Устанавливаем планировщик главной нити на SCHED_FIFO
    param.sched_priority = 20; // высокий приоритет
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);

    // Создаем высокоприоритетную нить
    pthread_attr_t attr_high;
    pthread_attr_init(&attr_high);
    pthread_attr_setinheritsched(&attr_high, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr_high, SCHED_FIFO);
    param.sched_priority = 20;
    pthread_attr_setschedparam(&attr_high, &param);

    pthread_create(&t1, &attr_high, high_priority_thread, NULL);

    // Небольшая задержка, чтобы гарантировать, что высокоприоритетная нить запустится первой
    usleep(1000);

    // Создаем низкоприоритетную нить
    pthread_attr_t attr_low;
    pthread_attr_init(&attr_low);
    pthread_attr_setinheritsched(&attr_low, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr_low, SCHED_FIFO);
    param.sched_priority = 10;
    pthread_attr_setschedparam(&attr_low, &param);

    pthread_create(&t2, &attr_low, low_priority_thread, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_attr_destroy(&attr_high);
    pthread_attr_destroy(&attr_low);

    return 0;
}