#-*- coding : utf-8 -*-
#导入模块
#这是python模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time , random , string  , binascii , csv , json ,sys 
#下边是自己的模块
import read_config

#这里是全局变量
driver = "" #这是浏览器对象

profile = ""#设置浏览器基本设置

baiduTitle = ""#设置百度标题,用于判断是否页面已经载入

#这是初始化浏览器的办法
def setHttpsProxy(ip,port,useragent = ""):#参数  ip地址   端口  这是useragent
    global driver , profile#全局变量
    profile = webdriver.FirefoxProfile(read_config.value("firfox_default_file"))#使用本地的firfox的配置文件
    #profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
    if ip !='':
        profile.set_preference('network.proxy.ssl', ip)#这里设置代理ip
        profile.set_preference('network.proxy.ssl_port', port)#这是设置代理的端口
    if useragent != "" :#判断usergaent是否为空
        profile.set_preference('general.useragent.override', useragent)#这是里设置useragent
    profile.update_preferences()
    driver = webdriver.Firefox(profile)#设置浏览器
    driver.maximize_window()#浏览器最大化(这个可选)


def pageReader(times = 10, stoptimes = 3):#页面停留
    global driver#全局变量
    time.sleep(stoptimes*read_config.value("page_stop_time"))#页面停留时间默认3分钟,因为百度会根据时间判断页面的重要性
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    for x in range(1,int(random.uniform(4,times))): #循环  设置循环表示要跳转几次. 上线 的话 可以多添加 几次
        time.sleep(3)   #每次循环之后添加停留时间增加容错率
        num = abs(num + int(random.sample([180,-180],1)[0]))
        driver.execute_script("window.scrollBy(0,%s)" % num,"") #最后了  开始 跳转  就酱



def baidu_list_page_reader():#这个页面 是百度 搜索 列表的阅读 页面   不知带 有用没  先 用用吧
    global driver#全局变量
    time.sleep(5) #先休息5秒防止出错
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    #先要 跳转到 页面 最下边
    for x in xrange(1,11):
        driver.execute_script("window.scrollBy(0,%s)" %(x*num),"") #最后了  开始 跳转  就酱
    #之后开始 随机跳转
    pageReader(10,0.2)


def noClick():#这个办法主要是 放一些 排除 的网站,然后  其他 的网站   都要 点击
        for x in read_config.r_no_click():
            driver.execute_script(x,"")

def baiduNextPage():#这个方法主要实现的是跳转到百度下一页 的页面.时间 的话   可以 根据 电脑 适当 的调节
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("下一页>").click()


#下边是两套规则
def type1():#规则1  除了过滤器其他的随机点
    time.sleep(5) #时间停留5秒 增加系统容错率
    for x in range(read_config.value("baidupagenumber1")):
        time.sleep(3)
        noClick()#过滤掉不要的链接
        content_list_num = driver.find_elements_by_tag_name("h3")
        for x in content_list_num:
            try:
                if suiji():
                    x.find_element_by_tag_name("a").click()
                    time.sleep(5)
                    driver.switch_to_window(driver.window_handles[-1])
                    pageReader()
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    time.sleep(5)
            except:
                pass
        baiduNextPage()

def type2(link):#规则2  点击特定的页面   其他的不点
    time.sleep(5) #时间停留5秒 增加系统容错率
    for x in range(read_config.value("baidupagenumber2")):#这是翻页页数在配置文件设置
        try:
            driver.find_element_by_partial_link_text(link).click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            pageReader()
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(5)
        except:
            pass
        baiduNextPage()


def suiji(sum = 7):#提供随机数  直接返回布尔值  默认为70%
    if int(random.uniform(0,10))<sum:
        return True
    else:
        return False

def baidustart(kew):#百度搜索开始搜索方法
    global driver  , baiduTitle #引入全局变量
    baiduTitle = kew + "_百度搜索"#设置title
    time.sleep(5)
    driver.get("https://www.baidu.com/s?wd="+kew)#开始搜索关键字
    assert baiduTitle in driver.title#确定页面是百度搜索页面

def man(dir):#主要控制办法,接收参数开始执行一次搜索
    global baiduTitle
    #这里应该 有一条 判断,但是  小程序  还是 算了
    try:
        setHttpsProxy(dir['ip'] , dir['port'] , dir['useragent'])#设置代理
        baidustart(dir['keyword'])#开始搜索
        if dir['search_type']:#值为真执行方法1值为假执行方法2
            type1()
        else:
            type2()
        return True
    except:
        print('search.py>>man()>>except')
        return False




def main():#用于测试种种
    search_inf = {'ip':'','port':'','useragent':'','search_type':True,'click_link':'www.51yam.com','keyword':'富硒六味地黄丸'}
    request = man(search_inf)
    print(request)
    

if __name__ == '__main__':
    sys.exit(int(main() or 0))
