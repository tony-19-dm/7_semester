#include <iostream>
#include <cstdlib>
#include <unistd.h>
#include <pthread.h>
#include <sys/neutrino.h>
#include <sys/wait.h>

const int NUM_ITERATIONS = 100000;

void* thread_function(void* arg) {
    return NULL;
}

int main() {
    unsigned long long start, end;
    double total_fork = 0, total_thread = 0;

    // Измерение времени fork()
    for (int i = 0; i < NUM_ITERATIONS; ++i) {
        start = ClockCycles();
        pid_t pid = fork();
        if (pid == 0) {
            _exit(0); // Дочерний процесс сразу завершается
        } else if (pid > 0) {
            waitpid(pid, NULL, 0); // Ждем завершения дочернего процесса
            end = ClockCycles();
            total_fork += (end - start);
        } else {
            std::cerr << "Error fork()" << std::endl;
            return 1;
        }
    }

    // Измерение времени создания нити
    for (int i = 0; i < NUM_ITERATIONS; ++i) {
        pthread_t tid;
        start = ClockCycles();
        int ret = pthread_create(&tid, NULL, thread_function, NULL);
        if (ret == 0) {
            pthread_join(tid, NULL); // Ожидаем завершения нити
            end = ClockCycles();
            total_thread += (end - start);
        } else {
            std::cerr << "Error pthread_create()" << std::endl;
            return 1;
        }
    }

    std::cout << "Avg time fork(): " << total_fork / NUM_ITERATIONS << " циклов" << std::endl;
    std::cout << "Avg time pthread_create(): " << total_thread / NUM_ITERATIONS << " циклов" << std::endl;

    return 0;
}