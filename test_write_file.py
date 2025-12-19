from functions.write_file import write_file

def test():
    print("Result for writing to lorem.txt file:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("")

    print("Result for writing to pkg/morelorem.txt file:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("")

    print("Result for writing to /tmp/temp.txt file:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print("")

if __name__ == "__main__":
    test()