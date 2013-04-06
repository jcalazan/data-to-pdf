from operator import itemgetter

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle

class DataToPdf():
    """
    Export a list of dictionaries to a table in a PDF file.
    """
    
    def __init__(self, fields, data, sort_by=None, title=None):
        """
        Arguments:
            fields - A tuple of tuples ((fieldname/key, display_name)) 
                specifying the fieldname/key and corresponding display
                name for the table header.
            data - The data to insert to the table formatted as a list of
                dictionaries.
            sort_by - A tuple (sort_key, sort_order) specifying which field
                to sort by and the sort order ('ASC', 'DESC').
            title - The title to display at the beginning of the document.
        """
        self.fields = fields
        self.data = data
        self.title = title
        self.sort_by = sort_by
        
    def export(self, filename, data_align='LEFT', table_halign='LEFT'):
        """
        Export the data to a PDF file.
        
        Arguments:
            filename - The filename for the generated PDF file.
            data_align - The alignment of the data inside the table (eg.
                'LEFT', 'CENTER', 'RIGHT')
            table_halign - Horizontal alignment of the table on the page
                (eg. 'LEFT', 'CENTER', 'RIGHT')
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        styles = getSampleStyleSheet()
        styleH = styles['Heading1']
        
        story = []

        if self.title:
            story.append(Paragraph(self.title, styleH))
            story.append(Spacer(1, 0.25 * inch))
            
        if self.sort_by:
            reverse_order = False
            if (str(self.sort_by[1]).upper() == 'DESC'):
                reverse_order = True

            self.data = sorted(self.data,
                               key=itemgetter(self.sort_by[0]),
                               reverse=reverse_order)

        converted_data = self.__convert_data()
        table = Table(converted_data, hAlign=table_halign)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN',(0, 0),(0,-1), data_align),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        
        story.append(table)
        doc.build(story)

    def __convert_data(self):
        """
        Convert the list of dictionaries to a list of list to create
        the PDF table.
        """
        # Create 2 separate lists in the same order: one for the 
        # list of keys and the other for the names to display in the
        # table header.
        keys, names = zip(*[[k, n] for k, n in self.fields])
        new_data = [names]
        
        for d in self.data:
            new_data.append([d[k] for k in keys])
            
        return new_data