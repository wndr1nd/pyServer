class AbstractMessage:
    def __init__(self, data):
        self.devid = data.get('devid')
        self.temperature = data.get('temperature')
        self.humidity = data.get('humidity')

    def __str__(self):
        return f'Data: Deviceid {self.devid}. Temperature {self.temperature}. Humidity {self.humidity}%.'


class DataMessage(AbstractMessage):
    def __init__(self, data):
        super().__init__(data)


