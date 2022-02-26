from main import read_metadata

def test_read_metadata():
    metadata = read_metadata('metadata.xlsx')
    assert(len(metadata.index)) == 63
    print("read_metadata test - Passed")

def main():
    test_read_metadata()

if __name__ == '__main__':
    main()




