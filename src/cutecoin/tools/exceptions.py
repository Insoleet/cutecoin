'''
Created on 9 févr. 2014

@author: inso
'''


class Error(Exception):

    def __init__(self, message):
        '''
        Constructor
        '''
        self.message = "Error : " + message


class NotMemberOfCommunityError(Error):

    '''
    Exception raised when adding a community the account is not a member of
    '''

    def __init__(self, account, community):
        '''
        Constructor
        '''
        super() \
            .__init__(account + " is not a member of " + community)


class PersonNotFoundError(Error):

    '''
    Exception raised when looking for a person in a community
    who isnt present in key list
    '''

    def __init__(self, value, community):
        '''
        Constructor
        '''
        super() .__init__(
            "Person looked by " +
            value +
            " in " +
            community +
            " not found ")


class AlgorithmNotImplemented(Error):

    '''
    Exception raised when a coin uses an algorithm not known
    '''

    def __init__(self, algo_name):
        '''
        Constructor
        '''
        super() \
            .__init__("Algorithm " + algo_name + " not implemented.")


class KeyAlreadyUsed(Error):

    '''
    Exception raised trying to add an account using
    a key already used for another account.
    '''

    def __init__(self, new_account, keyid, found_account):
        '''
        Constructor
        '''
        super() .__init__(
            "Cannot add account " +
            new_account.name +
            " : the key " +
            keyid +
            " is already used by " +
            found_account.name)


class NameAlreadyExists(Error):

    '''
    Exception raised trying to add an account using
    a key already used for another account.
    '''

    def __init__(self, account):
        '''
        Constructor
        '''
        super() .__init__(
            "Cannot add account " +
            account.name +
            " the name already exists")


class BadAccountFile(Error):

    '''
    Exception raised trying to add an account using
    a key already used for another account.
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        super() .__init__(
            "File " + path + " is not an account file")


class NotEnoughMoneyError(Error):

    '''
    Exception raised trying to add an account using
    a key already used for another account.
    '''

    def __init__(self, available, currency, nb_inputs, requested):
        '''
        Constructor
        '''
        super() .__init__(
            "Only {0} {1} available in {2} sources, needs {3}"
            .format(available,
                    currency,
                    nb_inputs,
                    requested))
