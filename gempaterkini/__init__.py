import bs4
import requests

description = '\nLatest Information Eartquake in Indonesia from BMKG\n'

class GempaTerkini:
    def __init__(self, url):
        self.result = None
        self.description = description
        self.url = url

    def extract_data(self):
        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            soup = bs4.BeautifulSoup(content.text, 'html.parser')

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')

            i = 0
            date = None
            hours = None
            magnitude = None
            depth = None
            lu = None
            bt = None
            location = None
            felt = None

            for res in result:
                if i == 0:
                    time = res.text.split(', ')
                    date = time[0]
                    hours = time[1]
                elif i == 1:
                    magnitude = res.text
                elif i == 2:
                    depth = res.text
                elif i == 3:
                    coordinate = res.text.split(' - ')
                    lu = coordinate[0]
                    bt = coordinate[1]
                elif i == 4:
                    location = res.text
                elif i == 5:
                    felt = res.text

                i = i + 1

            data = dict()
            data['time'] = {'date': date, 'hours': hours}
            data['magnitude'] = magnitude
            data['depth'] = depth
            data['coordinate'] = {'lu': lu, 'bt': bt}
            data['location'] = location
            data['felt'] = felt
            self.result = data
        else:
            return None

    def show_data(self):
        if self.result is None:
            print('Data not found')
            return

        print(self.description)
        print(f"Date : {self.result['time']['date']}")
        print(f"Hours : {self.result['time']['hours']}")
        print(f"Magnitude : {self.result['magnitude']}")
        print(f"Depth : {self.result['depth']}")
        print(f"Coordinate : {self.result['coordinate']['lu']}, {self.result['coordinate']['bt']}")
        print(f"Location : {self.result['location']}")
        print(f"{self.result['felt']}")

    def run(self):
        self.extract_data()
        self.show_data()


if __name__ == '__main__':
    gempa = GempaTerkini('https://www.bmkg.go.id/')
    gempa.run()
