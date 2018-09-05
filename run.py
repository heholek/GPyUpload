import main
from src.models.JuryAppointment import JuryAppointment
from src.models.StudentResponse import StudentResponse

if __name__ == "__main__":
    app = main.App()
    app.setModels([JuryAppointment, StudentResponse])
    app.register_classes()
    app.importData(exclusions=['MainSheet'],
                   models=[JuryAppointment, StudentResponse])
    app.filemanager.exportModels(JuryAppointment)
    app.filemanager.exportModels(StudentResponse)
    app.filemanager.joinModels()
    app.buildReports(JuryAppointment)
