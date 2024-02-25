class Education:
    def __init__(self,
                 id: int,
                 name: str,
                 entity: str = None,
                 time: str = None
                 ) -> None:
        self.id = id
        self.name = name
        self.entity = entity
        self.time = time
