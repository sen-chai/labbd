import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import configparser


# Configuração da conexão com o banco de dados
def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']


# Define a janela exibida após o login bem-sucedido para Admin
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=f"Olá, Admin!")
        self.label.pack(pady=20)

        # Obtém a quantidade de pilotos cadastrados
        pilot_count = self.get_pilot_count()  # Substitua com a função apropriada
        self.pilots_label = tk.Label(self, text=f"Pilotos cadastrados: {pilot_count}")
        self.pilots_label.pack()

        # Obtém a quantidade de escuderias cadastradas
        constructor_count = self.get_constructor_count()  # Substitua com a função apropriada
        self.constructors_label = tk.Label(self, text=f"Escuderias cadastradas: {constructor_count}")
        self.constructors_label.pack()

        # Obtém a quantidade de corridas cadastradas
        race_count = self.get_race_count()  # Substitua com a função apropriada
        self.races_label = tk.Label(self, text=f"Corridas cadastradas: {race_count}")
        self.races_label.pack()

        # Obtém a quantidade de temporadas (seasons) cadastradas
        season_count = self.get_season_count()  # Substitua com a função apropriada
        self.seasons_label = tk.Label(self, text=f"Temporadas cadastradas: {season_count}")
        self.seasons_label.pack(pady=(0, 10))

        self.escuderia_button = tk.Button(self, text="Cadastrar Escuderias",
                                          command=lambda: self.master.switch_frame(EscuderiaRegisterFrame(self.master)))
        self.escuderia_button.pack()

        self.piloto_button = tk.Button(self, text="Cadastrar Pilotos",
                                       command=lambda: self.master.switch_frame(PilotoRegisterFrame(self.master)))
        self.piloto_button.pack()

        self.button = tk.Button(self, text="Acessar Relatórios",
                                command=lambda: self.master.switch_frame(ReportFrame(self.master)))
        self.button.pack(pady=10)

        self.logout_button = tk.Button(self, text="Sair", command=self.logout)
        self.logout_button.pack(side="bottom", pady=50)

    def logout(self):
        self.master.switch_frame(self.master.login_frame)

    # Funções para obter as informações de overview
    def get_pilot_count(self):
        # Conecta ao banco de dados e obtém a quantidade de pilotos
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM driver")
        pilot_count = c.fetchone()[0]
        conn.close()
        return pilot_count

    def get_constructor_count(self):
        # Conecta ao banco de dados e obtém a quantidade de escuderias
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM constructors")
        constructor_count = c.fetchone()[0]
        return constructor_count

    def get_race_count(self):
        # Conecta ao banco de dados e obtém a quantidade de corridas
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM races")
        race_count = c.fetchone()[0]
        return race_count

    def get_season_count(self):
        # Conecta ao banco de dados e obtém a quantidade de temporadas
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM seasons")
        race_count = c.fetchone()[0]
        return race_count


# Define a janela para cadastro de escuderias
class EscuderiaRegisterFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.ref_label = tk.Label(self, text="Referência da Escuderia")
        self.ref_entry = tk.Entry(self)
        self.name_label = tk.Label(self, text="Nome da Escuderia")
        self.name_entry = tk.Entry(self)
        self.nationality_label = tk.Label(self, text="Nacionalidade")
        self.nationality_entry = tk.Entry(self)
        self.wiki_label = tk.Label(self, text="Link no Wikipédia")
        self.wiki_entry = tk.Entry(self)

        self.ref_label.pack()
        self.ref_entry.pack()
        self.name_label.pack()
        self.name_entry.pack()
        self.nationality_label.pack()
        self.nationality_entry.pack()
        self.wiki_label.pack()
        self.wiki_entry.pack()

        self.register_button = tk.Button(self, text="Cadastrar", command=self.register_escuderia)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Voltar",
                                     command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master)))
        self.back_button.pack()

    def register_escuderia(self):
        constructorref = self.ref_entry.get()
        name = self.name_entry.get()
        nationality = self.nationality_entry.get()
        url = self.wiki_entry.get()

        constructorid = 1000 + sum(ord(char) for char in constructorref)

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO constructors (constructorid, constructorref, name, nationality, url) VALUES (%s, %s, %s, %s, %s)",
                (constructorid, constructorref, name, nationality, url))
            conn.commit()

            # Limpa os campos de entrada
            self.ref_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.nationality_entry.delete(0, tk.END)
            self.wiki_entry.delete(0, tk.END)

            messagebox.showinfo("Sucesso", "Escuderia cadastrada com sucesso")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e.pgerror.split('CONTEXT')[0]}")
        finally:
            conn.close()


