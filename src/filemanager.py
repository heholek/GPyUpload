#filemanager.py

from .db.db import create_db, connect_db

class FileManager():

    def __init__(self, app, db_path, classes):
        self.app = app
        self.model_groups = {}
        self.models = {}
        self.db_path = db_path
        self.classes = classes
        self.dbsession = create_db(self.db_path, self.classes)

    def buildModel(self, model):
        model_objects = []
        self.model_groups[model.__name__] = []
        for key, item in self.app().importer.sheets.items():
            group = key
            meta = {}
            temp = [fields[0] for fields in item.items()]
            for field in temp:
                if field != 'records':
                    meta[field] = item[field]
            for record in item['records']:
                model_objects.append(model(meta=meta, record_group=group, **record))
            self.model_groups[model.__name__].append({group: meta})
            self.models[model.__name__] = model_objects

    def exportModels(self, model):
        """
        Adds all models to database
        """
        s = self.dbsession()
        for i in self.models[model.__name__]:
            temp = {}
            for j in i.__slots__:
                if j == 'datetime':
                    temp[j] = getattr(i,j)
                elif j != '__weakref__':
                    temp[j] = str(getattr(i,j))
            ormobject = model.ormobject(**temp)
            s.add(ormobject)
        s.commit()
