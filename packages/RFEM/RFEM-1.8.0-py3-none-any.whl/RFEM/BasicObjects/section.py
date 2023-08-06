from RFEM.initModel import Model, clearAtributes

class Section():
    def __init__(self,
                 no: int = 1,
                 name: str = 'IPE 300',
                 material_no: int = 1,
                 comment: str = '',
                 params: dict = None,
                 model = Model):

        '''
        Args:
            no (int): Section Tag
            name (str): Name of Desired Section (As Named in RFEM Database)
            material_no (int): Tag of Material assigned to Section
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
        '''

        # Client model | Section
        clientObject = model.clientModel.factory.create('ns0:section')

        # Clears object atributes | Sets all atributes to None
        clearAtributes(clientObject)

        # Section No.
        clientObject.no = no

        # Section nNme
        clientObject.name = name

        # Material No.
        clientObject.material = material_no

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Add Section to client model
        model.clientModel.service.set_section(clientObject)
