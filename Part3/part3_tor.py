from tbselenium.tbdriver import TorBrowserDriver
from scapy.all import sniff
def main():
    webs = ['https://en.wikipedia.org/wiki/Cat','https://en.wikipedia.org/wiki/Dog','https://en.wikipedia.org/wiki/Egress_filtering','http://web.mit.edu/','http://www.unm.edu/','https://www.cmu.edu/','https://www.berkeley.edu/','https://www.utexas.edu/','https://www.asu.edu/','https://www.utdallas.edu/']
    for web in webs:
        for i in range(10):
            with TorBrowserDriver("/home/class/.local/share/torbrowser/tbb/x86_64/tor-browser_en-US/") as driver:
                driver.get(web)
main()
