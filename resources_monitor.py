import psutil
import time
from tabulate import tabulate

class ResourceMonitor:
    def __init__(self):
        self.interval = 1  # Intervalo de actualización en segundos

    def get_cpu_count(self):
        logical_cpus = psutil.cpu_count()
        physical_cpus = psutil.cpu_count(logical=False)
        return logical_cpus, physical_cpus

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent, memory.total

    def get_disk_io(self):
        disk_io = psutil.disk_io_counters()
        return disk_io.read_bytes, disk_io.write_bytes

    def get_network_io(self):
        network_io = psutil.net_io_counters()
        return network_io.bytes_sent, network_io.bytes_recv

    def get_top_processes(self, n=5):
        processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent'], p.info['memory_percent'])
                     for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])]
        processes.sort(key=lambda x: x[2], reverse=True)
        return processes[:n]

    def print_metrics(self):
        logical_cpus, physical_cpus = self.get_cpu_count()
        while True:
            cpu_usage = self.get_cpu_usage()
            memory_usage, total_memory = self.get_memory_usage()
            disk_read, disk_write = self.get_disk_io()
            net_sent, net_recv = self.get_network_io()
            top_processes = self.get_top_processes()

            print("\n--- Uso de Recursos ---")
            print(f"CPU (Lógicos)  -> Número lógico de CPUs disponibles en el sistema: {logical_cpus}")
            print(f"CPU (Físico) -> número físico de CPUs disponibles: {physical_cpus}")
            print(f"Uso de CPU: {cpu_usage}%")
            print(f"Uso de Memoria: {memory_usage}% de {total_memory / (1024**3):.2f} GB")
            print(f"Lectura de Disco: {disk_read / (1024**2):.2f} MB")
            print(f"Escritura de Disco: {disk_write / (1024**2):.2f} MB")
            print(f"Red Enviada: {net_sent / (1024**2):.2f} MB")
            print(f"Red Recibida: {net_recv / (1024**2):.2f} MB")
            print("\n--- Procesos Principales ---")
            print(tabulate(top_processes, headers=["PID", "Nombre", "CPU %", "Memoria %"], tablefmt="pretty"))

            time.sleep(self.interval)

if __name__ == "__main__":
    monitor = ResourceMonitor()
    monitor.print_metrics()