# Define a janela para cadastro de pilotos
class PilotoRegisterFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.ref_label = tk.Label(self, text="Referência do Piloto")
        self.ref_entry = tk.Entry(self)
        self.number_label = tk.Label(self, text="Número de Corrida")
        self.number_entry = tk.Entry(self)
        self.code_label = tk.Label(self, text="Código (XXX)")
        self.code_entry = tk.Entry(self)
        self.name_label = tk.Label(self, text="Nome")
        self.name_entry = tk.Entry(self)
        self.surname_label = tk.Label(self, text="Sobrenome")
        self.surname_entry = tk.Entry(self)
        self.dob_label = tk.Label(self, text="Data de Nascimento (AAAA-MM-DD)")
        self.dob_entry = tk.Entry(self)
        self.nationality_label = tk.Label(self, text="Nacionalidade")
        self.nationality_entry = tk.Entry(self)
        self.wiki_label = tk.Label(self, text="Wiki")
        self.wiki_entry = tk.Entry(self)

        self.ref_label.pack()
        self.ref_entry.pack()
        self.number_label.pack()
        self.number_entry.pack()
        self.code_label.pack()
        self.code_entry.pack()
        self.name_label.pack()
        self.name_entry.pack()
        self.surname_label.pack()
        self.surname_entry.pack()
        self.dob_label.pack()
        self.dob_entry.pack()
        self.nationality_label.pack()
        self.nationality_entry.pack()
        self.wiki_label.pack()
        self.wiki_entry.pack()

        self.register_button = tk.Button(self, text="Cadastrar", command=self.register_piloto)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Voltar",
                                     command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master)))
        self.back_button.pack()

    def register_piloto(self):
        driverref = self.ref_entry.get()
        number = self.number_entry.get()
        code = self.code_entry.get()
        forename = self.name_entry.get()
        surname = self.surname_entry.get()
        dob = self.dob_entry.get()
        nationality = self.nationality_entry.get()
        wiki = self.wiki_entry.get()

        driverid = 1000 + sum(ord(char) for char in driverref)

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO driver (driverid, driverref, number, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (driverid, driverref, number, code, forename, surname, dob, nationality, wiki))
            conn.commit()

            # Limpa os campos de entrada
            self.ref_entry.delete(0, tk.END)
            self.number_entry.delete(0, tk.END)
            self.code_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.nationality_entry.delete(0, tk.END)
            self.wiki_entry.delete(0, tk.END)

            messagebox.showinfo("Sucesso", "Piloto cadastrado com sucesso")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e.pgerror.split('CONTEXT')[0]}")
        finally:
            conn.close()


# Define a janela que exibe os relatórios disponíveis para Admin
class ReportFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="Relatórios de Administrador")
        self.label.pack(pady=20)

        self.status_button = tk.Button(self, text="Relatório de Resultados dos Status",
                                       command=lambda: self.master.switch_frame(ReportStatusResultsFrame(self.master)))
        self.status_button.pack()

        self.airports_button = tk.Button(self, text="Relatório de Aeroportos Brasileiros Próximos",
                                         command=lambda: self.master.switch_frame(ReportAirportsFrame(self.master)))
        self.airports_button.pack()

        self.back_button = tk.Button(self, text="Voltar",
                                     command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master)))
        self.back_button.pack(side="bottom", pady=20)


