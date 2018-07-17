import main

if __name__ == "__main__":
    app = main.App()
    app.register_classes()
    app.importData()
    app.importer.load_files()
    app.importer.load_spreadsheets()
    app.importer.load_spreadsheet_values()
