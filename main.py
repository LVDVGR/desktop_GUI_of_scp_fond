from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import font
import check_space
import config
from check_space import check_faggots, check_void


def defef():
    from sqlalchemy import create_engine
    import psycopg2
    from config import creds, connection
    import pandas as pd

    user = input_login.get()
    password = input_password.get()

    if not (check_space.check_faggots(user) and check_space.check_void(user) and
            check_space.check_void(password) and check_space.check_faggots(password)):
        f_root = Tk()
        f_root.title('....')
        f_root.geometry("800x200")
        f_root.configure(bg='black')
        font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
        l1 = Label(f_root, text="ЛИБО ТЫ ВВЁЛ ПУСТЫЕ ЗНАЧЕНИЯ, ЛИБО ТЫ ПИДОРАС", font=font1, fg="white", bg="black")
        l1.pack(padx=50, pady=50, side=TOP, anchor=N)
        f_root.mainloop()
    else:
        try:

            engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
                                                                                creds["host"], creds["db_name"]))
            df = pd.read_sql(f"select passwords = crypt('{password}', passwords) AS passwords FROM main.main_stream_employees where logins = '{user}'", engine)

            bools = df['passwords'].values[0]
            print(bools)
            if bools:
                from config import connection
                config.connection = True
                df = pd.read_sql(f"select access_level from main.main_stream_employees where logins = '{user}'", engine)
                config.access_level = df['access_level'].values[0]
                config.curr_user = user
                config.curr_pass = password
                input_root.destroy()

            else:
                f_root = Tk()
                f_root.title('....')
                f_root.geometry("500x400")
                f_root.configure(bg='black')
                font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
                l1 = Label(f_root, text="Пароль не верный", font=font1, fg="white", bg="black")
                l1.pack(padx=50, pady=50, side=TOP, anchor=N)
                f_root.mainloop()
        except:
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("500x400")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Данные логина не верные", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()



input_root = Tk()
input_root.title('Вход')
input_root.geometry("500x400")
input_root.configure(bg='black')

font1 = font.Font(family= "Verdana", size=11, weight="bold", slant="roman")
l1 = Label(input_root, text="ВВЕДИТЕ ДАННЫЕ ДЛЯ ВХОДА В СИСТЕМУ", font=font1, fg="white", bg="black")
l1.pack(padx=50, pady=50, side=TOP, anchor=N)

input_login = Entry(input_root, width=40)
input_login.insert(0, "логин")
input_login.pack(pady=5, padx=5, side=TOP, anchor=N)

input_password = Entry(input_root, width=40)
input_password.insert(0, "пароль")
input_password.pack(pady=5, padx=5, side=TOP, anchor=N)

join = Button(input_root, text="Войти", width=10, height=2, bg="white", fg="black", command=defef)
join.pack(side=TOP, anchor=N, padx=7, pady=7)

input_root.mainloop()



