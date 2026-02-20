import psutil

print("Системный монитор\n")

cpu = psutil.cpu_percent(interval=1)
print(f"CPU: {cpu}%")

data = psutil.virtual_memory()
print(f"ОЗУ: использовано {data.percent}% ({data.used // (1024 ** 3)} ГБ из {data.total // (1024 ** 3)} ГБ)")

disk = psutil.disk_usage('/')
print(f"Диск: занято {disk.percent}% ({disk.used // (1024 ** 3)} ГБ из {disk.total // (1024 ** 3)} ГБ)")

print("\nДанные обновлены")