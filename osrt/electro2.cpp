#include <vingraph.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <cmath>

class Boiler;

struct BurnData {
    Boiler* boiler;
    std::vector<int> fuelBlocks;
    BurnData(Boiler* b, const std::vector<int>& fb) : boiler(b), fuelBlocks(fb) {}
};

class Storage {
public:
    Storage(int x, int y) : x(x), y(y) {
        pthread_mutex_init(&mtx, NULL);
        rect = Rect(x, y, 100, 80, 1, RGB(0, 100, 200));
        fill = Rect(x+2, y+2, 96, 76, 0, RGB(0, 200, 100));
        text = Text(x + 15, y + 35, "FUEL", RGB(255, 255, 255));
        Show(rect);
        Show(fill);
        Show(text);
    }
    int getFuelType() {
        pthread_mutex_lock(&mtx);
        int fuelType = rand() % 10 + 1;
        printf("[Storage] issued fuel type %d\n", fuelType);
        pthread_mutex_unlock(&mtx);
        return fuelType;
    }
    int getX() const { return x; }
    int getY() const { return y; }
private:
    int x, y;
    int rect, fill, text;
    pthread_mutex_t mtx;
};

class Boiler {
public:
    Boiler(int id, int x, int y, int capacity) : id(id), x(x), y(y), capacity(capacity), currentFuel(0), burnThread(0) {
        pthread_mutex_init(&burnMtx, NULL);
        rect = Rect(x, y, 100, 80, 1, RGB(200, 150, 0));
        statusRect = Rect(x+2, y+2, 96, 76, 0, RGB(255, 255, 100));
        
        char title[20];
        sprintf(title, "BOILER %d", id);
        text1 = Text(x + 25, y + 20, title, RGB(0, 0, 0));
        text2 = Text(x + 25, y + 50, "WAITING", RGB(255, 0, 0));
        
        Show(rect);
        Show(statusRect);
        Show(text1);
        Show(text2);
    }

    ~Boiler() {
        if (burnThread) {
            pthread_join(burnThread, NULL);
        }
        pthread_mutex_destroy(&burnMtx);
    }

    void fillAndBurn(int fuelType) {
        pthread_mutex_lock(&burnMtx);
        if (currentFuel == 0) {
            currentFuel = capacity;
            currentFuelType = fuelType;

            Delete(text2);
            text2 = Text(x + 25, y + 50, "BURNING", RGB(255, 100, 0));
            Show(text2);

            std::vector<int> fuelBlocks;
            for (int i = 0; i < capacity; i++) {
                int block = Rect(x + 80, y + 10 + (i * 8), 15, 6, 0, RGB(200, 50, 50));
                Show(block);
                fuelBlocks.push_back(block);
                usleep(200000);
            }

            usleep(500000);

            BurnData* data = new BurnData(this, fuelBlocks);
            pthread_create(&burnThread, NULL, burnHelper, data);
            Delete(text2);
            text2 = Text(x + 25, y + 50, "WORKING", RGB(0, 150, 0));
            Show(text2);
        } else {
            Delete(text2);
            text2 = Text(x + 25, y + 50, "WORKING", RGB(0, 150, 0));
            Show(text2);
        }
        pthread_mutex_unlock(&burnMtx);
    }

    static void* burnHelper(void* arg) {
        BurnData* data = static_cast<BurnData*>(arg);
        data->boiler->burnInternally(data->fuelBlocks);
        delete data;
        return NULL;
    }

    void burnInternally(const std::vector<int>& fuelBlocks) {
        pthread_mutex_lock(&burnMtx);
        for (int i = fuelBlocks.size() - 1; i >= 0; i--) {
            Delete(fuelBlocks[i]);
            usleep(currentFuelType * 100000);
        }
        Delete(text2);
        text2 = Text(x + 25, y + 50, "WAITING", RGB(255, 0, 0));
        Show(text2);
        currentFuel = 0;
        burnThread = 0;
        pthread_mutex_unlock(&burnMtx);
    }

    bool isEmpty() const {
        return currentFuel == 0;
    }

    int getX() const { return x; }
    int getY() const { return y; }

private:
    int id;
    int x, y;
    int rect, statusRect;
    int text1;
    int text2;
    int capacity;
    int currentFuel;
    int currentFuelType;
    pthread_t burnThread;
    pthread_mutex_t burnMtx;
};

