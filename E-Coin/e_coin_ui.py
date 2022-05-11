# Erik Fogle
# Date: 04/25/2022
# Description: Minimum-Viable-Product representing my blockchain microservices platform.

import e_coin


def main() -> None:
    """
    Runs a UI to initiate blockchain interaction.
    :return: None
    """

    while True:
        blockchain = e_coin.ECoin()

        print('Welcome to the E-Coin Blockchain Network.')
        print('Currently implemented features:')
        print('Transact on the Network: Enter ‘transact’')
        print('Mine on the Network: Enter ‘mine’')
        print('Check completed blocks on the Network: Enter ‘history’')
        print('Enter ‘main’ at any point to return to this page.' + '\n')
        print('Enter your selection in your terminal: ', end='')
        user_input = input()
        print('\n')

        if user_input == 'main':
            continue
        elif user_input == 'transact':
            print('TRANSACTIONS' + '\n' + '\n')
            print('Enter your address you’ll be sending coins from, the amount '
                  'to send, and recipient address pressing enter after each.' + '\n')
            print('Example: i46… + <ENTER>, 5 + <ENTER>, c3b… + <ENTER>' + '\n')
            print('WARNING! Transactions cannot be canceled or reversed once '
                  'posted. Verify the accuracy of your information before proceeding.' + '\n')
            print('Enter ‘main’ at any point to return to the main page.' + '\n')
            print('Enter your transaction details in your terminal:')

            sender = str(input())
            amount = int(input())
            recipient = str(input())

            if sender or amount or recipient == 'main':
                continue

            if amount != type(int):
                print('Enter a valid integer amount to send: ', end='')
                amount = int(input())

            index = blockchain.new_transaction(sender, amount, recipient)

            response = {'message': f'Transaction will be added to current block {index}'}
            print(response)
            continue
        elif user_input == 'mine':
            print('MINE' + '\n' + '\n')
            print('Enter your node address you’ll be performing work from.')
            print('If block work is successful you’ll receive a success message with relevant block details.')
            print('Enter ‘main’ at any point to return to the main page.' + '\n')
            print('Enter your node address in your terminal.')

            node = input()

            if user_input == 'main':
                continue

            last_block = blockchain.last_block()
            last_proof = last_block['proof']
            proof = blockchain.proof_of_work(last_proof)

            # Sender is '0' to signify that the current node mined a new coin.
            blockchain.new_transaction(
                sender='0',
                amount=1,
                recipient=node,
            )

            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)

            response = {
                'index': block['index'],
                'message': 'Block successfully forged',
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
            }

            print('Mine a new block.')
            continue
        elif user_input == 'history':
            print('HISTORY' + '\n' + '\n')
            print('The forged Network blocks are below.')
            print('Enter ‘main’ at any point to return to the main page.' + '\n')
            print(blockchain.get_chain())

            user_input = input()
            if user_input == 'main':
                continue
            else:
                print('Option not valid. Try again.' + '\n')
        else:
            print('Option not valid. Try again.' + '\n')


if __name__ == '__main__':
    main()
