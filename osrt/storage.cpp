#include <vingraph.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <cstring>

class BoilerRemote {
public:
    BoilerRemote(int id, const char* host, int port) : id(id), host(host), port(port) {}

    std::string getStatus() {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) return "ERROR";

        sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        inet_pton(AF_INET, host, &addr.sin_addr);

        if (connect(sock, (sockaddr*)&addr, sizeof(addr)) < 0) {
            close(sock);
            return "ERROR";
        }

        char buf[1024];
        sprintf(buf, "STATUS %d", id);
        send(sock, buf, std::strlen(buf), 0);

        int len = recv(sock, buf, 1024, 0);
        buf[len] = '\0';
        close(sock);

        return std::string(buf);
    }

    void refuel(int fuelType) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) return;

        sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        inet_pton(AF_INET, host, &addr.sin_addr);

        if (connect(sock, (sockaddr*)&addr, sizeof(addr)) < 0) {
            close(sock);
            return;
        }

        char buf[1024];
        sprintf(buf, "REFUEL %d %d", id, fuelType);
        send(sock, buf, std::strlen(buf), 0);
        close(sock);
    }

    bool isLowFuelOrEmpty() {
        std::string status = getStatus();
        return (status.compare("LOW") == 0) || (status.compare("EMPTY") == 0);
    }

    bool isEmpty() { 
        return getStatus().compare("EMPTY") == 0; 
    }

    int getX() const { return 200 + id * 150; }
    int getY() const { return 200; }

private:
    int id;
    const char* host;
    int port;
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
        int f = rand() % 10 + 1;
        printf("[Storage] issued fuel type %d\n", f);
        pthread_mutex_unlock(&mtx);
        return f;
    }

    void refreshDisplay() {
        pthread_mutex_lock(&mtx);
        Show(rect);
        Show(fill);
        Show(text);
        pthread_mutex_unlock(&mtx);
    }

    int getX() const { return x; }
    int getY() const { return y; }

private:
    int x, y;
    int rect, fill, text;
    pthread_mutex_t mtx;
};

class Vehicle {
public:
    Vehicle(Storage* s, std::vector<BoilerRemote*>& bs, int startX, int startY, int id)
        : storage(s), boilers(bs), vehicleId(id) {
        pthread_mutex_init(&moveMtx, NULL);
        vehicleRect = Rect(startX, startY, 25, 15, 0, id == 0 ? RGB(50, 100, 200) : RGB(200, 100, 50));
        Show(vehicleRect);
    }
    ~Vehicle() { pthread_mutex_destroy(&moveMtx); }

    static void* runHelper(void* arg) { return ((Vehicle*)arg)->runThread(); }

    void* runThread() {
        int i = vehicleId;
        while (1) {
            int fuel = storage->getFuelType();
            printf("[Vehicle %d] carrying fuel %d to boiler %d\n", vehicleId+1, fuel, i+1);

            if (boilers[i]->isLowFuelOrEmpty()) {
                moveTo(storage->getX(), storage->getY()-50, boilers[i]->getX(), boilers[i]->getY()-50);
                while (!boilers[i]->isEmpty()) { usleep(500000); }
                boilers[i]->refuel(fuel);
                moveTo(boilers[i]->getX(), boilers[i]->getY()-50, storage->getX(), storage->getY()-50);
            }
            i = (i+1) % boilers.size();
            usleep(2000000);
        }
    }

    void refreshDisplay() { Show(vehicleRect); }

private:
    void moveTo(int sx, int sy, int ex, int ey) {
        pthread_mutex_lock(&moveMtx);
        int steps = 30;
        int dx = (ex - sx) / steps;
        int dy = (ey - sy) / steps;
        MoveTo(sx, sy, vehicleRect);
        for (int s=0; s<steps; s++) {
            Move(vehicleRect, dx, dy);
            Fill(vehicleRect, vehicleId==0 ? RGB(50, 100, 200) : RGB(200, 100, 50));
            usleep(40000);
        }
        pthread_mutex_unlock(&moveMtx);
    }

    Storage* storage;
    std::vector<BoilerRemote*>& boilers;
    int vehicleId;
    int vehicleRect;
    pthread_mutex_t moveMtx;
};

int main() {
    ConnectGraph();

    int titleBg = Rect(250, 20, 200, 40, 1, RGB(100, 100, 200));
    int electricPlantText = Text(280, 40, "ELECTRIC PLANT", RGB(255, 255, 255));
    Show(titleBg);
    Show(electricPlantText);

    Storage storage(50, 200);
    BoilerRemote br1(0,"127.0.0.1",8080);
    BoilerRemote br2(1,"127.0.0.1",8080);
    BoilerRemote br3(2,"127.0.0.1",8080);
    BoilerRemote br4(3,"127.0.0.1",8080);

    std::vector<BoilerRemote*> boilers;
    boilers.push_back(&br1);
    boilers.push_back(&br2);
    boilers.push_back(&br3);
    boilers.push_back(&br4);

    Vehicle v1(&storage,boilers,20,20,0);
    Vehicle v2(&storage,boilers,60,20,1);

    int infoText = Text(50, 350, "Press ESC to exit", RGB(150, 150, 150));
    Show(infoText);

    pthread_t t1,t2;
    pthread_create(&t1,NULL,Vehicle::runHelper,&v1);
    pthread_create(&t2,NULL,Vehicle::runHelper,&v2);

    int key;
    while (1) {
        key = InputChar();
        if (key == 27) break;
        storage.refreshDisplay();
        v1.refreshDisplay();
        v2.refreshDisplay();
        usleep(10000);
    }

    pthread_join(t1,NULL);
    pthread_join(t2,NULL);
    CloseGraph();
    return 0;
}