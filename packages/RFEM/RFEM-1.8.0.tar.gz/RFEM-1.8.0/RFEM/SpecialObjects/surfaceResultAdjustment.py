from RFEM.initModel import Model, clearAtributes

class SurfaceResultsAdjustment():
    def __init__(self,
                 no: int = 1,
                 comment: str = '',
                 params: dict = None,
                 model = Model):

        # Client model | Surface Result Adjustment
        clientObject = model.clientModel.factory.create('ns0:surface_results_adjustment')

        # Clears object atributes | Sets all atributes to None
        clearAtributes(clientObject)

        # Surface Result Adjustment No.
        clientObject.no = no

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Add Surface Result Adjustmentto client model
        model.clientModel.service.set_surface_results_adjustment(clientObject)
