import pandas as pd

from snelstart.core import Base


class SnelStart(Base):
    def __init__(self):
        super().__init__()

    def artikelen(self):
        data = self.request_data(endpoint="artikelen")
        df = pd.DataFrame(data)

        return df

    def grootboekmutaties(self):
        data = self.request_data(endpoint="grootboekmutaties")
        df = pd.DataFrame(data)

        return df

    def dagboeken(self):
        data = self.request_data(endpoint="dagboeken")
        df = pd.DataFrame(data)

        return df

    def grootboeken(self):
        data = self.request_data(endpoint="grootboeken")
        df = pd.DataFrame(data)

        return df
