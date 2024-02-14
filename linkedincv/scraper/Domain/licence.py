class License:
    def __init__(self,
                 name: str,
                 emitted_by: str = None,
                 expedition: str = None
                 ) -> None:
        self.name = name
        self.emitted_by = emitted_by
        self.expedition = expedition
