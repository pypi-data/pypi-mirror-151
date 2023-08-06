num = 12
def add(x,y):
    return  x+y
class Animal:
    pass

print(__name__)
#  每一个模块 在被python解释器  识别时  会有一个模块的内置属性__name__
# if __name__ =="__main__":
# 一下的代码 是一堆测试我定义的一些 函数 变量 类 的使用情况 测试代码
if __name__ == "__main__":
    print(add(3, 4))
    print("1111")
    print(num)