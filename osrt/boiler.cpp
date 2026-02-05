#include <vingraph.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <string>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <cstring>

class BoilerLocal {
public:
    BoilerLocal(int id) : id(id), fuel(100) {
        pthread_mutex_init(&mtx, NULL);
        rect = Rect(200 + id * 150, 200, 100, 80, 1, RGB(200, 150, 0));
        statusRect = Rect(202 + id * 150, 202, 96, 76, 0, RGB(255, 255, 100));
        
        char title[20];
        sprintf(title, "BOILER %d", id + 1);
        text = Text(225 + id * 150, 230, title, RGB(0, 0, 0));
        
        Show(rect);
        Show(statusRect);
        Show(text);
    }

    std::string getStatus() {
        pthread_mutex_lock(&mtx);
        std::string status;
        if (fuel == 0) status = "EMPTY";
        else if (fuel < 30) status = "LOW";
        else status = "OK";
        pthread_mutex_unlock(&mtx);
        return status;
    }

    void consume() {
        pthread_mutex_lock(&mtx);
        if (fuel > 0) fuel--;
        updateDisplay();
        pthread_mutex_unlock(&mtx);
    }

    void refuel(int fuelType) {
        pthread_mutex_lock(&mtx);
        fuel = 100;
        updateDisplay();
        printf("[Boiler %d] Refueled with type %d\n", id + 1, fuelType);
        pthread_mutex_unlock(&mtx);
    }

    int getFuel() const { return fuel; }
    int getId() const { return id; }

private:
    void updateDisplay() {
        int fuelLevel = (fuel * 70) / 100;
        int fuelColor;
        
        if (fuel < 30) fuelColor = RGB(255, 50, 50);
        else if (fuel < 60) fuelColor = RGB(255, 200, 50);
        else fuelColor = RGB(50, 200, 50);
        
        Fill(statusRect, fuelColor);
        
        char fuelText[20];
        sprintf(fuelText, "%d%%", fuel);
        int fuelTextObj = Text(225 + id * 150, 250, fuelText, RGB(0, 0, 0));
        Show(fuelTextObj);
        usleep(50000);
        Delete(fuelTextObj);
    }

    int id;
    int fuel;
    int rect;
    int statusRect;
    int text;
    pthread_mutex_t mtx;
};

void* serverThread(void* arg) {
    std::vector<BoilerLocal*>* boilers =
        static_cast<std::vector<BoilerLocal*>*>(arg);

    int serverSock = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSock < 0) {
        perror("socket");
        return NULL;
    }

    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(serverSock, (sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(serverSock);
        return NULL;
    }

    listen(serverSock, 5);

    while (1) {
        int clientSock = accept(serverSock, NULL, NULL);
        if (clientSock < 0) continue;

        char buf[1024];
        int len = recv(clientSock, buf, sizeof(buf) - 1, 0);
        if (len > 0) {
            buf[len] = '\0';
            int id, fuelType;

            if (sscanf(buf, "STATUS %d", &id) == 1) {
                if (id >= 0 && id < (int)boilers->size()) {
                    std::string status = (*boilers)[id]->getStatus();
                    send(clientSock, status.c_str(),
                         status.size(), 0);
                }
            } else if (sscanf(buf, "REFUEL %d %d", &id, &fuelType) == 2) {
                if (id >= 0 && id < (int)boilers->size()) {
                    (*boilers)[id]->refuel(fuelType);
                    const char* ok = "OK";
                    send(clientSock, ok, std::strlen(ok), 0);
                }
            }
        }
        close(clientSock);
    }

    close(serverSock);
    return NULL;
}

void* consumeThread(void* arg) {
    std::vector<BoilerLocal*>* boilers =
        static_cast<std::vector<BoilerLocal*>*>(arg);

    while (1) {
        size_t i;
        for (i = 0; i < boilers->size(); ++i) {
            (*boilers)[i]->consume();
        }
        usleep(500000);
    }
    return NULL;
}

int main() {
    ConnectGraph();

    int titleBg = Rect(250, 20, 200, 40, 1, RGB(100, 100, 200));
    int serverText = Text(280, 40, "BOILER SERVER", RGB(255, 255, 255));
    Show(titleBg);
    Show(serverText);

    BoilerLocal b1(0);
    BoilerLocal b2(1);
    BoilerLocal b3(2);
    BoilerLocal b4(3);

    std::vector<BoilerLocal*> boilers;
    boilers.push_back(&b1);
    boilers.push_back(&b2);
    boilers.push_back(&b3);
    boilers.push_back(&b4);

    int infoText = Text(50, 350, "Press ESC to exit", RGB(150, 150, 150));
    Show(infoText);

    pthread_t srvThread, consThread;
    pthread_create(&srvThread, NULL, serverThread, &boilers);
    pthread_create(&consThread, NULL, consumeThread, &boilers);

    int key = 0;
    while (1) {
        key = InputChar();
        if (key == 27) break;
        usleep(10000);
    }

    pthread_cancel(srvThread);
    pthread_cancel(consThread);

    pthread_join(srvThread, NULL);
    pthread_join(consThread, NULL);

    CloseGraph();
    return 0;
}