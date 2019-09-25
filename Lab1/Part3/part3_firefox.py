from selenium import webdriver
from scapy.all import sniff
def main():
    webs = ['https://en.wikipedia.org/wiki/Cat','https://en.wikipedia.org/wiki/Dog','https://en.wikipedia.org/wiki/Egress_filtering','http://web.mit.edu/','http://www.unm.edu/','https://www.cmu.edu/','https://www.berkeley.edu/','https://www.utexas.edu/','https://www.asu.edu/','https://www.utdallas.edu/']
    # for web in webs:
     #   for i in range(10):
     #       driver = webdriver.Firefox()
     #       print(web)
     #       driver.get(web)
     #       print(driver.title)
     #       driver.quit()
     #       exit()
    web = webs[3]
    driver = webdriver.Firefox()
    print(web)
    driver.get(web)
    print(driver.title)
    driver.quit()

main()
