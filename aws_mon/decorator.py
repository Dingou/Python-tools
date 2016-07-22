def flyable(message):
    def flyable_to_return(cls):
        def fly(self):
            print(message)
        cls.fly = fly
        
        return cls
    return flyable_to_return