import json
import os

#global değişkenler
tasks = []
next_id = 1
FILE_NAME = "task.json"

def load_tasks():
    """görevleri dosyadan yükler."""
    global tasks, next_id
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r' , encoding='utf-8') as f:
                data = json.load(f)
                tasks = data.get("tasks", [])
                next_id = data.get("next_id", 1)
            print("Görevler yüklendi.")
        except json.JSONDecodeError:
            print("Görev dosyası bozuk, yeni liste oluşturuluyor.")
            tasks = []
            next_id = 1
    else:
        tasks = []
        next_id = 1
        print("Görev Dosyası bulunamadı, yeni liste oluşturuldu.")

def save_tasks():
    """görevleri dosyaya kaydeder."""
    with open(FILE_NAME, 'w' , encoding='utf-8') as f:
        json.dump({"tasks": tasks, "next_id": next_id}, f, indent=4, ensure_ascii=False)
    print("Görevler kaydedildi.")

def add_tasks(description):
    """yeni bir görev ekler."""
    global next_id
    tasks.append({"id": next_id, "description": description, "completed": False})
    print(f"'{description}' görevi eklendi. (ID: {next_id})")
    next_id += 1

def list_tasks():
    """tüm görevleri listeler"""
    if not tasks:
        print("listenizde henüz bir görev yok.")
        return
    print("\n---Görev Listeniz---")
    for task in tasks:
        status = "[x]" if task["completed"] else "[ ]"
        print(f"{status} ID: {task['id']} - {task['description']}")
    print("-------------------\n")

def complete_tasks(task_id):
    """belirtilen ID'ye sahip görevi tamamlandı olarak işaretler."""
    for task in tasks:
        if task ["id"] == task_id:
            task["completed"] = True
            print(f"ID {task_id} olan görev tamamlandı olarak işaretlendi.")
            return
        print(f"ID {task_id} ile eşleşen görev bulunamadı.")

def delete_tasks(task_id):
    """belirtilen ID'ye sahip görevi siler."""
    global tasks
    initial_task_count = len(tasks)
    tasks =[task for task in tasks if task["id"] != task_id]
    if len(tasks) < initial_task_count:
        print(f"ID {task_id} olan görev silindi.")
    else:
        print(f"ID {task_id} ile eşleşen görev bulunamadı.")

def filter_tasks(status_filter):
    """görevleri tamamlanma durumuna göre filtreler
    (True: tamamlanmul görevler, False: tamamlanmamış görevler """
#filtrelenmiş görevleri depolamak için boş bir liste oluşturur.
    filtered = []
    for task in tasks:
        if task["completed"] == status_filter:
            filtered.append(task)
    if not filtered:
        #eğer filtreye uyan görev yoksa kullanıcıya bilgi verir
        print(f"Hiç {'tamamlanmış' if status_filter else 'tamamlanmamış' } görev yok.")
        return

    #filtrelenmiş görevleri liste başlığıyla birlikte gösterir
    print(f"\n---{ 'Tamamlanmış' if status_filter else 'Tamamlanmamış' } Görev listeniz ---")
    for task in filtered:
        status = "[x]" if task["completed"] else "[ ]"
        # öncelik bilgisi varsa onuda gösterir
        priority = task.get("priority", "Belirtilmemiş")
        print(f"{status} ID: {task['id']} - [{priority}] - {task['description']}")
    print("----------------------------------------\n")
def display_menu():
    """kullanıcıya menüyü gösterir."""
    print("yapılacaklar listesi uygulaması")
    print("1. görev ekle")
    print("2. görevleri listele")
    print("3. görev tamamla")
    print("4. görev sil")
    print("5. Görev Düzenle")
    print("6. Görevleri Filtrele")
    print("7. çıkış")
    print("--------------------------")

def main():
    """uygulamanın ana döngüsü"""
    load_tasks() # uygulama başlarken görevleri yükle

    while True:
        display_menu()
        choice = input("seçiminizi yapın (1-7): ")

        if choice == '1':
            description = input("eklemek istediğiniz görevi yazın: ")
            add_tasks(description)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            try:
                task_id = int(input("tamamlamak istediğiniz görevin ID' sini girin."))
                complete_tasks(task_id)
            except ValueError:
                print("Geçersiz ID. Lütfen bir sayı girin. ")
        elif choice == '4':
            try:
                task_id = int(input("Silmek istediğiniz görevin ID'sini girin."))
                delete_tasks(task_id)
            except ValueError:
                print("Geçersiz ID. lütfen bir sayı girin. ")

        elif choice == '6' : # yeni: görev filtrele
            print("\nFiltreleme Seçenekleri:")
            print("1. Tamamlanmamış Görevler")
            print("2. Tamamnlanmış Görevler")
            filter_choice = input("Seçiminizi Yapın (1-2: ")
            if filter_choice == '1':
                filter_tasks(False) #tamamlanmamışları göster
            elif filter_choice == '2':
                filter_tasks(True)  #tamamlanmışları göster
            else:
                print("Geçersiz filtreleme seçimi.")
        elif choice == '7':
            save_tasks() # uygulama kapanırken görevleri kaydet
            print("Uygulamadan çıkılıyor. hoşka kalın!")
            break
        else:
            print("geçersiz seçim. lütfen 1 ile 7 arasında bir sayı girin.")
        if choice != '7':
            input("devam etmek için enter'a basın...") # kullanıcının çıktıyı görmesi için

#komutları editörde çalıştırmaya yarar#
if __name__ == "__main__":
    main()

