import tkinter as tk
from tkinter import ttk, messagebox
import csv

class Tournament:
    def __init__(self, id, name, game, date):
        self.id = id
        self.name = name
        self.game = game
        self.date = date
        self.teams = []

    def add_team(self, team):
        if team not in self.teams:
            self.teams.append(team)

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class EsportsManagement:
    def __init__(self):
        self.tournaments = []
        self.teams = []
        self.tournament_ids = set()
        self.team_ids = set()

    def add_tournament(self, tournament):
        if tournament.id in self.tournament_ids:
            return False
        self.tournaments.append(tournament)
        self.tournament_ids.add(tournament.id)
        return True

    def view_tournaments(self):
        return self.tournaments

    def update_tournament(self, id, new_name, new_game, new_date):
        for tournament in self.tournaments:
            if tournament.id == id:
                tournament.name = new_name
                tournament.game = new_game
                tournament.date = new_date
                return True
        return False

    def delete_tournament(self, id):
        for i, tournament in enumerate(self.tournaments):
            if tournament.id == id:
                del self.tournaments[i]
                self.tournament_ids.remove(id)
                return True
        return False

    def sort_tournaments_by_name(self):
        self.tournaments.sort(key=lambda x: x.name)

    def search_tournament_by_name(self, name):
        for tournament in self.tournaments:
            if tournament.name == name:
                return tournament
        return None

    def import_tournaments_from_csv(self, filename):
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    if len(row) >= 5:
                        id, name, game, date, teams_str = row
                        tournament = Tournament(id, name, game, date)
                        team_ids = teams_str.split(';')
                        for team_id in team_ids:
                            if team_id.strip():
                                team_name = team_id.strip()
                                team = Team(team_id, team_name)
                                if team.id not in self.team_ids:  
                                    self.add_team(team)
                                tournament.add_team(team)
                        if tournament.id not in self.tournament_ids:  
                            self.add_tournament(tournament)
                    elif len(row) == 4:
                        id, name, game, date = row
                        tournament = Tournament(id, name, game, date)
                        if tournament.id not in self.tournament_ids:  
                            self.add_tournament(tournament)
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return False
        return True

    def export_tournaments_to_csv(self, filename):
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Game", "Date", "Teams"])
                for tournament in self.tournaments:
                    team_names = ";".join([team.name for team in tournament.teams])
                    writer.writerow([tournament.id, tournament.name, tournament.game, tournament.date, team_names])
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
        return True

    def add_team(self, team):
        if team.id in self.team_ids:
            return False
        self.teams.append(team)
        self.team_ids.add(team.id)
        return True

    def view_teams(self):
        return self.teams

    def search_team_by_name(self, name):
        for team in self.teams:
            if team.name == name:
                return team
        return None

    def add_team_to_tournament(self, tournament_id, team_id):
        tournament = self.search_tournament_by_id(tournament_id)
        team = self.search_team_by_id(team_id)
        if tournament and team:
            tournament.add_team(team)
            return True
        return False

    def search_tournament_by_id(self, id):
        for tournament in self.tournaments:
            if tournament.id == id:
                return tournament
        return None

    def search_team_by_id(self, id):
        for team in self.teams:
            if team.id == id:
                return team
        return None

    def update_team(self, id, new_name):
        for team in self.teams:
            if team.id == id:
                team.name = new_name
                return True
        return False

    def delete_team(self, id):
        for i, team in enumerate(self.teams):
            if team.id == id:
                del self.teams[i]
                self.team_ids.remove(id)
                return True
        return False

class EsportsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Esports Management System")

        self.em = EsportsManagement()

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Data", command=self.export_data)

        self.tabControl = ttk.Notebook(root)
        self.tabTournaments = ttk.Frame(self.tabControl)
        self.tabTeams = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabTournaments, text="Tournaments")
        self.tabControl.add(self.tabTeams, text="Teams")
        self.tabControl.pack(expand=1, fill="both")

        self.create_tournaments_tab()
        self.create_teams_tab()

    def create_tournaments_tab(self):

        self.label_tournament_id = tk.Label(self.tabTournaments, text="ID")
        self.label_tournament_id.grid(column=0, row=0, padx=10, pady=10)
        self.entry_tournament_id = tk.Entry(self.tabTournaments)
        self.entry_tournament_id.grid(column=1, row=0, padx=10, pady=10)

        self.label_tournament_name = tk.Label(self.tabTournaments, text="Name")
        self.label_tournament_name.grid(column=0, row=1, padx=10, pady=10)
        self.entry_tournament_name = tk.Entry(self.tabTournaments)
        self.entry_tournament_name.grid(column=1, row=1, padx=10, pady=10)

        self.label_tournament_game = tk.Label(self.tabTournaments, text="Game")
        self.label_tournament_game.grid(column=0, row=2, padx=10, pady=10)
        self.entry_tournament_game = tk.Entry(self.tabTournaments)
        self.entry_tournament_game.grid(column=1, row=2, padx=10, pady=10)

        self.label_tournament_date = tk.Label(self.tabTournaments, text="Date (YYYY-MM-DD)")
        self.label_tournament_date.grid(column=0, row=3, padx=10, pady=10)
        self.entry_tournament_date = tk.Entry(self.tabTournaments)
        self.entry_tournament_date.grid(column=1, row=3, padx=10, pady=10)

        self.button_add_tournament = tk.Button(self.tabTournaments, text="Add Tournament", command=self.add_tournament)
        self.button_add_tournament.grid(column=0, row=4, padx=10, pady=10)

        self.button_update_tournament = tk.Button(self.tabTournaments, text="Update Tournament", command=self.update_tournament)
        self.button_update_tournament.grid(column=1, row=4, padx=10, pady=10)

        self.button_delete_tournament = tk.Button(self.tabTournaments, text="Delete Tournament", command=self.delete_tournament)
        self.button_delete_tournament.grid(column=0, row=5, padx=10, pady=10)

        self.label_team_id_for_tournament = tk.Label(self.tabTournaments, text="Team ID")
        self.label_team_id_for_tournament.grid(column=0, row=6, padx=10, pady=10)
        self.entry_team_id_for_tournament = tk.Entry(self.tabTournaments)
        self.entry_team_id_for_tournament.grid(column=1, row=6, padx=10, pady=10)

        self.label_tournament_id_for_team = tk.Label(self.tabTournaments, text="Tournament ID")
        self.label_tournament_id_for_team.grid(column=0, row=7, padx=10, pady=10)
        self.entry_tournament_id_for_team = tk.Entry(self.tabTournaments)
        self.entry_tournament_id_for_team.grid(column=1, row=7, padx=10, pady=10)

        self.button_add_team_to_tournament = tk.Button(self.tabTournaments, text="Add Team to Tournament", command=self.add_team_to_tournament)
        self.button_add_team_to_tournament.grid(column=0, row=8, padx=10, pady=10, columnspan=2)

        self.tournament_list = tk.Listbox(self.tabTournaments)
        self.tournament_list.grid(column=0, row=9, padx=10, pady=10, columnspan=2)
        self.tournament_list.bind("<<ListboxSelect>>", self.show_tournament_detail)
        self.update_tournament_list()

    def create_teams_tab(self):

        self.label_team_id = tk.Label(self.tabTeams, text="ID")
        self.label_team_id.grid(column=0, row=0, padx=10, pady=10)
        self.entry_team_id = tk.Entry(self.tabTeams)
        self.entry_team_id.grid(column=1, row=0, padx=10, pady=10)

        self.label_team_name = tk.Label(self.tabTeams, text="Name")
        self.label_team_name.grid(column=0, row=1, padx=10, pady=10)
        self.entry_team_name = tk.Entry(self.tabTeams)
        self.entry_team_name.grid(column=1, row=1, padx=10, pady=10)

        self.button_add_team = tk.Button(self.tabTeams, text="Add Team", command=self.add_team)
        self.button_add_team.grid(column=0, row=2, padx=10, pady=10)

        self.button_update_team = tk.Button(self.tabTeams, text="Update Team", command=self.update_team)
        self.button_update_team.grid(column=1, row=2, padx=10, pady=10)

        self.button_delete_team = tk.Button(self.tabTeams, text="Delete Team", command=self.delete_team)
        self.button_delete_team.grid(column=0, row=3, padx=10, pady=10)

        self.team_list = tk.Listbox(self.tabTeams)
        self.team_list.grid(column=0, row=4, padx=10, pady=10, columnspan=2)
        self.team_list.bind("<<ListboxSelect>>", self.show_team_detail)
        self.update_team_list()

    def add_tournament(self):
        id = self.entry_tournament_id.get()
        name = self.entry_tournament_name.get()
        game = self.entry_tournament_game.get()
        date = self.entry_tournament_date.get()

        if id in self.em.tournament_ids:
            messagebox.showerror("Error", f"Tournament with ID '{id}' already exists.")
            return

        tournament = Tournament(id, name, game, date)
        self.em.add_tournament(tournament)
        self.update_tournament_list()

    def update_tournament(self):
        id = self.entry_tournament_id.get()
        new_name = self.entry_tournament_name.get()
        new_game = self.entry_tournament_game.get()
        new_date = self.entry_tournament_date.get()

        if self.em.update_tournament(id, new_name, new_game, new_date):
            messagebox.showinfo("Success", "Tournament updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update tournament.")
        self.update_tournament_list()

    def delete_tournament(self):
        selection = self.tournament_list.curselection()
        if selection:
            index = selection[0]
            tournament_id = self.tournament_list.get(index).split(" - ")[0]

            if self.em.delete_tournament(tournament_id):
                messagebox.showinfo("Success", "Tournament deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete tournament.")
            self.update_tournament_list()
        else:
            messagebox.showerror("Error", "Please select a tournament to delete.")

    def add_team_to_tournament(self):
        team_id = self.entry_team_id_for_tournament.get()
        tournament_id = self.entry_tournament_id_for_team.get()

        if self.em.add_team_to_tournament(tournament_id, team_id):
            messagebox.showinfo("Success", "Team added to tournament successfully.")
        else:
            messagebox.showerror("Error", "Failed to add team to tournament.")

        self.update_tournament_list()

    def add_team(self):
        id = self.entry_team_id.get()
        name = self.entry_team_name.get()

        if id in self.em.team_ids:
            messagebox.showerror("Error", f"Team with ID '{id}' already exists.")
            return

        team = Team(id, name)
        self.em.add_team(team)
        self.update_team_list()

    def update_team(self):
        id = self.entry_team_id.get()
        new_name = self.entry_team_name.get()

        if self.em.update_team(id, new_name):
            messagebox.showinfo("Success", "Team updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update team.")
        self.update_team_list()

    def delete_team(self):
        selection = self.team_list.curselection()
        if selection:
            index = selection[0]
            team_id = self.team_list.get(index).split(" - ")[0]

            if self.em.delete_team(team_id):
                messagebox.showinfo("Success", "Team deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete team.")
            self.update_team_list()
        else:
            messagebox.showerror("Error", "Please select a team to delete.")

    def update_tournament_list(self):
        self.tournament_list.delete(0, tk.END)
        for tournament in self.em.view_tournaments():
            team_names = ", ".join([team.name for team in tournament.teams])
            self.tournament_list.insert(tk.END, f"{tournament.id} - {tournament.name} ({tournament.game}) on {tournament.date} - Teams: {team_names}")

    def update_team_list(self):
        self.team_list.delete(0, tk.END)
        for team in self.em.view_teams():
            self.team_list.insert(tk.END, f"{team.id} - {team.name}")

    def import_data(self):
        filename = "tournament.csv" 
        if self.em.import_tournaments_from_csv(filename):
            messagebox.showinfo("Success", "Tournaments imported successfully.")
        else:
            messagebox.showerror("Error", "Failed to import tournaments.")
        self.update_tournament_list()
        self.update_team_list()

    def export_data(self):
        filename = "tournament.csv"
        if self.em.export_tournaments_to_csv(filename):
            messagebox.showinfo("Success", "Tournaments exported successfully.")
        else:
            messagebox.showerror("Error", "Failed to export tournaments.")

    def show_tournament_detail(self, event):
        selection = self.tournament_list.curselection()
        if selection:
            index = selection[0]
            tournament_id = self.tournament_list.get(index).split(" - ")[0]
            tournament = self.em.search_tournament_by_id(tournament_id)
            if tournament:
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Tournament Details - {tournament.name}")

                tk.Label(detail_window, text=f"Name: {tournament.name}").pack()
                tk.Label(detail_window, text=f"Game: {tournament.game}").pack()
                tk.Label(detail_window, text=f"Date: {tournament.date}").pack()

                tk.Label(detail_window, text="Teams:").pack()
                team_list_box = tk.Listbox(detail_window)
                for team in tournament.teams:
                    team_list_box.insert(tk.END, f"{team.id} - {team.name}")
                team_list_box.pack()

    def show_team_detail(self, event):
        selection = self.team_list.curselection()
        if selection:
            index = selection[0]
            team_id = self.team_list.get(index).split(" - ")[0]
            team = self.em.search_team_by_id(team_id)
            if team:
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Team Details - {team.name}")

                tk.Label(detail_window, text=f"Name: {team.name}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = EsportsGUI(root)
    root.mainloop()