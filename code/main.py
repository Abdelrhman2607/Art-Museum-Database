import mysql.connector
import os
import shutil

class Program:
    def __init__(self):
        self.running = True
        self.create_connection()
        self.cur = self.cnx.cursor()
        self.execute_sql_file(f"sql{'\\' if os.name == "nt" else '/'}db_init.sql")

        self.get_tables() #create table_count and table_names {"1": "table_name", "2": "table_name", etc.}
        self.get_table_attrs() #create table_attrs dictionary of lists {"table-name": ["attr1", "attr2", etc.]}
        self.get_primary_keys() #create pk_columns dictionary of lists {"table_name": [pk1, pk2, etc.]} 

        self.user_role = self.prompt_role()
        if self.user_role == 0:
            self.running = False
            print("Exiting Program")
        
    def create_connection(self):
        username = input("Please enter mysql server username: ")
        password = input("Please enter mysql server password: ")

        try:
            self.cnx = mysql.connector.connect(
                host="localhost",
                port=3306,
                user=username,
                password= password)

            print("Connected to server succesfully")
            return

        except mysql.connector.Error as err:
                print(f"Error encountered while connecting: {err}")
                exit(1)
    
    def execute_sql_file(self, file_name):
        with open(file_name, "r") as FILE:
            DB = FILE.read()

            commands = DB.split(';')

        for command in commands:
            try:
                if command.strip() != "":
                    self.cur.execute(command)

            except mysql.connector.Error as err:
                print(f"Command skipped: {err}")

        print("MySQL Database succesfully loaded")
        print()
    
    def display_query_result(self, query):
        self.cur.execute(query)
        cols = self.cur.column_names
        results = self.cur.fetchall()
        
        # Calculate column widths based on content
        col_widths = []
        for i, col_name in enumerate(cols):
            width = len(str(col_name))
            for row in results:
                if row[i] is not None:
                    width = max(width, len(str(row[i])))
            col_widths.append(max(width, 10))
        
        # Get terminal width, default to 120 if unavailable
        try:
            terminal_width = shutil.get_terminal_size().columns
        except:
            terminal_width = 120
        
        # Group columns into rows that fit
        column_groups = []
        current_group = []
        current_width = 0
        
        for i, width in enumerate(col_widths):
            # Calculate total width if we add this column
            num_cols = len(current_group) + 1
            separator_overhead = 3 * num_cols + 1
            total_width = current_width + width + separator_overhead
            
            if total_width <= terminal_width or len(current_group) == 0:
                current_group.append(i)
                current_width += width
            else:
                column_groups.append(current_group)
                current_group = [i]
                current_width = width
        
        if current_group:
            column_groups.append(current_group)
        
        print()
        
        # Display table with column wrapping
        for group_idx, col_group in enumerate(column_groups):
            
            # Print header
            header_row = "|"
            separator_row = "|"
            for col_idx in col_group:
                header_row += f" {str(cols[col_idx]):<{col_widths[col_idx]}} |"
                separator_row += "-" * (col_widths[col_idx] + 2) + "|"
            
            print(separator_row)
            print(header_row)
            print(separator_row)
            
            # Print data rows
            if not results:
                # Calculate total table width: sum of column widths + separators
                total_table_width = sum(col_widths[i] for i in col_group) + len(col_group) * 3 + 1
                message_width = total_table_width - 4  # Subtract "| " and " |"
                print(f"| {'':^{message_width}} |")
                print(f"| {'No results found':^{message_width}} |")
                print(f"| {'':^{message_width}} |")
            else:
                for row in results:
                    data_row = "|"
                    for col_idx in col_group:
                        val = str(row[col_idx]) if row[col_idx] is not None else "NULL"
                        data_row += f" {val:<{col_widths[col_idx]}} |"
                    print(data_row)
            
            print(separator_row)
            print()
        
        self.prompt_enter()

    def get_tables(self):
        self.cur.execute("SHOW TABLES")
        tables = self.cur.fetchall()
        self.table_count = len(tables)
        self.table_names = {}

        for i in range(1, self.table_count + 1):
            self.table_names[str(i)] = tables[i-1][0]
    
    def get_table_attrs(self):
        self.table_attrs = {}
        for table in self.table_names.values():
            self.cur.execute(f"SHOW COLUMNS FROM `{table.upper()}`")
            cols = self.cur.fetchall()
            num_cols = len(cols)

            self.table_attrs[table] = [cols[i-1][0] for i in range(1, num_cols + 1)]
    
    def get_primary_keys(self):
        self.pk_columns = {}
        for table in self.table_names.values():
            self.cur.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
            self.pk_columns[table] = [row[4] for row in self.cur.fetchall()]

    def clear_terminal(self):
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS/Linux
        else:
            os.system('clear')

    def prompt_role(self):
        print("Select your role to continue: ")
        print("1. Visitor")
        print("2. Employee")
        print("0. Exit")
        return self.prompt_numbered(2, self.prompt_role)

    def prompt_enter(self):
        print()
        print('-' * 20, "Press Enter to continue", '-' * 20)
        input()
        print()

    def print_separator(self, length=20):
        print()
        print('=' * length)
        print()

    def prompt_numbered(self, option_limit, caller):
        try:
            user_input = int(input(f"Select an option from 1 to {option_limit} (0 to exit): "))
            self.print_separator(40)
        except ValueError:
            print(f"Invalid option, please select a number from 0 to {option_limit}")
            self.print_separator(40)
            return caller()
        if user_input in range(0, option_limit + 1):
            return user_input
        else:
            print(f"Invalid option, please select a number from 0 to {option_limit}")
            self.print_separator(40)
            return caller()

    def prompt_action(self):
        print("Select the action you would like to do: ")
        print("1. Insert data into a table")
        print("2. Update data in a table")
        print("3. Delete data from a table")
        print("4. Look up data from a table")
        print("0. Exit")

        input_result = self.prompt_numbered(4, self.prompt_action)
        return input_result
      
    def prompt_tables(self):
        while True:
            print(f"Select the table you would like to access: ")

            for i in range(1, self.table_count + 1):
                print(f"{i}. {self.table_names[str(i)].title()}")
            print("0. Exit")

            input_result = self.prompt_numbered(self.table_count, self.prompt_tables)
            return input_result

    def handle_sql_err(self, err_code):
        self.clear_terminal()
        print("Error encountered with entered values: ")
        match err_code:
            case 1064:     
                print("Make sure values are of the correct data type")
            case 1062:
                print("Duplicate ID value entered, IDs must be unique")
            case 1452:
                print("Make sure Foreign keys correctly reference an existing Primary key")
            case _:
                print("Unknown Error") 

        self.print_separator(40)    

    def table_insert(self, table_name):
        query_string = f"INSERT INTO {table_name.upper()}("
        for attr in self.table_attrs[table_name]:
            query_string += f"{attr}, "

        query_string = query_string[:-2]
        query_string += ") VALUES("

        attrs = self.prompt_table_attrs(table_name)
        for value in attrs.values():
            query_string += f"'{value}', "

        query_string = query_string[:-2]
        query_string += ')'
        
        try:
            self.cur.execute(query_string)
            self.cnx.commit()
            self.display_query_result(f"SELECT * FROM {table_name}")
        except mysql.connector.Error as err:
                self.handle_sql_err(err.errno)
                
    def table_update(self,table_name):
        search_key = input(f"Input value of {self.pk_columns[table_name][0]} for row to be updated: ")

        query_string = f"UPDATE `{table_name.upper()}` SET "

        attrs = self.prompt_table_attrs(table_name)
        for key, value in zip(attrs.keys(), attrs.values()):
            query_string += f"`{key}` = '{value}', "

        query_string = query_string[:-2]

        query_string += f" WHERE {self.pk_columns[table_name][0]} = \"{search_key}\""
        
        try:
            self.cur.execute(query_string)
            self.cnx.commit()
            self.display_query_result(f"SELECT * FROM {table_name}")
        except mysql.connector.Error as err:
                self.handle_sql_err(err.errno)

    def table_delete(self, table_name):
        search_key = input(f"Input value of {self.pk_columns[table_name][0]} for row to be deleted: ")
        query_string = f"DELETE FROM `{table_name.upper()}` WHERE {self.pk_columns[table_name][0]} = \"{search_key}\""

        try:
            self.cur.execute(query_string)
            self.cnx.commit()
            self.display_query_result(f"SELECT * FROM {table_name}")
        except mysql.connector.Error as err:
                self.handle_sql_err(err.errno)
   
    def table_select(self, table_name):
        self.display_query_result(f"SELECT * FROM {table_name}")

    def prompt_table_attrs(self, table_name):
        attrs = {}
        for attr in self.table_attrs[table_name]:
            attrs[attr] = input(f"Input value for {attr} column: ")

        return attrs

    def prompt_visitor_menu(self):
        print("What would you like to view?")
        print("1. Art pieces")
        print("2. Artists")
        print("3. Exhibitions")
        return self.prompt_numbered(3, self.prompt_visitor_menu)

    def prompt_art_pieces(self):
        print("Which art pieces would you like to view?")
        print("1. All art pieces")
        print("2. Art pieces by style")
        print("3. Art pieces by artist")
        return self.prompt_numbered(3, self.prompt_art_pieces)
    
    def prompt_artists(self):
        print("Which artists would you like to view?")
        print("1. All artists")
        print("2. Artists by country/culture")
        print("3. Artists by epoch")
        return self.prompt_numbered(3, self.prompt_artists)

    def prompt_exhibitions(self):
        print("Which exhibitions would you like to view?")
        print("1. All exhibitions")
        print("2. Current exhibitions")
        return self.prompt_numbered(2, self.prompt_exhibitions)
    
    def prompt_from_query(self, prompt_message, query):
        print(prompt_message)
        self.cur.execute(query)
        results = self.cur.fetchall()
        for i, result in enumerate(results):
            print(f"{i+1}. {result[0]}")
        while True:
            try:
                user_input = int(input(f"Select an option from 1 to {len(results)} (0 to exit): "))
                self.print_separator(40)
                if user_input == 0:
                    return None
                if user_input in range(1, len(results) + 1):
                    return results[user_input-1][0]
                else:
                    print(f"Invalid option, please select a number from 0 to {len(results)}")
                    self.print_separator(40)
            except ValueError:
                print(f"Invalid option, please select a number from 0 to {len(results)}")
                self.print_separator(40)
    
    def prompt_art_style(self):
        return self.prompt_from_query(
            "Which style would you like to view?",
            "SELECT DISTINCT Style FROM ART_OBJECT"
        )
    
    def prompt_art_artist(self):
        return self.prompt_from_query(
            "Which artist would you like to view?",
            "SELECT DISTINCT Artist FROM ART_OBJECT"
        )
    
    def prompt_artist_country(self):
        return self.prompt_from_query(
            "Which country/culture would you like to view?",
            "SELECT DISTINCT CountryCulture FROM ARTIST"
        )
    
    def prompt_artist_epoch(self):
        return self.prompt_from_query(
            "Which epoch would you like to view?",
            "SELECT DISTINCT Epoch FROM ARTIST"
        )

    def run_visitor(self):
        while self.running:
            menu_choice = self.prompt_visitor_menu()
            if menu_choice == 0:
                self.running = False
                print("Exiting Program")
                continue

            elif menu_choice == 1:
                selection = self.prompt_art_pieces()
                if selection == 1:
                    self.display_query_result("""
                        SELECT 
                            AO.Title,
                            AO.Year,
                            AO.Description,
                            AO.Style,
                            AO.Artist,
                            A.Epoch AS ArtistEpoch,
                            A.CountryCulture AS ArtistCountry
                        FROM ART_OBJECT AO
                        JOIN ARTIST A ON AO.Artist = A.Name
                        ORDER BY AO.Year DESC;
                    """)

                elif selection == 2:
                    style = self.prompt_art_style()
                    self.display_query_result(f"""
                        SELECT 
                            AO.Title,
                            AO.Year,
                            AO.Description,
                            AO.Style,
                            AO.Artist,
                            A.Epoch AS ArtistEpoch,
                            A.CountryCulture AS ArtistCountry
                        FROM ART_OBJECT AO
                        JOIN ARTIST A ON AO.Artist = A.Name
                        WHERE AO.Style = '{style}'
                        ORDER BY AO.Year DESC;
                    """)

                elif selection == 3:
                    artist = self.prompt_art_artist()
                    self.display_query_result(f"""
                        SELECT 
                            AO.Title,
                            AO.Year,
                            AO.Description,
                            AO.Style,
                            AO.Artist,
                            A.Epoch AS ArtistEpoch,
                            A.CountryCulture AS ArtistCountry
                        FROM ART_OBJECT AO
                        JOIN ARTIST A ON AO.Artist = A.Name
                        WHERE AO.Artist = '{artist}'
                        ORDER BY AO.Year DESC;
                    """)

                elif selection == 0:
                    self.running = False
                    print("Exiting Program")
                    continue

            elif menu_choice == 2:
                selection = self.prompt_artists()
                if selection == 1:
                    self.display_query_result("""
                        SELECT 
                            A.Name AS ArtistName,
                            A.MainStyle,
                            A.Epoch,
                            A.CountryCulture
                        FROM ARTIST A
                        ORDER BY A.Name;
                    """)
                elif selection == 2:
                    country = self.prompt_artist_country()
                    self.display_query_result(f"""
                        SELECT 
                            A.Name AS ArtistName,
                            A.MainStyle,
                            A.Epoch,
                            A.CountryCulture
                        FROM ARTIST A
                        WHERE A.CountryCulture = '{country}'
                        ORDER BY A.Name;
                    """)
                elif selection == 3:
                    epoch = self.prompt_artist_epoch()
                    self.display_query_result(f"""
                        SELECT 
                            A.Name AS ArtistName,
                            A.MainStyle,
                            A.Epoch,
                            A.CountryCulture
                        FROM ARTIST A
                        WHERE A.Epoch = '{epoch}'
                        ORDER BY A.Name;
                    """)
                elif selection == 0:
                    self.running = False
                    print("Exiting Program")
                    continue

            elif menu_choice == 3:
                selection = self.prompt_exhibitions()
                if selection == 1:
                    self.display_query_result("""
                        SELECT 
                            OD.ExhibitionName,
                            OD.StartDate,
                            OD.EndDate,
                            COUNT(*) AS PiecesOnDisplay
                        FROM ON_DISPLAY OD
                        JOIN ART_OBJECT AO ON OD.Object = AO.ID
                        GROUP BY OD.ExhibitionName, OD.StartDate, OD.EndDate
                        ORDER BY OD.StartDate;
                    """)

                elif selection == 2:
                    self.display_query_result("""
                        SELECT 
                            OD.ExhibitionName,
                            OD.StartDate,
                            OD.EndDate,
                            COUNT(*) AS PiecesOnDisplay
                        FROM ON_DISPLAY OD
                        JOIN ART_OBJECT AO ON OD.Object = AO.ID
                        WHERE OD.StartDate <= CURDATE() AND OD.EndDate >= CURDATE()
                        GROUP BY OD.ExhibitionName, OD.StartDate, OD.EndDate
                        ORDER BY OD.StartDate;
                    """)
                    
                elif selection == 0:
                    self.running = False
                    print("Exiting Program")
                    continue
    
    def run_entry(self):
        while self.running:
            self.user_action = self.prompt_action()
            if self.user_action == 0:
                self.running = False
                print("Exiting Program")
                continue
                            
            self.user_table_index = self.prompt_tables()
            if self.user_table_index == 0:
                self.running = False
                print("Exiting Program")
                continue
            else:
                self.user_table_name = self.table_names[str(self.user_table_index)]
            
            match self.user_action:
                case 1:
                    self.table_insert(self.user_table_name)
                case 2:
                    self.table_update(self.user_table_name)
                case 3:
                    self.table_delete(self.user_table_name)
                case 4:
                    self.table_select(self.user_table_name)



if __name__ == "__main__":
    prog = Program()
    while prog.running:
        if prog.user_role == 1:
            prog.run_visitor()
        elif prog.user_role == 2:
            prog.run_entry()