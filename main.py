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
                engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(config.curr_user, config.curr_pass,
                                                                                       creds["host"], creds["db_name"]))

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
                        df = pd.read_sql(f"select * from main.main_stream_employees where id_employee like '%%{data}%%'", engine)
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
                df = pd.read_sql('select id_employee from main.main_stream_employees where logins = current_user', engine)
                current_user = df['id_employee'].values[0]
                connection = psycopg2.connect(host=creds["host"], user=curr_user,
                                              password=curr_pass, database=creds["db_name"])
                with connection.cursor() as cursor:
                    cursor.execute(f"call main.add_observations({current_user} :: integer, '{id_scp}' :: text, '{desciption}'  :: text, '{datetime}'  :: text, '{access_level_obs}' :: integer)")
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


    l2 = Label(obs_root, text="Введите id наблюдаемого субъекта: ", bg="black", fg="white")
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
    add_incid = Button(system_root, text="Добавить инцидент", width=40, height=2, bg="white", fg="black", command=add_inc, font=font1)
    add_incid.pack(side=TOP, anchor=NW, padx=50, pady=25)

    system_root.mainloop()


def welcome_to_system_a():
    pass

def welcome_to_system_master():
    pass

if config.connection is True:

    if int(config.access_level) == 2 or int(config.access_level) == 1 or int(config.access_level) == 3:
        welcome_to_system_c()
    elif int(config.access_level) == 4:
        welcome_to_system_a()
    elif int(config.access_level) == 5:
        welcome_to_system_master()
else:
    print("nah")




