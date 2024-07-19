from multiprocessing import Process, Manager, freeze_support

class WarehouseManager:
    def __init__(self):
        Process.__init__(self) # Я процесс
        # Используем менеджер для создания словаря, который может быть разделен между процессами
        self.manager = Manager()
        self.data = self.manager.dict()

    def process_request(self, request):
        product, action, quantity = request
        if action == 'receipt':
            if product in self.data:
                self.data[product] += quantity
            else:
                self.data[product] = quantity
        elif action == 'shipment':
            if product in self.data and self.data[product] > 0:
                self.data[product] -= quantity
                if self.data[product] < 0:
                    self.data[product] = 0

    def run(self, requests):
        processes = []

        for request in requests:
            process = Process(target=self.process_request, args=(request,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

if __name__ == '__main__':
    freeze_support()  # Необходим в Windows для корректной работы

    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(dict(manager.data))