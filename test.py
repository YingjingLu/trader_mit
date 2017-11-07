# run any test experiments
class Try:

    @staticmethod
    def print_fuck(x):
        print("fuck", x)
        return x

    @staticmethod
    def sayhi(y):
        print("say hi", y)
        x = Try.print_fuck(y-1)
        print(y)
        return x+y


def main():

    x = Try.print_fuck(4)
    print("pass here")
    y = Try.sayhi(5)

if __name__ == "__main__":
    main()