def check_table():
    def search():
        way = combobox.get()
        filter_obj = combobox2.get()
        data = input_field.get()



        if  not check_space.check_faggots(data) and check_space.check_void(data):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="НЕ НАДО ТАК", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            import psycopg2
            from config import creds
            import pandas as pd
            from sqlalchemy import create_engine
            try:
                first_eng = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
                                                                                       creds["host"], creds["db_name"]))
                df = pd.read_sql(f"select access_level from main.main_stream_employees where logins = '{config.curr_user}'", first_eng)['access_level'].values[0]

                if int(df) < 4:
                    engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(config.curr_user, config.curr_pass,
                                                                                       creds["host"], creds["db_name"]))
                else:
                    engine = first_eng

                if way == 'Наблюдений':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.observations where id_obs like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.observations where description_of_obs like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.observations", engine)

                elif way == 'Инцидентов':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.incidents where incident_id like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.incidents where description_of_incident like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.incidents", engine)

                elif way == 'Аномалий':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.anomalous_objects where object_id like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.anomalous_objects where anomaly_name like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.anomalous_objects", engine)

                elif way == 'Коллег':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.main_stream_employees where logins like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.main_stream_employees where nsp like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.main_stream_employees", engine)

                elif way == 'заключенных D класса':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.employee_of_d_class where id_emp like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.employee_of_d_class where nsp like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.employee_of_d_class", engine)

                elif way == 'Задач':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.assignments where id_assigmnt like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.assignments where description like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.assignments", engine)

                elif way == 'Закупок':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.supplys where id_sup like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.supplys where name_sup like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.supplys", engine)

                elif way == 'Списаний':
                    if filter_obj == 'id':
                        df = pd.read_sql(f"select * from main.write_off where id_woff like '%%{data}%%'", engine)
                    elif filter_obj == 'Названию/Имени/Описанию':
                        df = pd.read_sql(f"select * from main.write_off where reason like '%%{data}%%'", engine)
                    else:
                        df = pd.read_sql(f"select * from main.write_off", engine)


                output_root = Tk()
                output_root.title('Вывод...')
                output_root.geometry("1500x1000")

                name_list = []

                cols = df.columns
                for col_name in cols:
                    name_list.append(str(col_name))
                print(name_list[1])
                tree = ttk.Treeview(output_root, columns=name_list, show='headings')

                xsb = ttk.Scrollbar(output_root, orient=tk.HORIZONTAL, command=tree.xview)
                tree.configure(xscrollcommand=xsb.set)

                def on_select(event):
                    from check_space import set_better
                    # вывод текстовых id всех выбранных строк
                    # (их может быть несколько, если при создании дерева не было указано selectmode='browse')
                    print(tree.selection())

                    # Если привязывались не к событию <<TreeviewSelect>>,
                    # то тут нужно проверить, что вообще что-то выбрано:
                    if not tree.selection():
                        return

                    # Получаем id первого выделенного элемента
                    selected_item = tree.selection()[0]

                    # Получаем значения в выделенной строке
                    values = tree.item(selected_item, option="values")

                    select_root = Tk()
                    select_root.title('Вывод...')
                    select_root.geometry("800x800")
                    select_root.configure(bg='black')

                    text = Text(select_root, width=100, height=50, wrap=WORD)
                    text.pack(anchor=NW)
                    text.insert(1.0, check_space.set_better(str(values)))
                    scroll = Scrollbar(select_root, command=text.yview)
                    scroll.pack(side=LEFT, fill=Y)

                    text.config(yscrollcommand=scroll.set)


                tree.bind('<<TreeviewSelect>>', on_select)


                for col in name_list:
                    tree.heading(col, text=col)

                data_list = df.values.tolist()

                for array in data_list:
                    print(data)
                    tree.insert(parent='', index='end', values=array)

                tree.pack(fill=X, padx=5, pady=30)

                output_root.mainloop()




            except Exception as error:
                print('ERROR:', error)

    params_find = ('Наблюдений', 'Инцидентов', 'Аномалий', 'Коллег', 'заключенных D класса', 'Задач', 'Закупок', 'Списание')
    filter = ('id', 'Названию/Имени/Описанию')
    find_root = Tk()
    find_root.title('Поиск клиента')
    find_root.geometry("600x250")
    find_root.configure(bg='black')

    l1 = Label(find_root, text="Просмотр... ", bg="black", fg="white")
    l1.pack(padx=5, pady=5, side=TOP, anchor=NW)

    var = StringVar()
    combobox = ttk.Combobox(find_root, textvariable=var, width=30)
    combobox['values'] = params_find
    combobox['state'] = 'readonly'
    combobox.pack(padx=5, pady=5, side=TOP, anchor=NW)

    l1 = Label(find_root, text="Фильтр по... ", bg="black", fg="white")
    l1.pack(padx=5, pady=5, side=TOP, anchor=NW)

    var = StringVar()
    combobox2 = ttk.Combobox(find_root, textvariable=var, width=30)
    combobox2['values'] = filter
    combobox2['state'] = 'readonly'
    combobox2.pack(padx=5, pady=5, side=TOP, anchor=NW)



    l2 = Label(find_root, text="Введите данные для фильтрации: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    input_field = Entry(find_root, width=33)
    input_field.pack(pady=5, padx=5, side=TOP, anchor=NW)

    search = Button(find_root, text="Поиск", width=10, height=1, bg="white", fg="black", command=search)
    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)

    find_root.mainloop()


