import requests
import time

class Advice:
    def __init__(self, slip):
        slip = slip.json()
        self.id = slip["slip"]["id"]
        self.advice = slip["slip"]["advice"]

    def __str__(self):
        return f"The advice with id {self.id}:\n{self.advice}"


class Slip:
    def __init__(self):
        self.url = "https://api.adviceslip.com/advice"
        self.advices = []

    def get_new_advice(self):
        resp = requests.get(self.url)
        adv = Advice(resp)
        self.advices.append(adv)
        return adv

    def print_advices(self):
        for advice in self.advices:
            print(advice)
            print("="*40)


def main():
    slip = Slip()
    for i in range(4):
        slip.get_new_advice()
        print(f"Got advice {i+1}")
        time.sleep(10)

    print("Done")
    slip.print_advices()


if __name__ == '__main__':
    main()