class Vehicle {
public:
    Vehicle(Storage* storage, std::vector<Boiler*>& boilers, int x, int y, int plantRect, int vehicleId)
        : storage(storage), boilers(boilers), x(x), y(y), plantRect(plantRect), vehicleId(vehicleId) {
        pthread_mutex_init(&moveMtx, NULL);
    }
    ~Vehicle() {
        pthread_mutex_destroy(&moveMtx);
    }
    
    static void* runHelper(void* arg) { return ((Vehicle*)arg)->runThread(); }
    
    void* runThread() {
        int i = vehicleId;
        while (1) {
            int fuelType = storage->getFuelType();
            printf("[Vehicle %d] carrying fuel type %d to the boiler %d\n", vehicleId + 1, fuelType, i + 1);
            if (boilers[i]->isEmpty()) {
                moveToBoiler(storage->getX(), storage->getY() - 50, boilers[i]->getX() + 20, boilers[i]->getY() - 50);
                boilers[i]->fillAndBurn(fuelType);
                moveToStorage(boilers[i]->getX(), boilers[i]->getY() - 50, storage->getX() + 20, storage->getY() - 50);
                usleep(1000000);
            } else {
                printf("[Vehicle %d] Boiler %d is not empty, skipping\n", vehicleId + 1, i + 1);
            }
            i = (i + 2) % boilers.size();
            usleep(10000);
        }
        return NULL;
    }

private:
    void moveToBoiler(int startX, int startY, int endX, int endY) {
        pthread_mutex_lock(&moveMtx);
        int steps = 30;
        int dx = (endX - startX) / steps;
        int dy = (endY - startY) / steps;
        MoveTo(startX, startY, plantRect);
        for (int step = 1; step <= steps; step++) {
            Move(plantRect, dx, dy);
            Fill(plantRect, vehicleId == 0 ? RGB(50, 100, 200) : RGB(200, 100, 50));
            usleep(15000);
        }
        pthread_mutex_unlock(&moveMtx);
    }

    void moveToStorage(int startX, int startY, int endX, int endY) {
        pthread_mutex_lock(&moveMtx);
        int steps = 30;
        int dx = (endX - startX) / steps;
        int dy = (endY - startY) / steps;
        MoveTo(startX, startY, plantRect);
        for (int step = 1; step <= steps; step++) {
            Move(plantRect, dx, dy);
            Fill(plantRect, vehicleId == 0 ? RGB(150, 50, 200) : RGB(200, 50, 150));
            usleep(15000);
        }
        pthread_mutex_unlock(&moveMtx);
    }

    Storage* storage;
    std::vector<Boiler*>& boilers;
    int x, y;
    int plantRect;
    int vehicleId;
    pthread_mutex_t moveMtx;
};

int main() {
    ConnectGraph();

    int titleBg = Rect(250, 20, 200, 40, 1, RGB(100, 100, 200));
    int electricPlantText = Text(280, 40, "ELECTRIC PLANT", RGB(255, 255, 255));
    Show(titleBg);
    Show(electricPlantText);

    Storage storage(50, 200);
    Boiler b1(1, 200, 200, 8);
    Boiler b2(2, 350, 200, 8);
    Boiler b3(3, 500, 200, 8);
    Boiler b4(4, 650, 200, 8);

    std::vector<Boiler*> boilers;
    boilers.push_back(&b1);
    boilers.push_back(&b2);
    boilers.push_back(&b3);
    boilers.push_back(&b4);

    int vehicleRect1 = Rect(20, 20, 25, 15, 0, RGB(50, 100, 200));
    int vehicleRect2 = Rect(60, 20, 25, 15, 0, RGB(200, 100, 50));
    Show(vehicleRect1);
    Show(vehicleRect2);

    Vehicle vehicle1(&storage, boilers, 20, 20, vehicleRect1, 0);
    Vehicle vehicle2(&storage, boilers, 20, 20, vehicleRect2, 1);
    pthread_t vehicleThread1, vehicleThread2;
    pthread_create(&vehicleThread1, NULL, Vehicle::runHelper, &vehicle1);
    pthread_create(&vehicleThread2, NULL, Vehicle::runHelper, &vehicle2);

    int infoText = Text(50, 350, "Press ESC to exit", RGB(150, 150, 150));
    Show(infoText);

    int key = 0;
    bool running = true;
    while (running) {
        key = InputChar();
        if (key == 27) {
            CloseGraph();
            return 0;
        }
    }

    pthread_join(vehicleThread1, NULL);
    pthread_join(vehicleThread2, NULL);

    CloseGraph();
    return 0;
}