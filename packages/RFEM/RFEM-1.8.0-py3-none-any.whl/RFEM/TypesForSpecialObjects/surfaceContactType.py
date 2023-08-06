from RFEM.initModel import Model, clearAtributes

class SurfaceContactType():
    def __init__(self,
                 no: int = 1,
                 comment: str = '',
                 params: dict = None,
                 model = Model):

        # Client model | Surface Contact Type
        clientObject = model.clientModel.factory.create('ns0:surfaces_contact_type')

        # Clears object atributes | Sets all atributes to None
        clearAtributes(clientObject)

        # Surface Contact Type No.
        clientObject.no = no

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Add Surface Contact Type to client model
        model.clientModel.service.set_surfaces_contact_type(clientObject)
