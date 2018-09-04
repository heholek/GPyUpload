from jinja2 import Environment, FileSystemLoader
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class ReportBuilder():
    """
    Creates a pdf when .buildReport() is called and passed a record object

    On building and initializing the ReportBuilder, certain defaults are set
    """

    def __init__(self, model, group):
        """
        Set Options
        """
        for key, value in group.items():
            self.meta = value
            self.group_name = key
            self.group = model.get_report_group(key)
            self.group.sort()
            self.type = model.REPORT_TYPE
            self.template_name = model.TEMPLATE_NAME
            self.environment = Environment(
                                loader=FileSystemLoader(THIS_DIR + '/templates/TEX/'),
                                trim_blocks=True,
                                block_start_string = '\BLOCK{',
                                block_end_string = '}',
                                variable_start_string = '\VAR{',
                                variable_end_string = '}',
                                comment_start_string = '\#{',
                                comment_end_string = '}',
                                line_statement_prefix = '%%',
                                line_comment_prefix = '%#',
                                autoescape = False,
                               )

    def buildReport(self):
        """
        Receives a report object and parses into the appropriate template
        """
        name = self.group_name
        _file = open('build/' + name + 'report.tex', 'w+')
        _file.write(self.environment.get_template(self.template_name).render(meta=self.meta, records=self.group))
        _file.close()

    def run(self):
        self.buildReport()

print("Successfully loaded ReportBuilder")
