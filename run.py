import main
from src.models.JuryAppointment import JuryAppointment

if __name__ == "__main__":
    app = main.App()
    app.setModels([JuryAppointment])
    app.register_classes()
    app.importData(exclusions=['MainSheet',
                               'StudentResponses'],
                   models=[JuryAppointment])
    app.filemanager.exportModels(JuryAppointment)
    app.buildReports(JuryAppointment)
