def isBalanced(s):
    dic = {'[':']','{':'}','(':')'}
    x = ''
    if len(s) % 2 == 0:
        for i in s[:len(s)//2]:
            x += dic[i]
        if x[::-1]==s[len(s)//2:]:
            return 'YES'
    return 'NO'

if __name__ == '__main__':
    print(isBalanced('{{[[(())]]}}'))
    print(isBalanced('{[(])}'))