# Define a janela que exibe o relatório de Resultados dos Status
class ReportStatusResultsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.city_label = tk.Label(self, text="Relatório de Resultados dos Status")
        self.city_label.pack(pady=20)

        self.create_table()

        self.back_button = tk.Button(self, text="Voltar",
                                     command=lambda: self.master.switch_frame(ReportFrame(self.master)))
        self.back_button.pack(side="bottom", pady=20)

    def create_table(self):
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute(
            "SELECT s.status, count(*)"
            " FROM results r"
            " JOIN status s on s.statusid=r.statusid"
            " GROUP by s.status"
            " ORDER BY s.status"
        )

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = (
            "Coluna 1", "Coluna 2")

        tree.column("Coluna 1", width=100)
        tree.heading("Coluna 1", text="Status")

        tree.column("Coluna 2", width=100)
        tree.heading("Coluna 2", text="Contagem")

        data = c.fetchall()

        print(len(data))

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()


# Define a janela que exibe o relatório de Aeroportos Brasileiros Próximos
class ReportAirportsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.city_label = tk.Label(self, text="Relatório de Aeroportos Brasileiros Próximos")
        self.city_label.pack(pady=20)

        self.city_label = tk.Label(self, text="Insira o nome de uma cidade abaixo")
        self.city_label.pack(pady=10)

        self.city_name = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.city_name)
        self.entry.pack()

        self.submit_button = tk.Button(self, text="Consultar", command=self.create_table)
        self.submit_button.pack(pady=5)

        self.back_button = tk.Button(self, text="Voltar",
                                     command=lambda: self.master.switch_frame(ReportFrame(self.master)))
        self.back_button.pack(side="bottom", pady=20)

        self.tree = None

    def create_table(self):
        if self.tree is not None:
            self.tree.destroy()

        self.tree = ttk.Treeview(self, show='headings')
        self.tree["columns"] = (
            "Coluna 1", "Coluna 2", "Coluna 3", "Coluna 4", "Coluna 5", "Coluna 6")

        self.tree.column("Coluna 1", width=100)
        self.tree.heading("Coluna 1", text="Cidade pesquisada")

        self.tree.column("Coluna 2", width=100)
        self.tree.heading("Coluna 2", text="Código IATA")

        self.tree.column("Coluna 3", width=300)
        self.tree.heading("Coluna 3", text="Aeroporto")

        self.tree.column("Coluna 4", width=200)
        self.tree.heading("Coluna 4", text="Cidade do Aeroporto")

        self.tree.column("Coluna 5", width=300)
        self.tree.heading("Coluna 5", text="Distância Aeroporto x Cidade pesquisada (km)")

        self.tree.column("Coluna 6", width=150)
        self.tree.heading("Coluna 6", text="Tipo do aeroporto")

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        c.execute(f"SELECT c.name, a.iata_code, a.name, a.city, ROUND(CAST(d.distance as numeric(10, 2)), 2)"
                  f" AS distance,"
                  "CASE "
                  "WHEN type = 'medium_airport' THEN 'Aeroporto médio'"
                  "WHEN type = 'large_airport' THEN 'Aeroporto grande'"
                  "ELSE type"
                  " END AS formatted_column"
                  " FROM airports as a"
                  " JOIN airport_city_distances as d on a.id = d.airport_id"
                  " JOIN geocities15k c on c.geonameid = d.city_id"
                  f" WHERE"
                  " type IN ('medium_airport', 'large_airport')"
                  " AND iso_country = 'BR'"
                  "AND c.name = %s"
                  " ORDER BY distance", (self.city_name.get(), ))

        data = c.fetchall()

        for row in data:
            self.tree.insert('', 'end', values=row)

        self.tree.pack()
