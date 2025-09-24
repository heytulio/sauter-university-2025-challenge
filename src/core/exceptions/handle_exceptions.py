class DataPipelineError(Exception): 
    """Classe base para exceções nesta aplicação.""" 
    pass 

class ONSApiError(DataPipelineError): 
    """Lançada quando há um erro na comunicação com a API do ONS.""" 
    pass
 
class GCSAdapterError(DataPipelineError): 
    """Lançada quando ocorre um erro no adaptador do Google Cloud Storage.""" 
    pass

class BQAdapterError(DataPipelineError): 
    """Lançada quando ocorre um erro no adaptador do BigQuery.""" 
    pass

class BQServiceError(DataPipelineError): 
    """Lançada quando ocorre um erro no serviço do BigQuery.""" 
    pass

