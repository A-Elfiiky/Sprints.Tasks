open_list = ["[", "{", "("]
close_list = ["]", "}", ")"]

# Function to check
def check_balance(string):
    container = []
    for X in string:
        if X in open_list:
            container.append(X)
        elif X in close_list:
            if len(container) == 0:
                return False
            if open_list[close_list.index(X)] == container[len(container)-1]:
                container.pop()
            else:
                return False
    if len(container) != 0:
        return False
    return True


string = input()
print(check_balance(string))