def add_obs():
    def add_observation():
        id_scp = id_obj_field.get()
        desciption = descript_field.get()
        datetime = date_field.get()
        access_level_obs = access_field.get()

        if not (check_space.check_faggots(id_scp) and check_space.check_void(id_scp) and
                check_space.check_void(desciption) and check_space.check_faggots(desciption) and
                check_space.check_void(datetime) and check_space.check_faggots(datetime) and
                check_space.check_void(access_level_obs) and check_space.check_faggots(access_level_obs)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(config.curr_user, config.curr_pass,
                                                                    creds["host"], creds["db_name"]))
                df = pd.read_sql('select logins from main.main_stream_employees where logins = current_user', engine)
                current_user = df['id_employee'].values[0]
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(f"call main.add_observations({current_user} :: text, '{id_scp}' :: text, '{desciption}'  :: text, '{datetime}'  :: text, '{access_level_obs}' :: integer)")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")





    obs_root = Tk()
    obs_root.title('welcome, C class')
    obs_root.geometry("800x600")
    obs_root.configure(bg='black')


    l2 = Label(obs_root, text="Введите id наблюдаемого объекта: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_obj_field = Entry(obs_root, width=33)
    id_obj_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l3 = Label(obs_root, text="Опишите наблюдение: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    descript_field = Entry(obs_root, width=33)
    descript_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l4 = Label(obs_root, text="Укажите дату и время до секунды: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    date_field = Entry(obs_root, width=33)
    date_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l5 = Label(obs_root, text="Укажите уровень доступа наблюдения: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    access_field = Entry(obs_root, width=33)
    access_field.pack(pady=5, padx=5, side=TOP, anchor=NW)

    search = Button(obs_root, text="Добавить наблюдение", width=15, height=1, bg="white", fg="black", command=add_observation)
    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()


def add_inc():
    def add_incident():
        id_scp = id_obj_field.get()
        desciption = descript_field.get()
        datetime = date_field.get()
        access_level_obs = access_field.get()
        type_inc = type_field.get()

        if not (check_space.check_faggots(id_scp) and check_space.check_void(id_scp) and
                check_space.check_void(desciption) and check_space.check_faggots(desciption) and
                check_space.check_void(datetime) and check_space.check_faggots(datetime) and
                check_space.check_void(access_level_obs) and check_space.check_faggots(access_level_obs) and
                check_space.check_void(type_inc) and check_space.check_faggots(type_inc)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(f"call main.add_incident('{id_scp}' :: text, '{datetime}'  :: text,'{type_inc}' :: text, '{desciption}'  :: text,  '{access_level_obs}' :: integer)")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")





    obs_root = Tk()
    obs_root.title('welcome, C class')
    obs_root.geometry("800x600")
    obs_root.configure(bg='black')


    l2 = Label(obs_root, text="Введите id наблюдаемого объекта: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_obj_field = Entry(obs_root, width=33)
    id_obj_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l6 = Label(obs_root, text="Укажите тип инцидента: ", bg="black", fg="white")
    l6.pack(padx=5, pady=5, side=TOP, anchor=NW)

    type_field = Entry(obs_root, width=33)
    type_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l3 = Label(obs_root, text="Опишите инцидент: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    descript_field = Entry(obs_root, width=33)
    descript_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l4 = Label(obs_root, text="Укажите дату инцидента: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    date_field = Entry(obs_root, width=33)
    date_field.pack(pady=5, padx=5, side=TOP, anchor=NW)


    l5 = Label(obs_root, text="Укажите уровень доступа инцидента: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    access_field = Entry(obs_root, width=33)
    access_field.pack(pady=5, padx=5, side=TOP, anchor=NW)

    search = Button(obs_root, text="Добавить инцидент", width=15, height=1, bg="white", fg="black", command=add_incident)
    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()


def get_stats():
    from config import creds, curr_user, curr_pass
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(config.curr_user, config.curr_pass,
                                                                           creds["host"], creds["db_name"]))

    df_task = pd.read_sql("select main.count_tasks() as counter", engine)['counter'].values[0]

    df_incident = pd.read_sql("select main.count_incident() as counter", engine)['counter'].values[0]

    df_objects = pd.read_sql("select main.count_anomalous() as counter", engine)['counter'].values[0]

    df_emp_d = pd.read_sql("select main.count_d_emp() as counter", engine)['counter'].values[0]

    total = f"Задачи к выполнению: {df_task}.  Кол-во инцидентов: {df_incident}.  Аномальные объекты в комплексе: {df_objects}.  Свободных сотрудников D класса: {df_emp_d}."

    return total



def close_task():
    close_root = Tk()
    close_root.title('welcome, C class')
    close_root.geometry("600x600")
    close_root.configure(bg='black')

    def close():
        id = id_task.get()
        status = status_task.get()
        if not (check_space.check_faggots(id) and check_space.check_void(id) and
                check_space.check_void(status) and check_space.check_faggots(status)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"update main.assignments set status = '{status}', finish_date = now() where id_assigmnt = {int(id)}")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")




    l2 = Label(close_root, text="Введите id задачи: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_task = Entry(close_root, width=33)
    id_task.pack(pady=5, padx=5, side=TOP, anchor=NW)

    l6 = Label(close_root, text="Укажите статус задачи: ", bg="black", fg="white")
    l6.pack(padx=5, pady=5, side=TOP, anchor=NW)

    status_task = Entry(close_root, width=33)
    status_task.pack(pady=5, padx=5, side=TOP, anchor=NW)



    search = Button(close_root, text="Закрыть задачу", width=15, height=1, bg="white", fg="black",
                    command=close)
    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    close_root.mainloop()

def update_d_class():
    close_root = Tk()
    close_root.title('welcome, C class')
    close_root.geometry("600x600")
    close_root.configure(bg='black')

    def update():
        id = id_d.get()
        status = combobox.get()
        if not (check_space.check_faggots(id) and check_space.check_void(id)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"update main.employee_of_d_class set status = '{status}' where id_emp = {int(id)}")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")


    params = ['Готов к распоряжениям', 'Мёртв', 'Освобождён', 'Госпитализован']

    l2 = Label(close_root, text="Введите id сотрудника: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_d = Entry(close_root, width=33)
    id_d.pack(pady=5, padx=5, side=TOP, anchor=NW)

    l6 = Label(close_root, text="Укажите статус сотрудника: ", bg="black", fg="white")
    l6.pack(padx=5, pady=5, side=TOP, anchor=NW)

    var = StringVar()
    combobox = ttk.Combobox(close_root, textvariable=var, width=30)
    combobox['values'] = params
    combobox['state'] = 'readonly'
    combobox.pack(padx=5, pady=5, side=TOP, anchor=NW)



    search = Button(close_root, text="Обновить статус", width=15, height=1, bg="white", fg="black",
                    command=update)
    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    close_root.mainloop()





def welcome_to_system_c():
    system_root = Tk()
    system_root.title('welcome, C class')
    system_root.geometry("800x600")
    system_root.configure(bg='black')

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    search = Button(system_root, text="Просмотр данных", width=20, height=2, bg="white", fg="black", command=check_table, font=font1)
    search.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_observ = Button(system_root, text="Добавить наблюдение", width=30, height=2, bg="white", fg="black", command=add_obs, font=font1)
    add_observ.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_stat = Button(system_root, text="Обновить статус D класса.", width=40, height=2, bg="white", fg="black",
                        command=update_d_class, font=font1)
    add_d_stat.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_incid = Button(system_root, text="Добавить инцидент", width=30, height=2, bg="white", fg="black", command=add_inc, font=font1)
    add_incid.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    close_assig = Button(system_root, text="Закрыть задачу", width=20, height=2, bg="white", fg="black", command=close_task, font=font1)
    close_assig.pack(side=TOP, anchor=NW, padx=50, pady=25)



    statistics_od_complex = get_stats()
    l5 = Label(system_root, text=statistics_od_complex, bg="black", fg="white", width=100)
    l5.pack(padx=50, pady=5, side=BOTTOM, anchor=W)



    system_root.mainloop()


def register_d():
    def add_d_emp():
        id = id_d.get()
        nsp = nsp_d.get()
        age = age_d.get()
        dossier = dossier_d.get()
        date = date_d.get()
        status = combobox.get()
        if not (check_space.check_faggots(nsp) and check_space.check_void(nsp) and
                check_space.check_void(dossier) and check_space.check_faggots(dossier) and
                check_space.check_faggots(date) and check_space.check_void(date) and
                check_space.check_void(age) and check_space.check_faggots(age) and
                check_space.check_void(id) and check_space.check_faggots(id)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"call main.add_d_employee('{id}', '{nsp}', {int(age)}, '{dossier}', '{date}', '{status}')")
                    print('i tut')
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")


    obs_root = Tk()
    obs_root.title('register D employees')
    obs_root.geometry("500x500")
    obs_root.configure(bg='black')

    l9 = Label(obs_root, text="Задайте численный идентификатор: ", bg="black", fg="white")
    l9.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_d = Entry(obs_root, width=33)
    id_d.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l2 = Label(obs_root, text="Имя сотрудника: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    nsp_d = Entry(obs_root, width=33)
    nsp_d.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l8 = Label(obs_root, text="Возраст: ", bg="black", fg="white")
    l8.pack(padx=5, pady=5, side=TOP, anchor=NW)

    age_d = Entry(obs_root, width=33)
    age_d.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l3 = Label(obs_root, text="Досье: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    dossier_d = Entry(obs_root, width=33)
    dossier_d.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l4 = Label(obs_root, text="Укажите дату вербовки: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    date_d = Entry(obs_root, width=33)
    date_d.pack(pady=5, padx=50, side=TOP, anchor=NW)

    params = ['Готов к распоряжениям', 'Мёртв', 'Освобождён', 'Госпитализован']
    l6 = Label(obs_root, text="Укажите статус сотрудника: ", bg="black", fg="white")
    l6.pack(padx=5, pady=5, side=TOP, anchor=NW)
    var = StringVar()
    combobox = ttk.Combobox(obs_root, textvariable=var, width=30)
    combobox['values'] = params
    combobox['state'] = 'readonly'
    combobox.pack(padx=50, pady=5, side=TOP, anchor=NW)

    search = Button(obs_root, text="Добавить сотрудника", width=20, height=1, bg="white", fg="black", command=add_d_emp)

    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()

def create_task():
    def add_assignment():
        scp = id_obj.get()
        description = descr.get()
        employeer = empl.get()
        date_start = date.get()
        status_task = status.get()
        equipment = equip.get()
        d_emp = d_cl.get()
        if not (check_space.check_faggots(scp) and check_space.check_void(scp) and
                check_space.check_void(description) and check_space.check_faggots(description) and
                check_space.check_faggots(date_start) and check_space.check_void(date_start) and
                check_space.check_void(employeer) and check_space.check_faggots(employeer) and
                check_space.check_void(status_task) and check_space.check_faggots(status_task) and
                check_space.check_void(equipment) and check_space.check_faggots(equipment) and
                check_space.check_void(d_emp) and check_space.check_faggots(d_emp)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=creds['user'],
                                              password=creds['password'], database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"call main.add_assignment('{scp}', '{description}', {employeer}, '{date_start}', '{status_task}', '{equipment}', '{d_emp}')")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")


    obs_root = Tk()
    obs_root.title('register D employees')
    obs_root.geometry("500x500")
    obs_root.configure(bg='black')

    l9 = Label(obs_root, text="Объект распоряжения: ", bg="black", fg="white")
    l9.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_obj = Entry(obs_root, width=33)
    id_obj.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l2 = Label(obs_root, text="Описание распоряжения: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    descr = Entry(obs_root, width=33)
    descr.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l8 = Label(obs_root, text="Внесите login исполнителя: ", bg="black", fg="white")
    l8.pack(padx=5, pady=5, side=TOP, anchor=NW)

    empl = Entry(obs_root, width=33)
    empl.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l3 = Label(obs_root, text="Внесите дату начала исполнения: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    date = Entry(obs_root, width=33)
    date.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l4 = Label(obs_root, text="Статус: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    status = Entry(obs_root, width=33)
    status.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Введите id предоставляемого оборудования: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    equip = Entry(obs_root, width=33)
    equip.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Введите id сотрудника D класса: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    d_cl = Entry(obs_root, width=33)
    d_cl.pack(pady=5, padx=50, side=TOP, anchor=NW)

    search = Button(obs_root, text="Добавить распоряжение", width=30, height=1, bg="white", fg="black", command=add_assignment)

    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()



def add_scp():
    def add_object():
        id_scp = id_obj.get()
        name = descr.get()
        description = empl.get()
        danger = combobox2.get()
        conditions = status.get()
        incidents = equip.get()
        age = d_cl.get()
        date = dates.get()
        access_level = combobox.get()
        if not (check_space.check_faggots(id_scp) and check_space.check_void(id_scp) and
                check_space.check_void(description) and check_space.check_faggots(description) and
                check_space.check_faggots(name) and check_space.check_void(name) and
                check_space.check_void(danger) and check_space.check_faggots(danger) and
                check_space.check_void(conditions) and check_space.check_faggots(conditions) and
                check_space.check_void(incidents) and check_space.check_faggots(incidents) and
                check_space.check_void(age) and check_space.check_faggots(age) and
                check_space.check_faggots(date) and check_space.check_void(date) and
                check_space.check_faggots(access_level) and check_space.check_void(access_level)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"call main.add_object('{id_scp}', '{name}', '{description}', '{danger}', '{conditions}', {int(incidents)}, {int(age)}, '{date}', {int(access_level)})")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")


    obs_root = Tk()
    obs_root.title('register D employees')
    obs_root.geometry("500x800")
    obs_root.configure(bg='black')

    l9 = Label(obs_root, text="Задайте идентификатор объекта: ", bg="black", fg="white")
    l9.pack(padx=5, pady=5, side=TOP, anchor=NW)

    id_obj = Entry(obs_root, width=33)
    id_obj.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l2 = Label(obs_root, text="Имя объекта: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    descr = Entry(obs_root, width=33)
    descr.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l8 = Label(obs_root, text="Описание: ", bg="black", fg="white")
    l8.pack(padx=5, pady=5, side=TOP, anchor=NW)

    empl = Entry(obs_root, width=33)
    empl.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l3 = Label(obs_root, text="Уровень опасности: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    params = ['безопасный', 'евклид', 'кетер', 'таумиэль']
    var = StringVar()
    combobox2 = ttk.Combobox(obs_root, textvariable=var, width=30)
    combobox2['values'] = params
    combobox2['state'] = 'readonly'
    combobox2.pack(padx=50, pady=5, side=TOP, anchor=NW)

    l4 = Label(obs_root, text="Условия содержания: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    status = Entry(obs_root, width=33)
    status.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Кол-во инцидентов: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    equip = Entry(obs_root, width=33)
    equip.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Предположительный возраст: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    d_cl = Entry(obs_root, width=33)
    d_cl.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l10 = Label(obs_root, text="Содержится с...: ", bg="black", fg="white")
    l10.pack(padx=5, pady=5, side=TOP, anchor=NW)

    dates = Entry(obs_root, width=33)
    dates.pack(pady=5, padx=50, side=TOP, anchor=NW)


    l11 = Label(obs_root, text="Уровень доступа: ", bg="black", fg="white")
    l11.pack(padx=5, pady=5, side=TOP, anchor=NW)
    params = [1, 2, 3, 4]
    var = StringVar()
    combobox = ttk.Combobox(obs_root, textvariable=var, width=30)
    combobox['values'] = params
    combobox['state'] = 'readonly'
    combobox.pack(padx=50, pady=5, side=TOP, anchor=NW)


    search = Button(obs_root, text="Добавить объект", width=30, height=1, bg="white", fg="black",
                    command=add_object)

    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()

def welcome_to_system_b():
    system_root = Tk()
    system_root.title('welcome, B class')
    system_root.geometry("800x800")
    system_root.configure(bg='black')

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    search = Button(system_root, text="Просмотр данных", width=20, height=2, bg="white", fg="black", command=check_table, font=font1)
    search.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_observ = Button(system_root, text="Добавить наблюдение", width=30, height=2, bg="white", fg="black", command=add_obs, font=font1)
    add_observ.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_stat = Button(system_root, text="Обновить статус D класса.", width=40, height=2, bg="white", fg="black", command=update_d_class, font=font1)
    add_d_stat.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_incid = Button(system_root, text="Добавить инцидент", width=30, height=2, bg="white", fg="black", command=add_inc, font=font1)
    add_incid.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    close_assig = Button(system_root, text="Закрыть задачу", width=20, height=2, bg="white", fg="black", command=close_task, font=font1)
    close_assig.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_emp = Button(system_root, text="Добавить сотрудика класса D", width=30, height=2, bg="white", fg="black", command=register_d, font=font1)
    add_d_emp.pack(side=TOP, anchor=NW, padx=50, pady=25)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_emp = Button(system_root, text="Создать распоряжение", width=40, height=2, bg="white", fg="black", command=create_task, font=font1)
    add_d_emp.pack(side=TOP, anchor=NW, padx=50, pady=25)


    statistics_od_complex = get_stats()
    l5 = Label(system_root, text=statistics_od_complex, bg="black", fg="white", width=100)
    l5.pack(padx=50, pady=5, side=BOTTOM, anchor=W)



    system_root.mainloop()



def new_user():
    def register():
        login = login_input.get()
        nsp = nsp_input.get()
        age = age_input.get()
        access_levels = combobox_lev.get()
        speciality = special_input.get()
        date = date_input.get()
        disease = disease_input.get()
        password = password_input.get()
        if not (check_space.check_faggots(login) and check_space.check_void(login) and
                check_space.check_void(nsp) and check_space.check_faggots(nsp) and
                check_space.check_faggots(age) and check_space.check_void(age) and
                check_space.check_void(access_levels) and check_space.check_faggots(access_levels) and
                check_space.check_void(speciality) and check_space.check_faggots(speciality) and
                check_space.check_void(date) and check_space.check_faggots(date) and
                check_space.check_void(disease) and check_space.check_faggots(disease) and
                check_space.check_faggots(password) and check_space.check_void(password)):
            f_root = Tk()
            f_root.title('....')
            f_root.geometry("800x200")
            f_root.configure(bg='black')
            font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
            l1 = Label(f_root, text="Ввод инъекции или пустых значений недопустим", font=font1, fg="white", bg="black")
            l1.pack(padx=50, pady=50, side=TOP, anchor=N)
            f_root.mainloop()
        else:
            try:
                import psycopg2
                from config import creds, curr_user, curr_pass, access_level
                from sqlalchemy import create_engine
                import pandas as pd

                class_access = ''
                if (int(access_levels) == 1) or (int(access_level) == 2) or (int(access_level) == 3):
                    class_access = 'c'
                elif (int(access_levels) == 4):
                    class_access = 'b'
                elif (int(access_levels) == 5):
                    class_access = 'a'

                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"call main.add_employee('{login}', '{nsp}', {int(age)}, '{class_access}', {int(access_levels)}, '{speciality}', '{date}', '{disease}', '{password}')")
                    cursor.execute(f"create role {login} inherit login password '{password}';")
                    cursor.execute(f"grant access_level_{str(access_levels)} to {str(login)}")
                    connection.commit()
            except Exception as error:
                print(f'{error}')
            finally:
                if connection:
                    connection.close()
                    print("connection closed")


    obs_root = Tk()
    obs_root.title('register D employees')
    obs_root.geometry("500x500")
    obs_root.configure(bg='black')

    l9 = Label(obs_root, text="Создайте логин: ", bg="black", fg="white")
    l9.pack(padx=5, pady=5, side=TOP, anchor=NW)

    login_input = Entry(obs_root, width=33)
    login_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l2 = Label(obs_root, text="Укажите ФИО: ", bg="black", fg="white")
    l2.pack(padx=5, pady=5, side=TOP, anchor=NW)

    nsp_input = Entry(obs_root, width=33)
    nsp_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l8 = Label(obs_root, text="Укажите возраст: ", bg="black", fg="white")
    l8.pack(padx=5, pady=5, side=TOP, anchor=NW)

    age_input = Entry(obs_root, width=33)
    age_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l3 = Label(obs_root, text="Уровень доступа: ", bg="black", fg="white")
    l3.pack(padx=5, pady=5, side=TOP, anchor=NW)

    params = [1, 2, 3, 4, 5]
    var = StringVar()
    combobox_lev = ttk.Combobox(obs_root, textvariable=var, width=30)
    combobox_lev['values'] = params
    combobox_lev['state'] = 'readonly'
    combobox_lev.pack(padx=50, pady=5, side=TOP, anchor=NW)

    l4 = Label(obs_root, text="Напишите специальность: ", bg="black", fg="white")
    l4.pack(padx=5, pady=5, side=TOP, anchor=NW)

    special_input = Entry(obs_root, width=33)
    special_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Дата зачисления: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    date_input = Entry(obs_root, width=33)
    date_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l5 = Label(obs_root, text="Заболевания: ", bg="black", fg="white")
    l5.pack(padx=5, pady=5, side=TOP, anchor=NW)

    disease_input = Entry(obs_root, width=33)
    disease_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    l11 = Label(obs_root, text="Придумайте пароль: ", bg="black", fg="white")
    l11.pack(padx=5, pady=5, side=TOP, anchor=NW)

    password_input = Entry(obs_root, width=33)
    password_input.pack(pady=5, padx=50, side=TOP, anchor=NW)

    search = Button(obs_root, text="Зарегестрировать", width=30, height=1, bg="white", fg="black",
                    command=register)

    search.pack(side=RIGHT, anchor=SE, padx=5, pady=5)
    obs_root.mainloop()



def welcome_to_system_master():
    system_root = Tk()
    system_root.title('welcome, a class')
    system_root.geometry("800x800")
    system_root.configure(bg='black')

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    search = Button(system_root, text="Просмотр данных", width=20, height=2, bg="white", fg="black",
                    command=check_table, font=font1)
    search.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_observ = Button(system_root, text="Добавить наблюдение", width=30, height=2, bg="white", fg="black",
                        command=add_obs, font=font1)
    add_observ.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_stat = Button(system_root, text="Обновить статус D класса.", width=40, height=2, bg="white", fg="black",
                        command=update_d_class, font=font1)
    add_d_stat.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_incid = Button(system_root, text="Добавить инцидент", width=30, height=2, bg="white", fg="black",
                       command=add_inc, font=font1)
    add_incid.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    close_assig = Button(system_root, text="Закрыть задачу", width=20, height=2, bg="white", fg="black",
                         command=close_task, font=font1)
    close_assig.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_emp = Button(system_root, text="Добавить сотрудика класса D", width=30, height=2, bg="white", fg="black",
                       command=register_d, font=font1)
    add_d_emp.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_d_emp = Button(system_root, text="Создать распоряжение", width=40, height=2, bg="white", fg="black",
                       command=create_task, font=font1)
    add_d_emp.pack(side=TOP, anchor=NW, padx=50, pady=10)



    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_obj = Button(system_root, text="Добавить объект", width=30, height=2, bg="white", fg="black",
                       command=add_scp, font=font1)
    add_obj.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_obj = Button(system_root, text="Внести закупку", width=20, height=2, bg="white", fg="black",
                     command=create_task, font=font1)
    add_obj.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_obj = Button(system_root, text="Внести списание", width=30, height=2, bg="white", fg="black",
                     command=create_task, font=font1)
    add_obj.pack(side=TOP, anchor=NW, padx=50, pady=10)

    font1 = font.Font(family="Verdana", size=11, weight="bold", slant="roman")
    add_obj = Button(system_root, text="Регистрация", width=40, height=2, bg="white", fg="black",
                     command=new_user, font=font1)
    add_obj.pack(side=TOP, anchor=NW, padx=50, pady=10)

    statistics_od_complex = get_stats()
    l5 = Label(system_root, text=statistics_od_complex, bg="black", fg="white", width=100)
    l5.pack(padx=50, pady=5, side=BOTTOM, anchor=W)

    system_root.mainloop()

if config.connection is True:

    if int(config.access_level) == 2 or int(config.access_level) == 1 or int(config.access_level) == 3:
        welcome_to_system_c()
    elif int(config.access_level) == 4:
        welcome_to_system_b()
    elif int(config.access_level) == 5:
        welcome_to_system_master()
else:
    print("nah")




