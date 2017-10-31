from nbi.DataStore import ErdaShare, IDMCShare, ErdaHome


def share_links_example():

    ### Sharelinks lib Tutorial ###

    # ERDA Sharelink example
    print("ERDA")
    # Open connection to a sharelink
    erda_share = ErdaShare('jg6pkLQJse')
    # List files/dirs in share
    print(erda_share.list())
    # Read file directly as string
    print(erda_share.read('tmp'))
    # Read file directly as binary
    print(erda_share.read_binary('tmp'))

    # Get a _io.TextIOWrapper object with automatic close
    with erda_share.open('tmp', 'r') as tmp:
        print(tmp.read())

    # Get a default _io.TextIOWrapper object with manual lifetime
    file = erda_share.open('tmp', 'r')
    print(file.read())
    file.close()

    print("\n")

    # IDMC Sharelink example
    print("IDMC")
    # Open connection to a sharelink
    idmc_share = IDMCShare('KGDlunrM3w')
    # List files/dirs in share
    print(idmc_share.list())
    # Read file directly as string
    print(idmc_share.read('fisk'))
    # Read file directly as binary
    print(idmc_share.read_binary('fisk'))
    # Get a _io.TextIOWrapper object with automatic close
    with idmc_share.open('fisk', 'r') as tmp:
        print(tmp.read())

    # Get a default _io.TextIOWrapper object with manual lifetime
    file = idmc_share.open('fisk', 'r')
    print(file.read())
    file.close()


def home_example():
    ### Erda Home example ###
    home = ErdaHome("username", "password")
    print(home.list())
    print(home.read('welcome.txt'))
    print(home.list('shared_folder'))
    print(home.read('shared_folder/tmp'))


if __name__ == "__main__":
    share_links_example()
    #home_example()


